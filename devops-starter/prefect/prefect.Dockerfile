FROM python:3.10-alpine

WORKDIR /prefect

RUN cp /usr/share/zoneinfo/UTC /etc/localtime && echo UTC > /etc/timezone

RUN pip install prefect

ENTRYPOINT [ "prefect" ]

CMD ["orion", "start"]