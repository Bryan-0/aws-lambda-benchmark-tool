def make_dynamic_payload(context: dict):
    """
    If --dynamic-payload is enabled,
    this function will get called on each lambda execution
    and passed as the payload event for the lambda.

    The context parameter will contain a dict with the following information:
    - workerNum: current worker number
    - executionNum: current execution number
    - lambdaName: lambda arn/name provided in the --function arg

    {
        "workerNum": 1,
        "executionNum": 10,
        "lambdaName": "Testing",
    }
    """

    # Return whatever dict you want to be consumed by the Lambda
    return {"dynamicContext": context}
