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

  - Create the admin policy:

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

## Setting a key/value secret and a user token that can read those secrets.

- Enabling key/value v1 secrets engine.

- Run commands:

  `vault secrets enable -path="kv-v1" -description="Test K/V v1" kv`

## Sample storing of key/value pair secrets

_Make sure the current operator has the correct capabilities to run commands below._

- Run commands:

  `vault kv put kv-v1/path <key>=the-value-part>`

  `vault kv put kv-v1/scraper-app/api-key/webproxyapi proxy-api=proxy-api-token`

## Create app policy

- Create the policy Example file: _scraper-policy.hcl_

- See `create admin policy`

- Create token with the create policy

  `vault token create -format=json -policy="scraper"`

## Cleanup

- Unset env variables

  `unset VAULT_TOKEN`

  `unset VAULT_ADDR`

  `unset VAULT_NAMESPACE`

- Remove generated files.
