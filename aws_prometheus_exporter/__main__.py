import time
import argparse

import boto3
import datetime
import sys

from aws_prometheus_exporter import AwsMetric, AwsMetricsCollector, parse_aws_metrics
from prometheus_client import REGISTRY, start_http_server


def parse_args():
    parser = argparse.ArgumentParser(
        description='AWS Prometheus Exporter'
    )
    parser.add_argument(
        '-f', '--metrics-file',
        metavar='PATH',
        dest='metrics_file_path',
        required=True,
        type=str,
        help='path to a YAML-formatted metrics file'
    )
    parser.add_argument(
        '-p', '--port',
        metavar='PORT',
        dest="port",
        required=True,
        type=int,
        help='listen to this port'
    )
    parser.add_argument(
        '--assume-role',
        metavar='ROLEARN',
        dest="assume_role_arn",
        required=True,
        type=str,
        help='Assume role arn'
    )
    parser.add_argument(
        '-s', '--period-seconds',
        metavar='SECONDS',
        dest="period_seconds",
        required=False,
        type=int,
        default=30,
        help='seconds between metric refreshes'
    )
    parser.add_argument(
        '--region-name',
        metavar='REGIONNAME',
        dest="region_name",
        required=False,
        type=str,
        default="eu-central-1",
        help='Region name'
    )
    parser.add_argument(
        '--duration-seconds',
        metavar='DURATIONSECONDS',
        dest="duration_seconds",
        required=False,
        type=int,
        default=3600,
        help='Assume Role session duration seconds'
    )
    return parser.parse_args()

# def filter_none_values(kwargs: dict) -> dict:
#     return {k: v for k, v in kwargs.items() if v is not None}

# def assume_session(role_session_name: str,
#     role_arn: str,
#     duration_seconds: int = 900,
#     region_name: str = "eu-central-1",) -> boto3.Session:
#     assume_role_kwargs = filter_none_values(
#         {
#             "RoleSessionName": role_session_name,
#             "RoleArn": role_arn,
#             "DurationSeconds": duration_seconds,
#         }
#     )
#     credentials = boto3.client("sts").assume_role(**assume_role_kwargs)["Credentials"]
#     create_session_kwargs = filter_none_values(
#         {
#             "aws_access_key_id": credentials["AccessKeyId"],
#             "aws_secret_access_key": credentials["SecretAccessKey"],
#             "aws_session_token": credentials["SessionToken"],
#             "region_name": region_name,
#             "expiry_time": credentials["Expiration"].isoformat(),
#         }
#     )
#     return boto3.Session(**create_session_kwargs)

def main(args):
    port = int(args.port)
    with open(args.metrics_file_path) as metrics_file:
        metrics_yaml = metrics_file.read()
    metrics = parse_aws_metrics(metrics_yaml)
    collector = AwsMetricsCollector(metrics, boto3.client("sts", region_name=args.region_name), args.assume_role_arn, "prometheusAssumeRole", args.duration_seconds)
    REGISTRY.register(collector)
    start_http_server(port)
    print("Serving at port: %s" % port)
    while True:
        try:
            print("Starting the collection again : ", datetime.datetime.now())
            collector.update()
            time.sleep(args.period_seconds)
        except KeyboardInterrupt:
            print("Caught SIGTERM - stopping...")
            break
    print("Done.")



main(parse_args())