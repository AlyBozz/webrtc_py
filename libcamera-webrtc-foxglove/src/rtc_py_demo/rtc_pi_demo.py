import argparse
import asyncio
import json
import logging
import time
from fractions import Fraction

import numpy as np
from aiohttp import web
import aiohttp_cors

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from av import VideoFrame
from picamera2 import Picamera2  # Requires picamera2, which uses libcamera under the hood

logger = logging.getLogger("pc")
pcs = set()

class VideoStream(MediaStreamTrack):
    kind = "video"

    def __init__(self, picam2):
        super().__init__()
        self.picam2 = picam2
        # Start the camera. You can adjust configuration as needed.
        self.picam2.start()

    async def recv(self):
        # Capture a frame from the camera
        image = self.picam2.capture_array()
        if image is None:
            raise RuntimeError("No image captured from Raspberry Pi camera.")

        video_frame = VideoFrame.from_ndarray(image, format="bgr24")
        video_frame.pts = time.time()
        # Set time base based on expected framerate; adjust if needed.
        video_frame.time_base = Fraction(1, 30)
        await asyncio.sleep(0)  # Yield to event loop
        return video_frame

async def offer(request):
    params = await request.json()
    logger.info(f"Received SDP Offer: {params.get('sdp', '')}")
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)
    logger.info(f"Created peer connection for {request.remote}")

    # Setup Picamera2 for Raspberry Pi (libcamera via picamera2)
    picam2 = Picamera2()
    # Configure the camera with a preview configuration; adjust parameters as needed.
    picam2.configure(picam2.create_preview_configuration())

    try:
        video_track = VideoStream(picam2)
        pc.addTrack(video_track)
    except Exception as e:
        logger.error(f"Failed to add video track: {e}")
        return web.Response(
            status=500,
            content_type="application/json",
            text=json.dumps({"error": "Failed to add video track"}),
        )

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        logger.info(f"Connection state: {pc.connectionState}")
        if pc.connectionState in ["failed", "closed", "disconnected"]:
            await pc.close()
            pcs.discard(pc)
            picam2.stop()

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    logger.info(f"Generated SDP Answer: {answer.sdp}")

    try:
        await pc.setLocalDescription(answer)
    except ValueError as e:
        logger.error(f"Failed to set local description: {e}")
        return web.Response(
            status=500,
            content_type="application/json",
            text=json.dumps({"error": "Failed to set local description"}),
        )

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )

async def on_shutdown(app):
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

def main():
    parser = argparse.ArgumentParser(
        description="ROS2 WebRTC streaming node for Raspberry Pi libcamera"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host for HTTP server")
    parser.add_argument("--port", type=int, default=8080, help="Port for HTTP server")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    app = web.Application()
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_methods=["POST", "OPTIONS"],
            allow_headers=["Content-Type"],
            expose_headers="*",
            allow_credentials=True,
        )
    })

    app.on_shutdown.append(on_shutdown)

    resource = cors.add(app.router.add_resource("/offer"))
    cors.add(resource.add_route("POST", offer))
    
    web.run_app(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()