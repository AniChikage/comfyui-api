import websocket
import uuid
import json
import urllib.request
import urllib.parse
import requests

import config as CONFIG
#server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

from utils import get_images

#load workflow from file
with open("./workflows/flux1_fp8_workflow_api.json", "r", encoding="utf-8") as f:
    workflow_data = f.read()

workflow = json.loads(workflow_data)

#set the text prompt for our positive CLIPTextEncode
workflow["6"]["inputs"]["text"]  = "masterpiece, best quality, a wide angle shot from the front of a girl posing on a bench in a beautiful meadow,:o face, short and rose hair,perfect legs, perfect arms, perfect eyes,perfect body, perfect feet,blue day sky,shorts, beautiful eyes,sharp focus, full body shot"

#random seed
import random


ws = websocket.WebSocket()
ws.connect(f"ws://{CONFIG.COMFYUI_IP}:{CONFIG.COMFYUI_PORT}/ws?clientId={client_id}")
images = get_images(ws, workflow, client_id)

#Commented out code to display the output images:

for node_id in images:
    for image_data in images[node_id]:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))
        #image.show()
        # save image
        image.save(f"{str(uuid.uuid4())}.png")
