import gc
from datetime import datetime
from io import BytesIO

import requests
import torch
from PIL import Image
from pydantic import HttpUrl


def clear_memory() -> None:
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def download_image(url: HttpUrl) -> Image.Image:
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGB")


def get_now_timestamp() -> int:
    return int(datetime.utcnow().timestamp() * 1000)
