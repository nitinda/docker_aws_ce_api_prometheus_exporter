# AWS Cost Explorer Prometheus Exporter

## Links
* Prometheus Python Client: https://github.com/prometheus/client_python
* Python module reference : https://github.com/movio/aws-prometheus-exporter


This Python module allows you to run AWS API calls through Boto3 and utilise IAM Role to query the AWS api.
It expose the results of api calls as Prometheus metrics. Metrics must be described in YAML. For example:



``` yaml
aws_services_information:
  description: AWS Services running in account
  service: ce
  method: get_cost_and_usage
  method_args: |
    {
      "TimePeriod": {
        "Start": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
        "End": datetime.now().strftime("%Y-%m-%d")
      },
      "Granularity": 'MONTHLY',
      "Metrics": ["BlendedCost","UnblendedCost"],
      "GroupBy": [
        {
          "Type": "DIMENSION",
          "Key": "SERVICE"
        }
      ]
    }
  label_names:
    - aws_service_name
    - blended_cost_amount
    - blended_cost_unit
  search: |
    ResultsByTime[].Groups[].{aws_service_name: Keys[0], blended_cost_amount: Metrics.UnblendedCost.Amount, blended_cost_unit: Metrics.UnblendedCost.Unit, value: `1`}

```

---

## Usage

Running using Docker (on EC2 instance):
```bash
# PERIOD_SECONDS in seconds to query AWS API, as AWS cost explorer api cast money every time we use it.
# EC2 should required a instance profile attached to it and 
# Please replace ROLEARN value to with other appropriate role ARN and Trust relationships should have EC2 instance role as Trusted entities.
# 

docker run --network="host" --rm -it -p 9000:9000 -e "APPPORT=9000"  -e "PERIOD_SECONDS=18000" -e "AWS_DEFAULT_REGION=eu-central-1" -e  -e "ROLEARN=arn:aws:iam::111111111:role/iam_role_nitin_test" nitindas/aws-api-prometheus-exporter:latest

```

Running using Docker (on local):
```bash
# PERIOD_SECONDS in seconds to query AWS API, as AWS cost explorer api cast money every time we use it.
# ACCESS and Secret keys are required as environment variable.
# Please replace ROLEARN value to with other appropriate role ARN and Trust relationships should have Account ARN as Trusted entities.
# 

docker run --network="host" --rm -it -p 9000:9000 -e "APPPORT=9000"  -e "PERIOD_SECONDS=18000" -e "AWS_DEFAULT_REGION=eu-central-1" -e  -e "ROLEARN=arn:aws:iam::111111111:role/iam_role_nitin_test" -e "AWS_ACCESS_KEY_ID=****************" -e "AWS_SECRET_ACCESS_KEY=*********************" nitindas/aws-api-prometheus-exporter:latest

```