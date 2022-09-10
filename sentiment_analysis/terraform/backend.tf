# Defines where terraform is going to storage the state of the infraestructure

# Local means that I'm gonna store the state on the local machine disk
# Remote is used when I need to share the state with others developers
terraform {
  backend "local" {}
}