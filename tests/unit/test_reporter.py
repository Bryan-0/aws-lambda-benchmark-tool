import json
from unittest.mock import patch, mock_open, ANY
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
        ResultReporter.export_json_file(aggregated_results, individual_results_dict)

    os_makedirs_mock.assert_called_once_with("/my_location/output/json", exist_ok=True)
    open_mock.assert_called_once_with("/my_location/output/json/report.json", mode="w")
    open_mock.return_value.write.assert_called_once_with(
        json.dumps(
            {
                "report": {
                    "aggregated": aggregated_results,
                    "individual": individual_results_dict,
                }
            },
            indent=4,
        )
    )


@patch("os.makedirs")
@patch("pathlib.Path.cwd")
@patch("src.reporter.plt")
def test_ResultReporter_export_graph_image(plt_mock, cwd_mock, os_makedirs_mock):
    cwd_mock.return_value = "/my_location"
    duration_results_arr = [1.5, 3.2, 2.3, 1.9, 4.5]
    lambda_name = "pollo"

    ResultReporter.export_graph_image(duration_results_arr, lambda_name)

    os_makedirs_mock.assert_called_once_with(
        "/my_location/output/graphs", exist_ok=True
    )

    plt_mock.plot.assert_called_once_with([1, 2, 3, 4, 5], duration_results_arr)
    plt_mock.ylabel.assert_called_once_with("Duration ms")
    plt_mock.xlabel.assert_called_once_with("No. Executions")
    plt_mock.xticks.assert_called_with(ticks=ANY, labels=ANY)
    plt_mock.title.assert_called_once_with(
        f"Execution Duration for Lambda {lambda_name}"
    )
    plt_mock.savefig.assert_called_once_with(
        "/my_location/output/graphs/durations_graph_report.png"
    )
