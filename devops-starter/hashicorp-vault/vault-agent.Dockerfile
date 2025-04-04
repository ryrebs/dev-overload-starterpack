FROM hashicorp/vault

RUN apk add jq

ENTRYPOINT [ "/bin/vault", "agent" ]

CMD ["-config=/vault/config.hcl"]