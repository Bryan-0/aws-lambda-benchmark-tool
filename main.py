from multiprocessing import Process, Array, Manager
from argparse import ArgumentParser
from cli_arguments import add_arguments_to_parser
from src.aggregated_analyzer import AggregatedAnalyzer
from src.analyzer import LambdaAnalyzer
from src.lambda_client import LambdaClient

import json

from src.reporter import ResultReporter


def main(
    args,
    duration_results_arr,
    init_results_arr,
    arr_start_idx,
    arr_end_idx,
    worker,
    individual_results_dict,
):
    lambda_client = LambdaClient(args)
    lambda_analyzer = LambdaAnalyzer(lambda_client, args)
    results = lambda_analyzer.get_results()
    duration_result_lst = results["durationList"]
    init_result_lst = results["initDurationList"]

    counter = 0
    init_results_length = len(init_result_lst)
    for i in range(arr_start_idx, arr_end_idx):
        # Populate shared array with results from process
        duration_results_arr[i] = duration_result_lst[counter]
        # Populate Init durations (cold starts) based on results length
        if init_results_length - 1 >= counter:
            init_results_arr[i] = init_result_lst[counter]

        counter += 1

    if args.verbose:
        print(
            f"Individual Results for worker {worker}: {json.dumps(results, indent=4)}"
        )

    individual_results_dict[f"worker{worker}Results"] = results
    return results


def distribute_array_indexes_per_worker(total_executions, worker_count):
    division = int(total_executions / worker_count)
    distribution_output = []

    for i in range(0, total_executions, division):
        distribution_output.append((i, i + division))

    return distribution_output


if __name__ == "__main__":
    # CLI Arguments setup
    parser = ArgumentParser()
    add_arguments_to_parser(parser)
    args = parser.parse_args()

    print(
        f"Starting with {args.workers} {'process' if args.workers == 1 else 'processes'}"
    )

    total_executions = int(args.num_invocations * args.workers)
    process_manager = Manager()
    individual_results_dict = process_manager.dict()
    duration_results_arr = Array("f", total_executions, lock=False)
    init_results_arr = Array("f", total_executions, lock=False)
    arr_distribution = distribute_array_indexes_per_worker(
        total_executions, args.workers
    )
    process_list = []

    for i in range(args.workers):
        arr_start_idx, arr_end_idx = arr_distribution[i]
        process = Process(
            target=main,
            args=(
                args,
                duration_results_arr,
                init_results_arr,
                arr_start_idx,
                arr_end_idx,
                i,
                individual_results_dict,
            ),
        )
        process.start()
        process_list.append(process)

    for process in process_list:
        process.join()

    aggregated_analyzer = AggregatedAnalyzer(duration_results_arr, init_results_arr)
    aggregated_results = aggregated_analyzer.get_results()
    print(f"Aggregated Results: {json.dumps(aggregated_results, indent=4)}")

    if args.export_report_json:
        ResultReporter.export_json_file(
            aggregated_results, dict(individual_results_dict)
        )

    if args.export_graph:
        ResultReporter.export_graph_image(duration_results_arr, args.function)
