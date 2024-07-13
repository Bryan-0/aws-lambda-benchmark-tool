from argparse import ArgumentParser, BooleanOptionalAction


def add_arguments_to_parser(parser: ArgumentParser):
    # Auth arguments
    parser.add_argument(
        "--profile",
        help="AWS Profile to use, default profile is used if no other specified.",
        type=str,
    )

    parser.add_argument(
        "--aws-access-key-id",
        help="Your AWS Access Key Id",
        type=str,
    )

    parser.add_argument(
        "--aws-secret-access-key",
        help="Your AWS Secret Key",
        type=str,
    )

    parser.add_argument(
        "--aws-session-token",
        help="Your AWS Session Token",
        type=str,
    )

    # AWS Config
    parser.add_argument(
        "--region",
        help="Region where your Lambda is located. Default is us-east-1",
        default="us-east-1",
        type=str,
    )

    # Function arguments
    parser.add_argument(
        "--function",
        help="Function to invoke, this could be only the name or the full ARN.",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--payload",
        help='Payload sent to the Lambd function, e.g.: \'{"foo": "bar"}\'',
        default="{}",
        type=str,
    )

    parser.add_argument(
        "--num-invocations",
        help="Number of invocations for the Lambda function, default to 10.",
        default=10,
        type=int,
    )

    # Config arguments
    parser.add_argument(
        "--verbose",
        help="This will log each lambda call output along with latency metrics.",
        default=False,
        type=bool,
        action=BooleanOptionalAction,
    )

    parser.add_argument(
        "--workers",
        help="How much workers/processes are used to invoke the lambda function (parallel invocations)",
        default=1,
        type=int,
    )

    parser.add_argument(
        "--export-report-json",
        help="If enabled, it will export a json file to the current directory",
        type=bool,
        default=False,
        action=BooleanOptionalAction,
    )

    parser.add_argument(
        "--export-graph",
        help="If enabled, it will export a line graph about the aggregated latency",
        type=bool,
        default=False,
        action=BooleanOptionalAction,
    )
