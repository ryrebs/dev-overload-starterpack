# Read-only permit
path "kv-v1/scraper/apikey/web-proxy" {
  capabilities = [ "read" ]
}

# Read-only permit. Using kv version 2
path "secret/data/scraper/apikey" {
  capabilities = ["read"]
}