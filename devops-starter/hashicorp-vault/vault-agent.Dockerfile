FROM vault:latest

RUN apk add jq

RUN unset VAULT_TOKEN

COPY vault-agent-config.hcl config.hcl

ENTRYPOINT [ "/bin/vault", "agent" ]

CMD [ "-config=config.hcl" ]