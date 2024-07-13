from src.helpers import convert_result_to_appropiate_unit


class AggregatedAnalyzer:
    def __init__(self, durations_lst, init_duration_lst) -> None:
        self.durations_lst = durations_lst
        self.init_duration_lst = AggregatedAnalyzer._clean_init_duration_zeros(
            init_duration_lst
        )

    def get_results(self) -> object:
        max_duration = convert_result_to_appropiate_unit(
            max(self.durations_lst) if len(self.durations_lst) > 0 else 0
        )
        min_duration = convert_result_to_appropiate_unit(
            min(self.durations_lst) if len(self.durations_lst) > 0 else 0
        )
        max_init_duration = convert_result_to_appropiate_unit(
            max(self.init_duration_lst) if len(self.init_duration_lst) > 0 else 0
        )

        return {
            "avgDuration": AggregatedAnalyzer._calculate_average_duration(
                self.durations_lst
            ),
            "percentilesDuration": AggregatedAnalyzer._calculate_percentiles_duration(
                self.durations_lst
            ),
            "maxDuration": max_duration,
            "minDuration": min_duration,
            "avgInitDuration": AggregatedAnalyzer._calculate_average_duration(
                self.init_duration_lst
            ),
            "maxInitDuration": max_init_duration,
        }

    @classmethod
    def _calculate_average_duration(cls, dur_lst) -> float:
        if len(dur_lst) <= 0:
            return convert_result_to_appropiate_unit(0)

        total = 0
        for duration in dur_lst:
            total += duration

        return convert_result_to_appropiate_unit(total / len(dur_lst))

    @classmethod
    def _calculate_percentiles_duration(cls, dur_lst):
        if len(dur_lst) <= 0:
            return convert_result_to_appropiate_unit(0)

        duration_lst_sorted = sorted(dur_lst)
        p80_index = int(len(duration_lst_sorted) * (80 / 100))
        p90_index = int(len(duration_lst_sorted) * (90 / 100))
        p95_index = int(len(duration_lst_sorted) * (95 / 100))
        p99_index = int(len(duration_lst_sorted) * (99 / 100))

        return {
            "p80": convert_result_to_appropiate_unit(duration_lst_sorted[p80_index]),
            "p90": convert_result_to_appropiate_unit(duration_lst_sorted[p90_index]),
            "p95": convert_result_to_appropiate_unit(duration_lst_sorted[p95_index]),
            "p99": convert_result_to_appropiate_unit(duration_lst_sorted[p99_index]),
        }

    @classmethod
    def _clean_init_duration_zeros(cls, init_duration_lst):
        init_dur_clean = []
        for init_dur in init_duration_lst:
            if init_dur > 0:
                init_dur_clean.append(init_dur)
        return init_dur_clean
