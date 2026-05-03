from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

@dataclass
class Result(Generic[T]):
    ok: bool
    data: T | None = None
    error: str | None = None

    @staticmethod
    def success(data: T | None = None) -> "Result[T]":
        return Result(ok=True, data=data)

    @staticmethod
    def fail(msg: str) -> "Result[T]":
        return Result(ok=False, error=msg)
