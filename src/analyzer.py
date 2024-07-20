from base64 import b64decode
import json

from src.costs import LambdaCostsCalculator
from src.lambda_client import LambdaClient
from src.helpers import (
    calculate_average_duration,
    calculate_max_min_duration,
    calculate_percentile_duration,
    convert_duration_unit_to_ms,
    convert_memory_value_to_MB,
    get_memory_value_and_unit,
    get_time_and_unit_duration,
)
from src.payload.dynamic_payload import make_dynamic_payload


class LambdaAnalyzer:
    def __init__(self, lambda_client: LambdaClient, args, worker_num) -> None:
        self.lambda_client = lambda_client
        self.function = args.function
        self.function_conf = self._get_function_config()
        self.payload = args.payload
        self.num_invocations = args.num_invocations
        self.is_dynamic_payload_enabled = args.dynamic_payload
        self.worker_num = worker_num

    def get_results(self) -> object:
        self._print_lambda_params()

        log_results_lst = []
        for execution_num in range(self.num_invocations):
            response = self.lambda_client.invoke_lambda(
                self.function,
                self._build_lambda_payload(execution_num + 1),
            )
            log_results_lst.append(
                b64decode(response.get("LogResult", "")).decode("utf-8")
            )

        return self._generate_report_from_log_results(log_results_lst)

    def _generate_report_from_log_results(self, log_results_lst: list[str]):
        durations = []
        init_durations = []
        max_memory_usages = []
        costs_per_execution = []

        for log_result in log_results_lst:
            for line in log_result.split("\n"):
                if "REPORT" in line:
                    analysis = line.split("\t")
                    for item in analysis:
                        if "Billed Duration:" in item:
                            time, unit = get_time_and_unit_duration(
                                item.split("Billed Duration: ")[-1]
                            )

                            billed_time_ms = convert_duration_unit_to_ms(unit, time)
                            execution_cost = (
                                LambdaCostsCalculator.calculate_execution_cost(
                                    billed_time_ms,
                                    self.function_conf["memorySize"],
                                    self.function_conf["ephemeralStorageSize"],
                                    self.function_conf["architecture"],
                                )
                            )
                            costs_per_execution.append(execution_cost)

                        elif "Init Duration:" in item:
                            time, unit = get_time_and_unit_duration(
                                item.split("Init Duration: ")[-1]
                            )
                            init_durations.append({"time": time, "unit": unit})
                        elif "Duration:" in item:
                            time, unit = get_time_and_unit_duration(
                                item.split("Duration: ")[-1]
                            )
                            durations.append({"time": time, "unit": unit})
                        elif "Max Memory Used:" in item:
                            value, unit = get_memory_value_and_unit(
                                item.split("Max Memory Used: ")[-1]
                            )
                            max_memory_usages.append({"value": value, "unit": unit})

        avg_duration = calculate_average_duration(durations)
        percentiles_duration = calculate_percentile_duration(durations)
        max_duration, min_duration = calculate_max_min_duration(durations)
        max_init, _ = calculate_max_min_duration(init_durations)

        return {
            "avgDuration": avg_duration,
            "p95Duration": percentiles_duration["p95"],
            "maxDuration": max_duration,
            "minDuration": min_duration,
            "maxInitDuration": max_init,
            "totalExecutionCosts": sum(costs_per_execution),
            "durationList": list(
                map(
                    lambda dur: convert_duration_unit_to_ms(dur["unit"], dur["time"]),
                    durations,
                )
            ),
            "initDurationList": list(
                map(
                    lambda dur: convert_duration_unit_to_ms(dur["unit"], dur["time"]),
                    init_durations,
                )
            ),
            "maxMemoryUsagesList": list(
                map(
                    lambda memory: convert_memory_value_to_MB(
                        memory["unit"], memory["value"]
                    ),
                    max_memory_usages,
                )
            ),
        }

    def _print_lambda_params(self):
        print(
            f"Calling Lambda function: `{self.function}` with payload `{self.payload}` for `{self.num_invocations}` times."
        )

    def _build_lambda_payload(self, executionNum):
        if self.is_dynamic_payload_enabled:
            return json.dumps(
                make_dynamic_payload(
                    {
                        "executionNum": executionNum,
                        "lambdaName": self.function,
                        "workerNum": self.worker_num,
                    }
                )
            )

        return self.payload

    def _get_function_config(self):
        config = {}
        response = self.lambda_client.get_function_configuration(self.function)

        config["name"] = response["FunctionName"]
        config["memorySize"] = response["MemorySize"]
        config["ephemeralStorageSize"] = response["EphemeralStorage"]["Size"]
        config["architecture"] = (
            "arm" if "arm64" in response["Architectures"] else "x86"
        )

        return config
