"""Result types for Maya skills."""

from enum import IntEnum
from typing import Literal, TypedDict


class ExitCode(IntEnum):
    OK = 0
    WARN = 1
    CONFIG_ERROR = 2
    DATA_ERROR = 3
    EXTERNAL_ERROR = 4
    SAFETY_REFUSAL = 5
    UNEXPECTED = 10


FindingSeverity = Literal["info", "warn", "fail"]


class Finding(TypedDict):
    severity: FindingSeverity
    code: str
    subject: str
    message: str


class Result(TypedDict):
    skill: str
    status: str
    summary: str
    data: dict
    findings: list[Finding]
    metrics: dict
