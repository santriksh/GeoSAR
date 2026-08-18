from __future__ import annotations

import cProfile
import pstats
from pathlib import Path
from time import perf_counter


class Profiler:
    """
    Context manager for profiling a code block.

    Example
    -------
    with Profiler():
        result = apply_window_filter(...)
    """

    def __init__(
        self,
        sort_by: str = "cumtime",
        top: int = 25,
        dump_file: str | None = None,
    ):
        self.sort_by = sort_by
        self.top = top
        self.dump_file = dump_file

    def __enter__(self):
        self.profiler = cProfile.Profile()
        self.start = perf_counter()
        self.profiler.enable()
        return self

    def __exit__(self, exc_type, exc, tb):

        self.profiler.disable()

        elapsed = perf_counter() - self.start

        print("\n" + "=" * 60)
        print(f"Elapsed Time : {elapsed:.2f} seconds")
        print("=" * 60)

        stats = pstats.Stats(self.profiler)
        stats.sort_stats(self.sort_by)
        stats.print_stats(self.top)

        if self.dump_file is not None:
            Path(self.dump_file).parent.mkdir(
                parents=True,
                exist_ok=True,
            )
            stats.dump_stats(self.dump_file)