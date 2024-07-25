# AWS Lambda Benchmarking Tool

## Overview

This tool allows you to benchmark your AWS Lambda functions by invoking them multiple times in parallel and generating detailed latency reports. The tool provides overall average latency, maximum and minimum latency, and percentile latencies (p80, p90, p95, p99). The results are available in JSON format and as PNG graphs for easy analysis and reporting.

Additionally, it gives you an average of the memory utilized by your Lambda along with the memory utilized on each execution (available in the output reports).

Here are some examples of the reports you can expect to see when benchmarking your Lambda:

[Insert Image]

[Insert Image]


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

...

## Issues

If you encounter any issue or bug while running this tool, please open a issue on the repository and I will take a look as soon as I can.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

Note that, when developing this tool, you will need to install the `dev-requirements.txt` dependencies to properly debug and run the unit tests.
