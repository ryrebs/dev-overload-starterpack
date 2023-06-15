FROM hashicorp/vault

RUN apk add jq

ENTRYPOINT [ "/bin/vault", "server"]

CMD ["-config=/vault/config.hcl"]