from src.aggregated_analyzer import AggregatedAnalyzer


def test_AggregatedAnalyzer_get_results_returns_aggregated_report_correctly():
    durations_lst = [3.60, 1.45, 7.40, 4.25, 2.22]
    init_durations_lst = [0, 0, 30.6, 0, 56.9]
    max_memory_usages_lst = [35, 35, 35, 36, 36]

    aggregated_analyzer = AggregatedAnalyzer(
        durations_lst, init_durations_lst, max_memory_usages_lst
    )
    report_results = aggregated_analyzer.get_results()

    assert report_results == {
        "avgDuration": "3.78 ms",
        "percentilesDuration": {
            "p80": "7.4 ms",
            "p90": "7.4 ms",
            "p95": "7.4 ms",
            "p99": "7.4 ms",
        },
        "maxDuration": "7.4 ms",
        "minDuration": "1.45 ms",
        "avgInitDuration": "43.75 ms",
        "maxInitDuration": "56.9 ms",
        "avgMaxMemoryUsage": "35 MB",
        "maxMemoryUsage": "36 MB",
    }


def test_AggregatedAnalyzer_get_results_returns_zeros_when_no_list_values_provided():
    durations_lst = []
    init_durations_lst = []
    max_memory_usages_lst = []

    aggregated_analyzer = AggregatedAnalyzer(
        durations_lst, init_durations_lst, max_memory_usages_lst
    )
    report_results = aggregated_analyzer.get_results()

    assert report_results == {
        "avgDuration": "0 ms",
        "percentilesDuration": "0 ms",
        "maxDuration": "0 ms",
        "minDuration": "0 ms",
        "avgInitDuration": "0 ms",
        "maxInitDuration": "0 ms",
        "avgMaxMemoryUsage": "0 MB",
        "maxMemoryUsage": "0 MB",
    }
