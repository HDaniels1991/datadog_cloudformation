# CloudFormation & DataDog

The repo demonstrates how to manage monitors in DataDog using CloudFormation. As of 2021-03-21 only simple monitors alerting for failed lambda invocations can be created.

## Quick Start

All infrastructure here is deployed using the SAM cli.

* Define the SAM config file:

```
 version=0.1
 [default.deploy.parameters]
 profile = "personal"
 stack_name = "datadog-monitor-dev"
 s3_bucket = "custom-resources-dev-20200318"
 s3_prefix = "datadog"
 region = "eu-west-1"
 capabilities = "CAPABILITY_IAM"
 confirm_changeset = true
 tags = "project=\"datadog-monitor-dev\" stage=\"dev\""
```

* Ensure that an integration exists between your AWS account and DataDog account. Detailed instructions are available [here](https://docs.datadoghq.com/integrations/#cat-aws).

* The custom resource requres programmatic access to DataDog. As such you must save your DataDog API Key and App Key in AWS Secrets Manager.

## How it all works!

### The DataDog Module

The DataDog module contains a Monitors class which uses the DataDog API to create, update or delete simple lambda monitors. The create_monitor method creates a DataDog method which alerts for any failed lambda invocations within the last hour.

```python
from datadog import Monitor

LambdaFunctionName = "test-lambda"

DD_monitor = Monitor(api_key, app_key)
monitor_id = DD_monitor.create_monitor(
        name="Test Monitor",
        message=f"{LambdaFunctionName} has failed!\n@recipient@email.com",
        priority=1,
        functionname=LambdaFunctionName,
        tags=["env:dev"]
    )    

```

## Author

Harry Daniels