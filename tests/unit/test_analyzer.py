import json
from unittest.mock import Mock, patch
from src.analyzer import LambdaAnalyzer


@patch('builtins.print')
def test_LambdaAnalyzer_get_results_returns_report_dict_correctly(print_mock):
    lambda_client = Mock()
    boto3_streaming_body_response = Mock()
    args = Mock()
    args.function = "EldenRing"
    args.payload = json.dumps({"git": "gud"})
    args.num_invocations = 1

    lambda_client.invoke_lambda.return_value = {
        "ResponseMetadata": {
            "RequestId": "foobarfoobar",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "date": "Fri, 23 Nov 2001 15:43:24 GMT",
                "content-type": "application/json",
                "content-length": "53",
                "connection": "keep-alive",
                "x-amzn-requestid": "foobarfoobar",
                "x-amzn-remapped-content-length": "0",
                "x-amz-executed-version": "$LATEST",
                "x-amz-log-result": "U1RBUlQgUmVxdWVzdElkOiBmZDQ1YjBmOS0yZWUwLTRmMTItYWNhZi05OWM4NzQwYmM5MTUgVmVyc2lvbjogJExBVEVTVApTb21lIGxvZ3MgaGVyZSEKUmVjZWl2ZWQgZXZlbnQ6ICB7J2RvY2tlcic6ICdydW4nfQpFdmVudCB0eXBlOiAgPGNsYXNzICdkaWN0Jz4KRU5EIFJlcXVlc3RJZDogZmQ0NWIwZjktMmVlMC00ZjEyLWFjYWYtOTljODc0MGJjOTE1ClJFUE9SVCBSZXF1ZXN0SWQ6IGZkNDViMGY5LTJlZTAtNGYxMi1hY2FmLTk5Yzg3NDBiYzkxNQlEdXJhdGlvbjogMi4zMCBtcwlCaWxsZWQgRHVyYXRpb246IDMgbXMJTWVtb3J5IFNpemU6IDEyOCBNQglNYXggTWVtb3J5IFVzZWQ6IDM1IE1CCUluaXQgRHVyYXRpb246IDkyLjE4IG1zCQo=",
                "x-amzn-trace-id": "root=rootfoo;parent=parentfoo;sampled=0;lineage=123457:0",
            },
            "RetryAttempts": 0,
        },
        "StatusCode": 200,
        "LogResult": "U1RBUlQgUmVxdWVzdElkOiBmZDQ1YjBmOS0yZWUwLTRmMTItYWNhZi05OWM4NzQwYmM5MTUgVmVyc2lvbjogJExBVEVTVApTb21lIGxvZ3MgaGVyZSEKUmVjZWl2ZWQgZXZlbnQ6ICB7J2RvY2tlcic6ICdydW4nfQpFdmVudCB0eXBlOiAgPGNsYXNzICdkaWN0Jz4KRU5EIFJlcXVlc3RJZDogZmQ0NWIwZjktMmVlMC00ZjEyLWFjYWYtOTljODc0MGJjOTE1ClJFUE9SVCBSZXF1ZXN0SWQ6IGZkNDViMGY5LTJlZTAtNGYxMi1hY2FmLTk5Yzg3NDBiYzkxNQlEdXJhdGlvbjogMi4zMCBtcwlCaWxsZWQgRHVyYXRpb246IDMgbXMJTWVtb3J5IFNpemU6IDEyOCBNQglNYXggTWVtb3J5IFVzZWQ6IDM1IE1CCUluaXQgRHVyYXRpb246IDkyLjE4IG1zCQo=",
        # Log Result above, once is b64decoded, it should evalute to:
        # "START RequestId: fd45b0f9-2ee0-4f12-acaf-99c8740bc915 Version: $LATEST\nSome logs here!\nReceived event:  {'docker': 'run'}\nEvent type:  <class 'dict'>\nEND RequestId: fd45b0f9-2ee0-4f12-acaf-99c8740bc915\nREPORT RequestId: fd45b0f9-2ee0-4f12-acaf-99c8740bc915\tDuration: 2.30 ms\tBilled Duration: 3 ms\tMemory Size: 128 MB\tMax Memory Used: 35 MB\tInit Duration: 92.18 ms\t\n"
        # Core analysis is done on logs `REPORT` section
        "ExecutedVersion": "$LATEST",
        "Payload": boto3_streaming_body_response,
    }

    lambda_analyzer = LambdaAnalyzer(lambda_client, args)
    report_results = lambda_analyzer.get_results()

    print_mock.assert_called_once_with(
        f"Calling Lambda function: `EldenRing` with payload `{json.dumps({"git": "gud"})}` for `1` times."
    )
    assert report_results == {
        "avgDuration": "2.3 ms",
        "p95Duration": "2.3 ms",
        "maxDuration": "2.3 ms",
        "minDuration": "2.3 ms",
        "maxInitDuration": "92.18 ms",
        "durationList": [2.3],
        "initDurationList": [92.18],
        "maxMemoryUsagesList": [35],
    }
