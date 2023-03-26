import os
from typing import List

import cv2
import numpy as np
import torch
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline
from PIL import Image

from common.enums import SchedulerEnum
from common.schemas import RequestBody
from common.settings import model_settings
from common.utils.etc import download_image
from common.utils.scheduler_list import get_scheduler_list


class StableDiffusionControlNetCannyGenerator:
    def __init__(self) -> None:
        self.pipe = None
        os.makedirs(model_settings.output_path, exist_ok=True)

    def load_model(self, scheduler: SchedulerEnum) -> StableDiffusionControlNetPipeline:
        if self.pipe is None:
            controlnet = ControlNetModel.from_pretrained(
                model_settings.controlnet_model_path, torch_dtype=torch.float16
            )
            self.pipe = StableDiffusionControlNetPipeline.from_pretrained(
                pretrained_model_name_or_path=model_settings.stable_model_path,
                controlnet=controlnet,
                safety_checker=None,
                torch_dtype=torch.float16,
            )
        self.pipe = get_scheduler_list(pipe=self.pipe, scheduler=scheduler)
        self.pipe.to("cuda")

    def controlnet_canny(self, image: Image.Image):
        image = np.array(image)

        image = cv2.Canny(image, 100, 200)
        image = image[:, :, None]
        image = np.concatenate([image, image, image], axis=2)
        image = Image.fromarray(image)

        return image

    def generate_image(
        self,
        body: RequestBody,
    ) -> List[Image.Image]:
        pipe = self.load_model(scheduler=body.scheduler)
        generator = torch.manual_seed(body.seed_generator)
        image = download_image(body.image_url)
        canny_image = self.controlnet_canny(image=image)

        output = pipe(
            prompt=body.prompt,
            image=canny_image,
            negative_prompt=body.negative_prompt,
            num_images_per_prompt=body.num_images_per_prompt,
            num_inference_steps=body.num_inference_step,
            guidance_scale=body.guidance_scale,
            generator=generator,
        ).images

        return output
