from typing import Dict, Optional

from pydantic import BaseModel, Field, HttpUrl

from common.enums import ErrorCodeEnum, ErrorMessageEnum, ResponseStatusEnum, SchedulerEnum


class RequestBody(BaseModel):
    prompt: str = Field(..., description="The prompt to guide the image generation.")
    image_url: HttpUrl = Field(..., description="Image URL")
    negative_prompt: Optional[str] = Field(None, description="The prompt not to guide the image generation.")
    guidance_scale: Optional[float] = Field(
        7.5,
        description='Guidance scale as defined in "Classifier-Free Diffusion Guidance" Guidance scale is enabled by setting `guidance_scale >1`. Higher guidance scale encourages to generate images that are closely linked to the text `prompt`,usually at the expense of lower image quality.',
    )
    num_inference_step: Optional[int] = Field(
        50,
        "The number of denoising steps. More denoising steps usually lead to a higher quality image at the expense of slower inference.",
    )
    scheduler: SchedulerEnum = Field(
        SchedulerEnum.DDIM,
        description="A scheduler to be used in combination with `unet` to denoise the encoded image latents.",
    )
    seed: Optional[int] = Field(42, ge=0, le=4294967295, description="The desired seed")


class CustomError(BaseModel):
    error_code: ErrorCodeEnum
    error_message: ErrorMessageEnum


class ResponseBody(BaseModel):
    status: ResponseStatusEnum
    response: Optional[Dict[str, HttpUrl]]
    error: Optional[CustomError]
    updated_at: int
