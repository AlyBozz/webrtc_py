import asyncio
import json
import logging
from aiohttp import web
from camera import Camera
from webrtc import WebRTC

logger = logging.getLogger("libcamera-webrtc-foxglove")

async def offer(request):
    params = await request.json()
    logger.info(f"Received SDP Offer: {params['sdp']}")

    web_rtc = WebRTC()
    await web_rtc.set_remote_description(params["sdp"], params["type"])

    answer = await web_rtc.create_answer()
    logger.info(f"Generated SDP Answer: {answer.sdp}")

    return web.Response(
        content_type="application/json",
        text=json.dumps({"sdp": answer.sdp, "type": answer.type}),
    )

async def on_shutdown(app):
    await camera.stop()
    await web_rtc.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    camera = Camera()
    web_rtc = WebRTC()

    app = web.Application()
    app.on_shutdown.append(on_shutdown)

    app.router.add_post("/offer", offer)

    camera.start()
    web.run_app(app, host="0.0.0.0", port=8080)