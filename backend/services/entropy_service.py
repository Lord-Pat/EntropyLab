import importlib
from config import ALGORITHM_VERSION

class EntropyService:

    def __init__(self, camera_reader):
        self.camera_reader = camera_reader
        self.previous_frame = None
        version_module = ALGORITHM_VERSION.replace(".", "_")
        modulo = importlib.import_module(f"services.algorithms.v{version_module}")
        self.extraer_entropia = modulo.extraer_entropia

    def extract_entropy(self):
        if self.previous_frame is None:
            frame1 = self.camera_reader.read_frame()
        else:
            frame1 = self.previous_frame

        frame2 = self.camera_reader.read_frame()
        self.previous_frame = frame2

        return self.extraer_entropia(frame1, frame2)