import importlib
from config import ALGORITHM_VERSION
import time
import json
import os
class EntropyService:

    def __init__(self, camera_reader):
        self.camera_reader = camera_reader
        self.previous_frame = None
        self.preprevious_frame = None

        version_module = ALGORITHM_VERSION.replace(".", "_")
        modulo = importlib.import_module(f"services.algorithms.v{version_module}")
        self.extraer_entropia = modulo.extraer_entropia

        json_path = os.path.join(os.path.dirname(__file__), "algorithms", "algorithms.json")
        with open(json_path, "r") as f:
            algoritmos = json.load(f)

        config = algoritmos.get(version_module, {"frames": 2})
        self.num_frames = config["frames"]

    def extract_entropy(self):
        if self.num_frames == 3:
            if self.preprevious_frame is None or self.previous_frame is None:
                frame1 = self.camera_reader.read_frame()
                time.sleep(0.1)
                frame2 = self.camera_reader.read_frame()
            else:
                frame1 = self.preprevious_frame
                frame2 = self.previous_frame

            time.sleep(0.1)
            frame3 = self.camera_reader.read_frame()
            self.preprevious_frame = frame2
            self.previous_frame = frame3

            return self.extraer_entropia(frame1, frame2, frame3)
        
        else:
            if self.previous_frame is None:
                frame1 = self.camera_reader.read_frame()
            else:
                frame1 = self.previous_frame

            frame2 = self.camera_reader.read_frame()
            self.previous_frame = frame2

            return self.extraer_entropia(frame1, frame2)  