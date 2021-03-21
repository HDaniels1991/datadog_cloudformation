import os
import logging
import json
from crhelper import CfnResource
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools import Logger, Tracer
from datadog import Monitor

logger = Logger()
tracer = Tracer()
secrets = json.loads(parameters.get_secret(os.environ['SECRETS']))

helper = CfnResource(
	json_logging=False,
	log_level='DEBUG', 
	boto_level='CRITICAL'
)

DD_monitor = Monitor(secrets["DD_CLIENT_API_KEY"], secrets["DD_CLIENT_APP_KEY"])

@tracer.capture_lambda_handler
@logger.inject_lambda_context
def handler(event, context):
    helper(event, context)


@helper.create
def create(event, context):
    logger.info("Resource Created")
    ResourceProperties = event['ResourceProperties']
    monitor_id = DD_monitor.create_monitor(
        name=ResourceProperties['Name'],
        message=ResourceProperties['Message'],
        priority=ResourceProperties['Priority'],
        functionname=ResourceProperties['FunctionName'],
        tags=ResourceProperties['Tags']
    )    
    return monitor_id


@helper.update  
def update(event, context):
    logger.info("Resource Updated")
    ResourceProperties = event['ResourceProperties']
    monitor_id = DD_monitor.update_monitor(
        monitor_id=event['PhysicalResourceId'],
        name=ResourceProperties['Name'],
        message=ResourceProperties['Message'],
        priority=ResourceProperties['Priority'],
        functionname=ResourceProperties['FunctionName'],
        tags=ResourceProperties['Tags']
    )
    return monitor_id


@helper.delete
def delete(event, context):
    logger.info("Resource Deleted")
    DD_monitor.delete_monitor(event['PhysicalResourceId'])
