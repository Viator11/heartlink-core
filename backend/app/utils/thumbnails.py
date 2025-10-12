from io import BytesIO
from PIL import Image

def make_thumbnail(image_bytes: bytes, size=(512, 512)) -> bytes:
    im = Image.open(BytesIO(image_bytes))
    im = im.convert("RGB")
    im.thumbnail(size)
    out = BytesIO()
    im.save(out, format="JPEG", quality=85, optimize=True)
    return out.getvalue()