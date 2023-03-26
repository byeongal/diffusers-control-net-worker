import os
import shutil
from typing import Dict, List

import firebase_admin
from firebase_admin import credentials, db, storage
from PIL import Image
from pydantic import HttpUrl

from common.schemas import ResponseBody
from common.settings import firebase_settings, model_settings


app_name = firebase_settings.app_name


def init():
    cred = credentials.Certificate(firebase_settings.cred_path)
    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": firebase_settings.database_url,
            "storageBucket": firebase_settings.storage_bucket,
        },
    )


def upload_output_images(task_id: str, images: List[Image.Image]) -> Dict[str, HttpUrl]:
    bucket = storage.bucket()
    output_path = os.path.join(model_settings.output_path, task_id)
    result = {}
    for image_no, image in enumerate(images, start=1):
        image_path = os.path.join(output_path, f"{image_no}.png")
        image.save(os.path.join(output_path, f"{image_no}.png"))
        blob = bucket.blob(f"{app_name}/results/{task_id}/{image_no}.png")
        blob.upload_from_filename(image_path)
        blob.make_public()
        url = blob.public_url
        result[f"{image_no}"] = url
    shutil.rmtree(output_path, ignore_errors=True)
    return result


def update_response(task_id: str, response: ResponseBody):
    db.reference(f"{app_name}/tasks/{task_id}").update(response.dict())
