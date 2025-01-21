import io
import uuid
import json
import websocket
import boto3
from botocore.client import Config
from PIL import Image
from fastapi import APIRouter, Form, File, UploadFile, Request
from utils import get_images
import asyncio
import config as CONFIG

router = APIRouter()


async def generate_img(prompt, width, height):
    with open("./workflows/flux1_fp8_workflow_api.json", "r", encoding="utf-8") as f:
        workflow_data = f.read()
    workflow = json.loads(workflow_data)
    workflow["6"]["inputs"]["text"] = prompt
    workflow["51"]["inputs"]["width"] = str(width)
    workflow["51"]["inputs"]["height"] = str(height)
    
    client_id = str(uuid.uuid4())
    output_image_name = str(uuid.uuid4())

    ws = websocket.WebSocket()
    ws.connect(f"ws://{CONFIG.COMFYUI_IP}:{CONFIG.COMFYUI_PORT}/ws?clientId={client_id}")
    images = get_images(ws, workflow, client_id)

    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data))
            image.save(f"./images/{output_image_name}.png")

    # 创建S3客户端
    s3 = boto3.client(
        's3',
        endpoint_url=f"http://{CONFIG.OSS_END_POINT}",
        aws_access_key_id=CONFIG.OSS_ACCESS_KEY,
        aws_secret_access_key=CONFIG.OSS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )

    try:
        s3.upload_file(f"./images/{output_image_name}.png", CONFIG.OSS_BUCKET, f"{output_image_name}.png")
        print(f"{output_image_name}.png 已成功上传到 {CONFIG.OSS_BUCKET}/{output_image_name}.png")
        return 200, "ok", output_image_name
    except Exception as e:
        print(f"上传文件时出错: {e}")
        return 500, "error", ""


@router.post("/v1/api/function/text2image")
async def text2image(request: Request, prompt: str=Form(...), height: str=Form(...), width: str=Form(...)):
    try:
        code, msg, output_image_name = await asyncio.wait_for(generate_img(), timeout=60)
        if code == 200:
            return {"status": "200", "msg": "generate successfully", "data": {"image_name": f"{output_image_name}.png"}}
        else:
            return {"status": "500", "msg": "generate failed", "data": {}}
    except asyncio.TimeoutError:
        return {"status": "500", "msg": "timeout", "data": {}}
