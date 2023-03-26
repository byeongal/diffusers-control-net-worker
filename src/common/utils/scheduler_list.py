from diffusers import (
    DDIMScheduler,
    EulerAncestralDiscreteScheduler,
    EulerDiscreteScheduler,
    HeunDiscreteScheduler,
    LMSDiscreteScheduler,
    StableDiffusionControlNetPipeline,
    UniPCMultistepScheduler,
)

from src.common.enums import SchedulerEnum


def get_scheduler_list(pipe: StableDiffusionControlNetPipeline, scheduler: SchedulerEnum):
    if scheduler == SchedulerEnum.DDIM:
        pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)

    elif scheduler == SchedulerEnum.EULER_A:
        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)

    elif scheduler == SchedulerEnum.EULER:
        pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)

    elif scheduler == SchedulerEnum.LMS:
        pipe.scheduler = LMSDiscreteScheduler.from_config(pipe.scheduler.config)

    elif scheduler == SchedulerEnum.HEUN:
        pipe.scheduler = HeunDiscreteScheduler.from_config(pipe.scheduler.config)

    elif scheduler == SchedulerEnum.UNI_PC:
        pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)

    return pipe
