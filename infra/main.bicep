targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment (e.g., sigap-prod)')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Name of the App Service for the backend')
param backendServiceName string = ''

@description('Name of the Static Web App for the frontend')
param frontendServiceName string = ''

@description('PostgreSQL admin password')
@secure()
param databasePassword string

@description('JWT secret key')
@secure()
param jwtSecretKey string

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

// Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-${environmentName}'
  location: location
  tags: tags
}

// PostgreSQL Flexible Server
module database './modules/postgresql.bicep' = {
  name: 'database'
  scope: rg
  params: {
    name: 'sigap-db-${resourceToken}'
    location: location
    tags: tags
    administratorLogin: 'sigapadmin'
    administratorLoginPassword: databasePassword
    databaseName: 'sigap_db'
  }
}

// App Service Plan (Linux, F1 free tier)
module appServicePlan './modules/appserviceplan.bicep' = {
  name: 'appServicePlan'
  scope: rg
  params: {
    name: 'plan-${environmentName}'
    location: location
    tags: tags
    sku: {
      name: 'F1'
      tier: 'Free'
    }
    kind: 'linux'
  }
}

// Backend App Service
module backend './modules/appservice.bicep' = {
  name: 'backend'
  scope: rg
  params: {
    name: !empty(backendServiceName) ? backendServiceName : 'sigap-api-${resourceToken}'
    location: location
    tags: union(tags, { 'azd-service-name': 'backend' })
    appServicePlanId: appServicePlan.outputs.id
    runtimeName: 'python'
    runtimeVersion: '3.11'
    appSettings: {
      DATABASE_URL_RAW: database.outputs.connectionString
      JWT_SECRET_KEY: jwtSecretKey
      APP_ENV: 'production'
      APP_DEBUG: 'false'
      BMKG_API_URL: 'https://data.bmkg.go.id/api/'
      CORS_ORIGINS: 'https://${frontend.outputs.uri},http://localhost:5173'
      SCM_DO_BUILD_DURING_DEPLOYMENT: 'true'
    }
    appCommandLine: 'gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app'
  }
}

// Frontend Static Web App
module frontend './modules/staticwebapp.bicep' = {
  name: 'frontend'
  scope: rg
  params: {
    name: !empty(frontendServiceName) ? frontendServiceName : 'sigap-web-${resourceToken}'
    location: location
    tags: union(tags, { 'azd-service-name': 'frontend' })
  }
}

// Outputs for azd
output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output BACKEND_URI string = backend.outputs.uri
output FRONTEND_URI string = frontend.outputs.uri
output DATABASE_HOST string = database.outputs.fqdn
