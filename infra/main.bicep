param location string = 'uksouth'
param resourceGroupName string = 'RG_KonpliAI'

resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: resourceGroupName
  location: location
}

// Placeholder for additional resources (App Service, Storage, etc.)
