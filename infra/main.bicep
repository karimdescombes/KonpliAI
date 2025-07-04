// Optional infrastructure provisioning
param location string = 'uksouth'

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'konpliai-rg'
  location: location
}

// Add additional resources such as Web App and Static Web App here
