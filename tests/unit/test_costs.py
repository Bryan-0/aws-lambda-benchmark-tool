from src.costs import LambdaCostsCalculator


def test_LambdaCostsCalculator_calculate_execution_cost_works_correctly_with_x86():
    billed_time_ms = 15000
    memory_size = 1024
    ephemeral_storage_size = 512
    architecture = "x86"

    result = LambdaCostsCalculator.calculate_execution_cost(
        billed_time_ms, memory_size, ephemeral_storage_size, architecture
    )

    assert result == 0.0002500005


def test_LambdaCostsCalculator_calculate_execution_cost_works_correctly_with_arm():
    billed_time_ms = 15000
    memory_size = 1024
    ephemeral_storage_size = 512
    architecture = "arm"

    result = LambdaCostsCalculator.calculate_execution_cost(
        billed_time_ms, memory_size, ephemeral_storage_size, architecture
    )

    assert result == 0.000200001
