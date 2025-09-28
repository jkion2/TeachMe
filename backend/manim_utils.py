from datetime import datetime
from time import perf_counter


class Timer:
    """
    A utility to benchmark and diagnose code performance and detect bottle necks.
    """

    def __init__(self, task: str) -> None:
        self.task = task
        self.start_time = 0
        self.end_time = 0
        self.duration = 0

    def __enter__(self):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting {self.task}")
        self.start_time = perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = perf_counter()
        self.duration = self.end_time - self.start_time
        print(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {self.task} took {self.duration:.3f} seconds"
        )


def load_prompt_template(template_path: str) -> str:
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()
