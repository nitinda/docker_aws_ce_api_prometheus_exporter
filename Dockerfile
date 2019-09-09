FROM python:3.7-slim


RUN apt-get update -y && apt-get clean

WORKDIR /opt/aws_prometheus_exporter

COPY requirements.txt /opt/aws_prometheus_exporter/
COPY aws_prometheus_exporter/*.py /opt/aws_prometheus_exporter/
COPY metrics-cost-explorer.yml /mnt/metrics.yml

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="/opt"
ENV APPPORT=9000
ENV PERIOD_SECONDS=20
ENV ROLEARN=None

EXPOSE ${APPPORT}

ENTRYPOINT python -u /opt/aws_prometheus_exporter -p ${APPPORT} -f /mnt/metrics.yml -s ${PERIOD_SECONDS} --assume-role ${ROLEARN}

CMD ["/bin/bash"]