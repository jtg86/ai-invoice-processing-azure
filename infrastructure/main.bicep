@description('Prefix for all resource names.')
param namePrefix string = 'ai-invoice-poc'

@description('Azure region for the deployment.')
param location string = resourceGroup().location

@description('Azure OpenAI resource name (existing).')
param openAiAccountName string

@description('Document Intelligence account name (existing).')
param documentIntelligenceAccountName string

@description('Storage account name (existing).')
param storageAccountName string

@description('App Insights name (existing).')
param appInsightsName string

@description('Function App name (existing).')
param functionAppName string

@description('Logic App name (existing).')
param logicAppName string

@description('Entra ID app registration name (existing).')
param entraAppName string

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' existing = {
  name: storageAccountName
}

resource openAiAccount 'Microsoft.CognitiveServices/accounts@2023-05-01' existing = {
  name: openAiAccountName
}

resource documentIntelligence 'Microsoft.CognitiveServices/accounts@2023-05-01' existing = {
  name: documentIntelligenceAccountName
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: appInsightsName
}

resource functionApp 'Microsoft.Web/sites@2022-09-01' existing = {
  name: functionAppName
}

resource logicApp 'Microsoft.Logic/workflows@2019-05-01' existing = {
  name: logicAppName
}

resource entraApp 'Microsoft.Graph/applications@2023-04-01' existing = {
  name: entraAppName
}

output storageAccountId string = storageAccount.id
output openAiAccountId string = openAiAccount.id
output documentIntelligenceId string = documentIntelligence.id
output appInsightsId string = appInsights.id
output functionAppId string = functionApp.id
output logicAppId string = logicApp.id
output entraAppId string = entraApp.id
