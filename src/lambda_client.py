import boto3


class LambdaClient:
    def __init__(self, args) -> None:
        session = boto3.Session(
            aws_access_key_id=args.aws_access_key_id,
            aws_secret_access_key=args.aws_secret_access_key,
            aws_session_token=args.aws_session_token,
            profile_name=args.profile,
            region_name=args.region,
        )
        self.client = session.client("lambda")

    def invoke_lambda(self, function, payload) -> None:
        return self.client.invoke(
            FunctionName=function,
            LogType="Tail",
            Payload=bytes(payload, encoding="utf-8"),
        )
