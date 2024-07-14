from pathlib import Path
import matplotlib.pyplot as plt
import json
import os


class ResultReporter:
    @staticmethod
    def export_json_file(aggr_results: dict, individual_results_dict: dict):
        file_location = f"{Path.cwd()}/output/json/report.json"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)

        json_report_content = {
            "report": {
                "aggregated": aggr_results,
                "individual": individual_results_dict,
            }
        }

        with open(file_location, mode="w") as f:
            f.write(json.dumps(json_report_content, indent=4))

    @staticmethod
    def export_graph_image(duration_results_arr: list, lambda_name: str):
        duration_graph_location = (
            f"{Path.cwd()}/output/graphs/durations_graph_report.png"
        )
        os.makedirs(os.path.dirname(duration_graph_location), exist_ok=True)

        x_axis = [i + 1 for i in range(len(duration_results_arr))]
        plt.plot(x_axis, duration_results_arr)
        plt.ylabel("Duration ms")
        plt.xlabel("No. Executions")
        plt.xticks(ticks=plt.xticks()[0], labels=plt.xticks()[0].astype(int))
        plt.title(f"Execution Duration for Lambda {lambda_name}")
        plt.savefig(duration_graph_location)
