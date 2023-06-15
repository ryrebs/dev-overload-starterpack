## Recommended setup using integrated vault storage.
## Additional config refer to: https://developer.hashicorp.com/vault/docs/configuration/storage/raft
## storage "raft" {
##  path    = "/data"
##  node_id = "vault_1"
## }

## Setup using external storage
storage "file" {
  path  = "/data"
}

## Docker container setup
listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = "true"
}

ui = true
## Setting to `true` is recommended only when using integrated storage.
disable_mlock = false

## High Availability Parameters
api_addr = "http://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"