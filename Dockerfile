FROM python:3.7-slim

RUN apt-get update -y && apt-get clean

WORKDIR /opt/aws_prometheus_exporter

COPY requirements.txt /opt/aws_prometheus_exporter/

RUN pip install --no-cache-dir -r requirements.txt

COPY aws_prometheus_exporter/*.py /opt/aws_prometheus_exporter/
COPY metrics.yaml /mnt/metrics.yaml


EXPOSE 9000

ENV PYTHONPATH="/opt"

ENTRYPOINT [ "python", "-u", "/opt/aws_prometheus_exporter", "-p", "9000" ]
CMD [ "-f", "/mnt/metrics.yaml", "-s", "200" ]