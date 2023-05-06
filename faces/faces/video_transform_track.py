from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay
from av import VideoFrame
from cv2 import resize, VideoCapture
from face_recognition import face_encodings, face_locations
from flask import g
from uuid import uuid4


pcs = set()
relay = MediaRelay()

class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from another track.
    """

    kind = 'video'

    def __init__(self, track, transform):  # transform is reserved fot future use
        super().__init__()
        self.track = track
        self.transform = transform
        self.vc = VideoCapture(0)
    
    async def rebuild(self, img=None, frame=None):
        return frame

    async def recv(self):
        frame = await self.track.recv()

        ## TODO use this space to add transform filters
        
        small_frame = resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        locations = face_locations(rgb_small_frame)
        encodings = face_encodings(rgb_small_frame, locations)

        ## TODO maybe save here

        encoding = ''
        for i in encodings:
            encoding += str(i) + ','
        print(encoding)
        
        # img = frame.to_ndarray(format="bgr24")
        return self.rebuild(frame=frame)
    
    async def offer(request):
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

        pc = RTCPeerConnection()
        pc_id = "PeerConnection(%s)" % uuid4()
        pcs.add(pc)

        print("Created for %s", request.remote)


