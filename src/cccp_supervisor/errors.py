from __future__ import annotations


class SupervisorError(RuntimeError):
    """Stable machine-readable failure without payload-bearing details."""

    def __init__(self, code: str, message: str | None = None) -> None:
        self.code = code
        super().__init__(message or code)


class AdapterUnavailable(SupervisorError):
    pass
