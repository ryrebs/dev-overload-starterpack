FROM vault:latest

WORKDIR /vault

RUN apk add jq

RUN unset VAULT_TOKEN

COPY config.hcl config.hcl

COPY admin-policy.hcl admin-policy.hcl

ENTRYPOINT [ "/bin/vault", "server" , "-config=config.hcl"]