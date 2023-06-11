vault {
   ## Vault service address.
   address = "vault:8200"
   tls_skip_verify = true
}

auto_auth {
  method "approle" {
    config = {
      ## File path to the role id 
      role_id_file_path = "role_id_file_path"
      ## File path to the secret id
      secret_id_file_path = "secret_id_file_path-webapp"
      ## Path to the secret_id role: e.g auth/approle/role/webservers/secret-id
      ## If set, `secret_id_file_path` is expected to contain a response wrapping token.
      secret_id_response_wrapping_path = auth/approle/role/scraper/secret-id
    }
  }

  sink "file" {
    config = {
      ## This is the token which the application needed to access the vault.
      ## Will be populated after agent authenticates with vault.
      path = "/vault/.agent-token"
    }
  }
}

template {
   ## File template that tells how to extract the data.
   source      = "/vault/vault-agent.json.tmpl"
   ## Output file.
   destination = "/vault/vault-agent.json"
}

listener "tcp" {
   ## Vault agent client address. Use this address to request for secrets.
   address     = "127.0.0.1:8100"
   tls_disable = true
}

listener "tcp" {
   address     = "127.0.0.1:3000"
   tls_disable = true
   role        = "metrics_only"
}

api_proxy {
   use_auto_auth_token = true
}