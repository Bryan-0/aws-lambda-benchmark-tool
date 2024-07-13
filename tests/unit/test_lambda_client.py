import json
from unittest.mock import Mock, patch

from src.lambda_client import LambdaClient


@patch("boto3.Session")
def test_lambda_client_creates_boto_session_with_provided_arguments(boto3_session):
    args = Mock()
    args.aws_access_key_id = None
    args.aws_secret_access_key = None
    args.aws_session_token = None
    args.profile = "brayan"
    args.region = "us-east-1"

    LambdaClient(args)

    boto3_session.assert_called_once_with(
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_session_token=None,
        profile_name="brayan",
        region_name="us-east-1",
    )
    boto3_session.return_value.client.assert_called_once_with("lambda")


@patch("boto3.Session")
def test_lambda_client_invoke_lambda_with_expected_payload(boto3_session):
    args = Mock()
    args.aws_access_key_id = None
    args.aws_secret_access_key = None
    args.aws_session_token = None
    args.profile = "brayan"
    args.region = "us-east-1"
    payload = json.dumps({"foo": "bar"})

    lambda_client = LambdaClient(args)
    lambda_client.invoke_lambda("MyFunction", payload)

    boto3_session.return_value.client.return_value.invoke.assert_called_once_with(
        FunctionName="MyFunction",
        LogType="Tail",
        Payload=bytes(payload, encoding="utf-8"),
    )
