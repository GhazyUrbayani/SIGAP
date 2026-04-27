@description('Name of the App Service')
param name string

@description('Location for the resource')
param location string

@description('Tags for the resource')
param tags object = {}

@description('ID of the App Service Plan')
param appServicePlanId string

@description('Runtime name')
param runtimeName string = 'python'

@description('Runtime version')
param runtimeVersion string = '3.11'

@description('App settings')
param appSettings object = {}

@description('Startup command')
param appCommandLine string = ''

resource appService 'Microsoft.Web/sites@2022-09-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    serverFarmId: appServicePlanId
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: '${toUpper(runtimeName)}|${runtimeVersion}'
      appCommandLine: appCommandLine
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      appSettings: [for key in objectKeys(appSettings): {
        name: key
        value: appSettings[key]
      }]
    }
  }
}

output id string = appService.id
output name string = appService.name
output uri string = appService.properties.defaultHostName
