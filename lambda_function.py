from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

@tracer.capture_lambda_handler
@logger.inject_lambda_context
def handler(event, context):
    if event['status'] == 'success':
        return
    if event['status'] == 'failure':
        raise ValueError("ValueError exception thrown")
