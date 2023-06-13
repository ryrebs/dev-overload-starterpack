# Sample basic setup for Hashicorp vault

### Setting up basics (DEV mode)

- On vault client terminal, run:

  `export VAULT_ADDR=http://127.0.0.1:8200`

  `export VAULT_TOKEN=<The root login token>`

### Setting up production mode

- Get unseal keys and initial root token:

  `export VAULT_ADDR=http://127.0.0.1:8200`

  `vault operator init`

- Or with options:

  `vault operator init -key-shares=<default-is-5> -key-threshold=<default-is-3>`

  Example results:

        Unseal Key 1: l0jZQJ+mkSoMLrw3gADJakOp70z7lXM1SyPI1bzAE/dh
        Unseal Key 2: 5DRp/dgPBbQo3ULkDR+U1cSUSBPseNUxrBic4c0bYIVf
        Unseal Key 3: UVbYzUI1YI13tlW1b6dGIHkbSLp3MUlgJAF0M4Om6wn6
        Unseal Key 4: nj1fBaiCPxnCMOJwwIon2hz8WUE9C+TTTXziaEwSFv02
        Unseal Key 5: M0hnqAbRdfWO1VVvRhrimoFkT4/MKQ+OQDKsrALqtYC4

        Initial Root Token: hvs.dElxyhWtCQNXCBKFNnMOid7E

- Create admin token:

  - Create the admin policy file and upload it to vault:

    `vault policy write admin admin-policy.hcl`

  - Create the token:

    `vault token create -format=json -policy="admin"`

    Sample result:

        {
              "request_id": "a3fde833-a6a9-5e2c-7d89-2b5e511ccfea",
              "lease_id": "",
              "lease_duration": 0,
              "renewable": false,
              "data": null,
              "warnings": null,
              "auth": {
                  "client_token": "hvs.CAESIMJUb89cat5cFz8zAaWwUbDvJkysmjH9vFiYrAOG_a-yGh4KHGh2cy5HSFkzalpxRmRrd3pRSHpTZ05Nc1J5S04",
                  "accessor": "6cotHZk6orXoe03IFc5INKMy",
                  "policies": [
                  "admin",
                  "default"
                  ],
                  "token_policies": [
                  "admin",
                  "default"
                  ],
                  "identity_policies": null,
                  "metadata": null,
                  "orphan": false,
                  "entity_id": "",
                  "lease_duration": 2764800,
                  "renewable": true,
                  "mfa_requirement": null
            }
        }

- Make sure to store unseal keys and revoke root token.

---

### Setting a key/value secret and a user token that can read those secrets.

- Enabling key/value v1 secrets engine.

- Run commands:

  `vault secrets enable -path="kv-v1" -description="Test K/V v1" kv`

### Sample storing of key/value pair secrets

_Make sure the current operator has the correct capabilities to run commands below._

- Run commands:

  `vault kv put kv-v1/path <key>=the-value-part>`

  `vault kv put kv-v1/scraper-app/api-key/webproxyapi proxy-api=proxy-api-token`

### Cleanup

- Unset env variables

  `unset VAULT_TOKEN`

  `unset VAULT_ADDR`

  `unset VAULT_NAMESPACE`

- Remove generated files.

  `rm <custom|docker-set-work-dir>/.vault-token`

---

## Setting up Vault with approle and Vault agent and sample python app.

Pre-requisite lessons:

https://developer.hashicorp.com/vault/tutorials/vault-agent/agent-quick-start
https://developer.hashicorp.com/vault/tutorials/vault-agent/agent-read-secrets

### Vault agent act as the main client for the vault instead of your application.

Setup:

A. Vault agent with the same environment with the application/client

B. Vault agent in a separate environment.

Setup B Example:

_Side note_: It's advice to use an admin account instead of a default root account.

- Set up vault with the same setup as above.

  - Enable kv version 2: `vault secrets enable -version=2 kv`

- Create a policy and role for a client app.

  ```
  tee scraper-policy.hcl <<EOF
  # Read-only permit.Using kv version 2
  path "secret/data/scraper/apikey" {
    capabilities = ["read"]
    }
  EOF
  ```

  `vault policy write scraper scraper-policy.hcl`

- Create secrets for the sample client.

  `vault kv put -mount=secret scraper/apikey api_key=api_key_value`

- Enable approle

  `vault auth enable approle`

- Create named role

      vault write auth/approle/role/scraper \ # "scraper" is the role that you want to create
      token_policies="scraper" \ # Policy name
      token_ttl=1h \
      token_max_ttl=4h \
      secret_id_num_uses=10 # Secret ID valid for only 10 uses

- Get secret id and role id.

  `vault read auth/approle/role/scraper/role-id`

  `vault write -f auth/approle/role/scraper/secret-id`

_**Important notes**_:

1. Delivery of secret and role id should be done by a trusted client.

2. Deliver the secret id and role id in a separate manner.

3. Use wrapped tokens to transmit a reference to these credentials instead of passing secret and role ids. See https://developer.hashicorp.com/vault/tutorials/auth-methods/approle

- Get the login token with:

      vault write auth/approle/login \
      role_id=<role-id> \
      secret_id=<secred-id>

- Check if this role or current user is capable of accessing a desired secret.

  `VAULT_TOKEN=<token> vault kv get secret/scraper/apikey`

- Wrapping the secret id/role id with wrap token

  `vault write -wrap-ttl=120s -f auth/approle/role/scraper/secret-id`

- Unwrap the secret id with the generated token during wrapping.

  `VAULT_TOKEN=<token> vault unwrap`

- Setup vault agent. _See vault-agent.Dockerfile and vault-agent-config.hcl_.

- Use a trusted agent (Ansible) that supplies the secret\*id (Can be response wrapped) and/or role_id. See **\*Important notes**\_.

- Create a sample python application as client that uses the vault agent to get secrets from vault.

### Automation with ansible

- TODO: Initial vault setup.

- Encrypted `vars.yml` is for development only.

- Ansible decryption password is `dev`.

- Setup vault (Add user, enable auth and secret engines etc..)

      pipenv run ansible-playbook playbook.yml \
        --tags root,setup \
        --ask-vault-pass \
        --extra-vars "vault_container_name=<container-name>"

- Create admin user

      pipenv run ansible-playbook playbook.yml \
        --tags root,create-admin \
        --ask-vault-pass \
        --extra-vars "vault_container_name=<container-name>"

- Initialize a basic setup for the client

      pipenv run ansible-playbook playbook.yml \
        --tags vault-client-init \
        --ask-vault-pass \
        --extra-vars \
        "vault_container_name=hashicorp-vault_vault_1 \
        client_name=<client_name> \
        vault_admin_token=<admin-token>"


See `playbook.yml` for other tasks.