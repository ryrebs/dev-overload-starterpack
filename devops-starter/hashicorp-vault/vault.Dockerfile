FROM vault:latest

RUN apk add jq

RUN unset VAULT_TOKEN

COPY config.hcl config.hcl

ENTRYPOINT [ "/bin/vault", "server"]

CMD [ "-config=config.hcl" ]
