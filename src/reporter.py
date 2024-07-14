from pathlib import Path
import json
import os

from src.graphics import Graphics
from src.helpers import extract_lambda_name


class ResultReporter:
    @staticmethod
    def export_json_file(
        aggr_results: dict, individual_results_dict: dict, lambda_name: str
    ):
        extracted_lambda_name = extract_lambda_name(lambda_name)

        file_location = f"{Path.cwd()}/output/json/report_{extracted_lambda_name}.json"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)

        json_report_content = {
            "report": {
                "lambda": extracted_lambda_name,
                "aggregated": aggr_results,
                "individual": individual_results_dict,
            }
        }

        with open(file_location, mode="w") as f:
            f.write(json.dumps(json_report_content, indent=4))

    @staticmethod
    def export_graph_image(
        duration_results_arr: list, max_memory_usages_arr: list, lambda_name: str
    ):
        cwd = Path.cwd()
        extracted_lambda_name = extract_lambda_name(lambda_name)
        duration_graph_filename = (
            f"{cwd}/output/graphs/durations_graph_report_{extracted_lambda_name}.png"
        )
        memory_graph_filename = f"{cwd}/output/graphs/memory_usages_graph_report_{extracted_lambda_name}.png"
        os.makedirs(os.path.dirname(duration_graph_filename), exist_ok=True)

        x_axis = [i + 1 for i in range(len(duration_results_arr))]

        # Duration Graph
        Graphics.draw_line_graph(
            title=f"Execution Duration for Lambda {extracted_lambda_name}",
            x_axis=x_axis,
            x_label="No. Executions",
            y_axis=duration_results_arr,
            y_label="Duration ms",
            filename=duration_graph_filename,
        )
        # Memory Graph
        Graphics.draw_line_graph(
            title=f"Max Memory Usages for Lambda {extracted_lambda_name}",
            x_axis=x_axis,
            x_label="No. Executions",
            y_axis=max_memory_usages_arr,
            y_label="Memory MB",
            filename=memory_graph_filename,
        )
