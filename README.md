# AWS Lambda Benchmarking Tool

## Overview

This tool allows you to benchmark your AWS Lambda functions by invoking them multiple times in parallel and generating detailed latency reports. The tool provides overall average latency, maximum and minimum latency, and percentile latencies (p80, p90, p95, p99). The results are available in JSON format and as PNG graphs for easy analysis and reporting.

It also gives you an average of the memory utilized by your Lambda, and a cost estimation based on your function configuration for each execution done.


## CLI Arguments

This tool support the following arguments:

| Argument                | Description                                                                                   | Type | Default   | Required |
|-------------------------|-----------------------------------------------------------------------------------------------|------|-----------|----------|
| --function              | Function to invoke, this could be only the name or the full ARN.                              | str  | None      | Yes      |
| --payload               | Static Payload sent to the Lambda function, e.g.: '{"foo": "bar"}'.                           | str  | '{}'      | No       |
| --dynamic-payload       | Use of the make_dynamic_payload function to generate a payload on each lambda execution.      | bool | False     | No       |
| --num-invocations       | Number of invocations for the Lambda function.                                                | int  | 10        | No       |
| --workers               | Define number of processes that are used to invoke the lambda function (parallel invocations) | int  | 1         | No       |
| --export-report-json    | Export a json file report about the aggregated latency, memory and costs.                     | bool | False     | No       |
| --export-graph          | Export graphs about the aggregated latency and memory utilized.                               | bool | False     | No       |
| --verbose               | Log each lambda call output along with latency metrics.                                       | bool | False     | No       |
| --aws-access-key-id     | Your AWS Access Key Id.                                                                       | str  | None      | No       |
| --aws-secret-access-key | Your AWS Secret Key.                                                                          | str  | None      | No       |
| --aws-session-token     | Your AWS Session Token.                                                                       | str  | None      | No       |
| --region                | Region where your Lambda is located.                                                          | str  | us-east-1 | No       |
| --profile               | AWS Profile to use.                                                                           | str  | default   | No       |


If you want to have a programmatic view of the arguments supported, see the `./cli_arguments.py` file.

You can also run the script with only the `--help` flag to view the arguments supported.


## Usage

You have two ways to run this tool:

- ### Using Docker container

1. Clone the repository

```
git clone https://github.com/Bryan-0/aws-lambda-benchmark-tool.git
cd aws-lambda-benchmarking-tool
```

2. Build the docker image
```
docker build --tag lambda-benchmark .
```

3. Run the docker image

Basic example of running the tool:
```
docker run lambda-benchmark --function <FunctionName> --payload '{"docker": "run"}' --num-invocations 10 --workers 1 --aws-access-key-id <your_access_key_id> --aws-secret-access-key <your_secret_access_key>
```

- ### Using Python environment

1. Clone the repository

```
git clone https://github.com/Bryan-0/aws-lambda-benchmark-tool.git
cd aws-lambda-benchmarking-tool
```

2. Create your python environment and install dependencies

```
python3 -m venv venv
source venv/bin/activate
pip install requirements.txt
```

3. Run the python script

```
python main.py --function <FunctionName> --profile brayan --payload '{"foo": "bar"}' --num-invocations 10 --workers 2 --export-report-json --export-graph
```

## Report Examples

Graphs for Duration and Memory utilization:

![image](https://github.com/user-attachments/assets/2305b66a-0157-4ab4-a884-59accf9de5e1)
![image](https://github.com/user-attachments/assets/66dc1df1-940b-461c-bf78-9dc9adff841c)

JSON Report Format:
```json
{
    "report": {
        "lambda": "Testing",
        "aggregated": {
            "avgDuration": "2.45 ms",
            "percentilesDuration": {
                "p80": "1.8 ms",
                "p90": "4.98 ms",
                "p95": "10.5 ms",
                "p99": "14.67 ms"
            },
            "maxDuration": "19.61 ms",
            "minDuration": "0.9 ms",
            "avgInitDuration": "92.72 ms",
            "maxInitDuration": "99.76 ms",
            "avgMaxMemoryUsage": "36 MB",
            "maxMemoryUsage": "37 MB",
            "totalExecutionCosts": 6.1833457e-06
        },
        "individual": {
            "worker1Results": {
                "avgDuration": "2.89 ms",
                "p95Duration": "12.22 ms",
                "maxDuration": "14.6 ms",
                "minDuration": "0.98 ms",
                "maxInitDuration": "90.26 ms",
                "totalExecutionCosts": 7.145847625000001e-07,
                "durationList": [
                    "11.49 ms",
                    ...
                ],
                "initDurationList": [
                    "90.26 ms"
                ],
                "maxMemoryUsagesList": [
                    "37 MB",
                    ...
                ]
            },
            ...
        }
    }
}
```

## How does this tool internally work?

If you are curious about the code itself, the core logic is happening in the `src/analyzer.py` file, the class `LambdaAnalyzer` is in charge of calling the Lambda using the [Invoke API](https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html) through boto3, and then ingesting the LogResults given.

On those logs, we only care for the `REPORT` log line, which contains the duration latency, billed duration and max memory used information used for the later aggregated analysis.

## Issues

If you encounter any issue or bug while running this tool, please open an issue on the repository and I will take a look as soon as I can.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

Note that, when developing this tool, you will need to install the `dev-requirements.txt` dependencies to properly debug and run the unit tests.
