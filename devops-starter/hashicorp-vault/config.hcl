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

listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = "true"
}

disable_mlock = true

api_addr = "http://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"
ui = false