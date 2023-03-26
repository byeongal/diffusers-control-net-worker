from enum import Enum


class StrEnum(str, Enum):
    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class IntEnum(int, Enum):
    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class SchedulerEnum(StrEnum):
    DDIM: str = "ddim"  # DDIMScheduler
    EULER_A: str = "EulerA"  # EulerAncestralDiscreteScheduler
    EULER: str = "Euler"  # EulerDiscreteScheduler
    LMS: str = "LMS"  # LMSDiscreteScheduler
    HEUN: str = "Heun"  # HeunDiscreteScheduler
    UNI_PC: str = "UniPC"  # UniPCMultistepScheduler


class ResponseStatusEnum(StrEnum):
    PENDING: str = "pending"
    ASSIGNED: str = "assigned"
    COMPLETED: str = "completed"
    ERROR: str = "error"


class ErrorCodeEnum(IntEnum):
    UNKNOWN: int = 1
    VALUE: int = 2


class ErrorMessageEnum(StrEnum):
    UNKNOWN: str = "Unknowns Error {}"
    VALUE: str = "Value Error {}"
