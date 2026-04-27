@description('Name of the App Service Plan')
param name string

@description('Location for the resource')
param location string

@description('Tags for the resource')
param tags object = {}

@description('SKU of the plan')
param sku object

@description('Kind of the plan')
param kind string = 'linux'

resource plan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: name
  location: location
  tags: tags
  kind: kind
  properties: {
    reserved: true // Linux
  }
  sku: sku
}

output id string = plan.id
output name string = plan.name
