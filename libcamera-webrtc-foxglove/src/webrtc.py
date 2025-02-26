class WebRTC:
    def __init__(self, signaling_server_url):
        self.signaling_server_url = signaling_server_url
        self.pc = RTCPeerConnection()
        self.local_stream = None

    async def start(self):
        # Connect to the signaling server
        self.signaling_socket = await websockets.connect(self.signaling_server_url)
        await self.signaling_socket.send(json.dumps({"type": "join"}))
        await self.receive_signaling()

    async def receive_signaling(self):
        while True:
            message = await self.signaling_socket.recv()
            data = json.loads(message)

            if data["type"] == "offer":
                await self.handle_offer(data["sdp"])
            elif data["type"] == "answer":
                await self.handle_answer(data["sdp"])
            elif data["type"] == "ice_candidate":
                await self.handle_ice_candidate(data["candidate"])

    async def handle_offer(self, sdp):
        offer = RTCSessionDescription(sdp=sdp, type="offer")
        await self.pc.setRemoteDescription(offer)
        answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(answer)
        await self.send_signaling({"type": "answer", "sdp": answer.sdp})

    async def handle_answer(self, sdp):
        answer = RTCSessionDescription(sdp=sdp, type="answer")
        await self.pc.setRemoteDescription(answer)

    async def handle_ice_candidate(self, candidate):
        await self.pc.addIceCandidate(candidate)

    async def send_signaling(self, message):
        await self.signaling_socket.send(json.dumps(message))

    def add_local_stream(self, stream):
        self.local_stream = stream
        self.pc.addTrack(stream)

    async def close(self):
        await self.signaling_socket.close()
        await self.pc.close()