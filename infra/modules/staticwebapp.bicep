@description('Name of the Static Web App')
param name string

@description('Location for the resource')
param location string

@description('Tags for the resource')
param tags object = {}

resource staticWebApp 'Microsoft.Web/staticSites@2022-09-01' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: 'Free'
    tier: 'Free'
  }
  properties: {
    buildProperties: {
      appLocation: '/frontend'
      outputLocation: 'dist'
      appBuildCommand: 'npm run build'
    }
  }
}

output id string = staticWebApp.id
output name string = staticWebApp.name
output uri string = staticWebApp.properties.defaultHostname
