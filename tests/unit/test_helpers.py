import pytest
import src.helpers as helpers


def test_calculate_average_duration_returns_correct_average():
    durations_lst = [
        {"unit": "ms", "time": 1.50},
        {
            "unit": "ms",
            "time": 2.50,
        },
    ]

    average_duration = helpers.calculate_average_duration(durations_lst)

    assert average_duration == "2.0 ms"


def test_calculate_average_duration_returns_0_when_empty_list():
    assert helpers.calculate_average_duration([]) == 0


@pytest.mark.parametrize(
    "unit, time, expected", [("ms", 5.5, 5.5), ("s", 1.2, 1200), ("m", 1, 60000)]
)
def test_convert_duration_unit_to_ms_returns_correct_conversion(unit, time, expected):
    assert helpers.convert_duration_unit_to_ms(unit, time) == expected


def test_calculate_percentile_duration_returns_correct_percentiles():
    durations_lst = [
        {"unit": "ms", "time": 1.50},
        {
            "unit": "ms",
            "time": 2.50,
        },
        {
            "unit": "ms",
            "time": 1.10,
        },
        {
            "unit": "ms",
            "time": 0.95,
        },
        {
            "unit": "ms",
            "time": 3.50,
        },
        {
            "unit": "ms",
            "time": 0.35,
        },
        {
            "unit": "ms",
            "time": 2.95,
        },
        {
            "unit": "ms",
            "time": 3.25,
        },
        {
            "unit": "ms",
            "time": 1.95,
        },
        {
            "unit": "ms",
            "time": 0.75,
        },
        {
            "unit": "ms",
            "time": 2.99,
        },
    ]

    percentiles = helpers.calculate_percentile_duration(durations_lst)

    assert percentiles == {
        "p80": "2.99 ms",
        "p90": "3.25 ms",
        "p95": "3.5 ms",
        "p99": "3.5 ms",
    }


def test_calculate_percentile_duration_returns_0_when_empty_list():
    assert helpers.calculate_percentile_duration([]) == 0


def test_calculate_max_min_duration_returns_correct_values():
    durations_lst = [
        {"unit": "ms", "time": 1.50},
        {
            "unit": "ms",
            "time": 2.50,
        },
        {
            "unit": "ms",
            "time": 0.55,
        },
    ]

    max_dur, min_dur = helpers.calculate_max_min_duration(durations_lst)

    assert max_dur == "2.5 ms"
    assert min_dur == "0.55 ms"


def test_calculate_max_min_duration_returns_tuple_of_zeros_when_empty_list():
    assert helpers.calculate_max_min_duration([]) == (0, 0)


@pytest.mark.parametrize(
    "ms_result, expected_result", [(2000, "2.0 s"), (500, "500 ms"), (60000, "1.0 m")]
)
def test_convert_result_to_appropiate_unit_returns_correct_conversion(
    ms_result, expected_result
):
    assert helpers.convert_result_to_appropiate_unit(ms_result) == expected_result


@pytest.mark.parametrize(
    "duration_str, expected_result",
    [("1.5 ms", (1.5, "ms")), ("5 s", (5.0, "s")), ("2 m", (2.0, "m"))],
)
def test_get_time_and_unit_duration_returns_expected_split_values(
    duration_str, expected_result
):
    assert helpers.get_time_and_unit_duration(duration_str) == expected_result