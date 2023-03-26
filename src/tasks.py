from functools import partialmethod
from typing import Dict, List

from celery.signals import celeryd_init
from loguru import logger
from PIL import Image
from tqdm import tqdm

from common.enums import ErrorCodeEnum, ErrorMessageEnum, ResponseStatusEnum
from common.schemas import CustomError, RequestBody, ResponseBody
from common.utils import firebase
from common.utils.etc import clear_memory, get_now_timestamp
from diffusion_models.control_net.canny import StableDiffusionControlNetCannyGenerator
from worker import app


model = StableDiffusionControlNetCannyGenerator()


@celeryd_init.connect
def init_worker(**kwargs):
    tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)
    firebase.init()


@app.task(name="inference")
def inference(task_id: str, data: Dict) -> str:
    response_body = ResponseBody(status=ResponseStatusEnum.ASSIGNED, updated_at=get_now_timestamp())
    firebase.update_response(task_id, response_body)
    try:
        request_body: RequestBody = RequestBody(**data)
        result: List[Image.Image] = model.generate_image(request_body)
        response_body.response = firebase.upload_output_images(task_id, result)
        response_body.status = ResponseStatusEnum.COMPLETED
        response_body.updated_at = get_now_timestamp()
        firebase.update_response(task_id, response_body)
        logger.info(f"task_id: {task_id} is done")
    except ValueError as e:
        error = CustomError(
            status_code=ErrorCodeEnum.VALUE,
            error_message=ErrorMessageEnum.VALUE.format(e),
        )
        error_response = ResponseBody(status=ResponseStatusEnum.ERROR, error=error, updated_at=get_now_timestamp())
        firebase.update_response(task_id, error_response)
    except Exception as e:
        error = CustomError(status_code=ErrorCodeEnum.UNKNOWN, error_message=ErrorMessageEnum.format(e))
        error_response = ResponseBody(status=ResponseStatusEnum.ERROR, error=error, updated_at=get_now_timestamp())
        firebase.update_response(task_id, error_response)
    finally:
        clear_memory()
