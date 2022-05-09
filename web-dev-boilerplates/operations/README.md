### Sample Operations setup

*Note* : Replace tags online/offline with dev-online/offline for development

Running service:

`poetry run ansible-playbook playbook.yml --tags online --ask-vault-pass`

Stopping service:

`poetry run ansible-playbook playbook.yml --tags offline --ask-vault-pass`

A. Setup

- Install dependencies: `poetry install`

- Setup the dockerfiles

- Setup vars for context directory (path to docker-compose file)

- Setup .env files

Example:

```
PRIVATE_TOKEN=sample_private_token
PORT=5000
ENV=production
CENTRIFUGO_API_KEY=sample_secret_key
SECRET_KEY=sample_secret_key
FE_PORT=3000
CENTRIFUGO_PORT=8000
```

- Encrypt files: .env and vars.yml with:

`poetry run ansible-vault encrypt <file>`



B. Ports to consider:

Set in their own configs

1. Centrifugo:

   api - 8000

   admin - 9000

2. Prometheus: 9090

B. Ports on env

1. backend - 5000

2. frontend - 3000


C. Self signed certificate

1. Generate key and signed cert:

   openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -keyout certs/key.pem -out certs/cert.pem

2. Generate Diffie-Hellman 

   openssl dhparam -out dhparam.pem 4096

C. Deployment notes

- **Replace all** configs, variables, keys and certificates for `production` environment