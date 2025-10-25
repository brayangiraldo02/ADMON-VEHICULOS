import base64

def decode_image(image_base64: str):
  if image_base64.startswith("data:image/png;base64,"):
    signature = image_base64.split(",")[1]
  else:
    signature = image_base64
  return base64.b64decode(signature)
