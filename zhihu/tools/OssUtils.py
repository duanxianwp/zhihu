import base64
import io
from io import BytesIO
import oss2
from PIL import Image

from zhihu import settings
import time


def upload_img(img):
    auth = oss2.Auth(settings.OSS_KEY, settings.OSS_SECRET)
    bucket = oss2.Bucket(auth, settings.OSS_AREA, settings.OSS_BUCKET)
    img_name = str(int(time.time() * 1000)) + '.png'
    result = bucket.put_object(settings.OSS_PATH + img_name, base64_to_bytes(img))
    if result.status == 200:
        return img_name
    else:
        return None


def base64_to_bytes(img):
    return base64.b64decode(img)
