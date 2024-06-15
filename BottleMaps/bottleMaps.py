from ui_mainwindow import ui_MainWindow
from PySide6.QtGui import QPixmap
from singleton import singleton
from PIL import Image, ImageDraw
import json, os
from enum import Enum

class WasteType(Enum):
    ball="ball"
    bottle="bottle"
    branch="branch"
    grass="grass"
    leaf="leaf"
    milk_box="milk_box"
    plastic_bag="plastic_bag"
    plastic_garbage="plastic_garbage"

class TiltedWasteData: 
    x:float
    y:float
    type:str

    def __init__(self, x:float, y:float, type:WasteType):
        self.x = x
        self.y = y
        self.type = str(type)

class BottleMapsData:
    
    wastes:list[TiltedWasteData]

    def __init__(self, wastes:list):
        self.wastes = []
        for waste in wastes:
            self.wastes.append(TiltedWasteData(waste["x"], waste["y"], waste["type"]))

    def add_waste(self, waste:TiltedWasteData) -> None:
        self.wastes.append(waste)

    def json(self) -> str:
        dict = \
        {
            "wastes":[]
        }

        for waste in self.wastes:
            waste_dict = \
            {
                "x":waste.x,
                "y":waste.y,
                "type":waste.type
            }
            dict["wastes"].append(waste_dict)

        return json.dumps(dict, indent=4)

@singleton
class BottleMaps:
    data:BottleMapsData

    def __init__(self):
        try:
            json_file_path = os.path.join(os.getcwd(), "BottleMaps/TiltedWasteData.json")
            with open(json_file_path, 'r') as file:
                dict = json.load(file)
                self.data = BottleMapsData(dict)
        except Exception as e:
            self.data = BottleMapsData([])

    def add_waste(self, waste:TiltedWasteData) -> None:
        self.data.add_waste(waste)

    def save_map(self):

        json_string = self.data.json()
        file_name = os.path.join(os.getcwd(), "BottleMaps/TiltedWasteData.json")

        with open(file_name, 'w') as file:
            file.write(json_string)

        img_path = os.path.join(os.getcwd(), "BottleMaps/basemaps.png")
        image = Image.open(img_path)
        draw = ImageDraw.Draw(image)
        for tiltedWasteData in self.data.wastes:
            x = tiltedWasteData.x
            y = tiltedWasteData.y
            radius = 3
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='red', outline='red')

        image.save(os.path.join(os.getcwd(), "BottleMaps/maps.png"))

        ui_MainWindow.label_2.setPixmap(QPixmap(u"BottleMaps/maps.png"))

bottleMaps = BottleMaps()
