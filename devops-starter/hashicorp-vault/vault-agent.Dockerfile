FROM vault:latest

WORKDIR /vault

RUN apk add jq

RUN unset VAULT_TOKEN

COPY vault-agent-config.hcl config.hcl

ENTRYPOINT [ "/bin/vault", "agent" , "-config=config.hcl"]