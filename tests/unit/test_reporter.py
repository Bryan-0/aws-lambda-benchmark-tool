import json
from unittest.mock import patch, mock_open, ANY, call
from src.reporter import ResultReporter


@patch("os.makedirs")
@patch("pathlib.Path.cwd")
def test_ResultReporter_export_json_file(cwd_mock, os_makedirs_mock):
    cwd_mock.return_value = "/my_location"
    aggregated_results = {"avgDuration": "24.5 ms"}
    individual_results_dict = {
        "worker0Results": {"avgDuration": "24.5 ms"},
    }

    with patch("builtins.open", mock_open()) as open_mock:
        ResultReporter.export_json_file(
            aggregated_results, individual_results_dict, "FunctionName"
        )

    os_makedirs_mock.assert_called_once_with("/my_location/output/json", exist_ok=True)
    open_mock.assert_called_once_with(
        "/my_location/output/json/report_FunctionName.json", mode="w"
    )
    open_mock.return_value.write.assert_called_once_with(
        json.dumps(
            {
                "report": {
                    "lambda": "FunctionName",
                    "aggregated": aggregated_results,
                    "individual": individual_results_dict,
                }
            },
            indent=4,
        )
    )


@patch("os.makedirs")
@patch("pathlib.Path.cwd")
@patch("src.graphics.plt")
def test_ResultReporter_export_graph_image(plt_mock, cwd_mock, os_makedirs_mock):
    cwd_mock.return_value = "/my_location"
    duration_results_arr = [1.5, 3.2, 2.3, 1.9, 4.5]
    memory_usages_arr = [35, 35, 35, 36, 36]
    lambda_name = "pollo"

    ResultReporter.export_graph_image(
        duration_results_arr, memory_usages_arr, lambda_name
    )

    os_makedirs_mock.assert_called_once_with(
        "/my_location/output/graphs", exist_ok=True
    )

    plt_mock.plot.assert_has_calls(
        [
            call([1, 2, 3, 4, 5], duration_results_arr),
            call([1, 2, 3, 4, 5], memory_usages_arr),
        ]
    )
    plt_mock.ylabel.assert_has_calls(
        [
            call("Duration ms"),
            call("Memory MB"),
        ]
    )
    plt_mock.xlabel.assert_has_calls(
        [
            call("No. Executions"),
            call("No. Executions"),
        ]
    )
    plt_mock.title.assert_has_calls(
        [
            call(f"Execution Duration for Lambda {lambda_name}"),
            call(f"Max Memory Usages for Lambda {lambda_name}"),
        ]
    )
    plt_mock.savefig.assert_has_calls(
        [
            call("/my_location/output/graphs/durations_graph_report_pollo.png"),
            call("/my_location/output/graphs/memory_usages_graph_report_pollo.png"),
        ]
    )
