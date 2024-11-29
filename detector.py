import warnings
import numpy as np
from skimage import io
from face_detection import RetinaFace


warnings.filterwarnings("ignore")


class LandmarksDetector:
    def __init__(self, device="cuda", model_name="resnet50"):
        # Initialize the RetinaFace detector
        self.face_detector = RetinaFace(gpu_id=0)


    def __call__(self, video_frames):
        detected_faces = self.face_detector(video_frames)
        landmarks = []
        for frame_detected in detected_faces:
            try:
                landmarks.append(np.reshape(frame_detected[0][0], (2, 2)))
            except IndexError:
                landmarks.append(None)
        return landmarks
