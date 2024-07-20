PRICE_GB_SECONDS_PER_ARCHITECTURE = {
    "x86": 0.0000166667,  # First 6 Billion executions
    "arm": 0.0000133334,  # First 7.5 Billion executions
}
MONTHLY_EPHEMERAL_PRICE_GB_SECONDS = 0.0000000309
BASE_GB_SIZE_IN_MB = 1024
BASE_FREE_EPHEMERAL_STORAGE = 512


class LambdaCostsCalculator:

    @staticmethod
    def calculate_execution_cost(
        billed_time_ms: int,
        memory_size: int,  # received in MB
        ephemeral_storage_size: int,  # received in MB
        architecture: str,
    ) -> float:
        # This calculation is not including Free Tier - TODO: cli argument to toggle it.
        # Compute time billed
        total_compute_seconds = billed_time_ms / 1000
        total_compute_GB_seconds = total_compute_seconds * (
            memory_size / BASE_GB_SIZE_IN_MB
        )
        total_compute_billed = (
            total_compute_GB_seconds * PRICE_GB_SECONDS_PER_ARCHITECTURE[architecture]
        )

        # Ephemeral total
        # billable_ephemeral_storage = (
        #     ephemeral_storage_size - BASE_FREE_EPHEMERAL_STORAGE
        # )
        # total_ephemeral_GB_seconds = total_compute_seconds * (
        #     billable_ephemeral_storage / BASE_GB_SIZE_IN_MB
        # )
        # total_ephemeral_billed = (
        #     total_ephemeral_GB_seconds * MONTHLY_EPHEMERAL_PRICE_GB_SECONDS
        # )

        return total_compute_billed
