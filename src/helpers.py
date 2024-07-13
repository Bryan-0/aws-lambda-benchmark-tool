def convert_duration_unit_to_ms(unit, time):
    if unit == "s":
        return time * 1000
    if unit == "m":
        return time * 60 * 1000
    if unit == "ms":
        return time


def calculate_average_duration(durations: list[object]):
    if not durations:
        return 0

    total_duration_ms = 0
    for duration in durations:
        total_duration_ms += convert_duration_unit_to_ms(
            duration["unit"], duration["time"]
        )

    result = total_duration_ms / len(durations)

    return convert_result_to_appropiate_unit(result)


def calculate_percentile_duration(durations: list[object]):
    if not durations:
        return 0

    total_duration_ms_lst = []
    for duration in durations:
        total_duration_ms_lst.append(
            convert_duration_unit_to_ms(duration["unit"], duration["time"])
        )

    total_duration_ms_lst.sort()
    p80_index = int(len(durations) * (80 / 100))
    p90_index = int(len(durations) * (90 / 100))
    p95_index = int(len(durations) * (95 / 100))
    p99_index = int(len(durations) * (99 / 100))

    return {
        "p80": convert_result_to_appropiate_unit(total_duration_ms_lst[p80_index]),
        "p90": convert_result_to_appropiate_unit(total_duration_ms_lst[p90_index]),
        "p95": convert_result_to_appropiate_unit(total_duration_ms_lst[p95_index]),
        "p99": convert_result_to_appropiate_unit(total_duration_ms_lst[p99_index]),
    }


def calculate_max_min_duration(durations: list[object]):
    if not durations:
        return 0, 0

    total_duration_ms_lst = []
    for duration in durations:
        total_duration_ms_lst.append(
            convert_duration_unit_to_ms(duration["unit"], duration["time"])
        )

    return convert_result_to_appropiate_unit(
        max(total_duration_ms_lst)
    ), convert_result_to_appropiate_unit(min(total_duration_ms_lst))


def convert_result_to_appropiate_unit(result: float):
    if result >= 1000 and result < 60000:  # ms to s
        return f"{round(result / 1000, 2)} s"
    if result >= 60000:  # ms to m
        return f"{round(result / 60000, 2)} m"

    return f"{round(result, 2)} ms"


def get_time_and_unit_duration(duration_str: str):
    split = duration_str.split(" ")
    return float(split[0]), split[1]
