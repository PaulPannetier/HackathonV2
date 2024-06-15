from roboflow import Roboflow
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class PredictionResult:
    x:float
    y:float
    width:float
    height:float
    confidence:float
    type:str
    type_id:int
    prediction_type:str

    def __init__(self, x, y, width, height, confidence, type, type_id, prediction_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.confidence = confidence
        self.type = type
        self.type_id = type_id
        self.prediction_type = prediction_type

class ImageDetector:
    def __init__(self):
        rf = Roboflow(api_key="uMUVjvL3wu5Jz1Y3sq4J")
        project = rf.workspace("bao-bao-3gkoq").project("vocimgs")
        version = project.version(1)
        self.model = version.model

    def predict(self, imgage_path) -> list[PredictionResult]:
        # img = mpimg.imread(image_path)
        result = self.model.predict(imgage_path, confidence=40, overlap=30).json()
        res = []
        for i in range(0, len(result["predictions"])):
            result["predictions"][i].pop("image_path")
            tmp = result["predictions"][i]
            res.append(PredictionResult(tmp["x"], tmp["y"], tmp["width"], tmp["height"], tmp["confidence"], tmp["class"], tmp["class_id"], tmp["prediction_type"]))
        return res