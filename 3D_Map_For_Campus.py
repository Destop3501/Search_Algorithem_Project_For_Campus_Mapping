from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, LineSegs, TextNode
import math

class FlatMap(ShowBase):
    def __init__(self):
        super().__init__()
        
        # --- CAMERA SETUP ---
        self.disableMouse()
        # Wide top-down view to see the full campus
        self.camera.setPos(25, -60, 50)
        self.camera.lookAt(25, 20, 0)
        # --------------------

        self.setBackgroundColor(1, 1, 1, 1)

        # Floor height separation: Ground=0, Floor1=5, Floor2=10
        G  = 0    # Ground floor
        F1 = 5    # 1st floor
        F2 = 10   # 2nd floor
        G1 = -5
        G2 = -10

        # Graph data — spread out on a larger grid so labels don't overlap
        self.graph = {
            # === ENTRANCE ===
            "Entering_Gate":               {"pos": (0,  0,  G),  "connections": ["Path_1"],                                             "size": (0.8, 0.8, 0.8), "model": "box"},
            "Path_1":                      {"pos": (0,  6,  G),  "connections": ["Entering_Gate", "Main_Divition_buildings", "Path_2"], "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Main_Divition_buildings":     {"pos": (12, 6,  G),  "connections": ["Path_1"],                                             "size": (0.8, 0.8, 0.8), "model": "box"},

            # === CANTEEN / GYM AREA ===
            "Path_2":                      {"pos": (0,  12, G),  "connections": ["Path_1", "Path_3"],                                   "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Goda_Canteen":                {"pos": (8,  12, G),  "connections": ["Path_2"],                                             "size": (0.8, 0.8, 0.8), "model": "box"},
            "Goda_Uda_Canteen":            {"pos": (8,  16, F1),  "connections": ["Goda_Canteen"],                                      "size": (0.8, 0.8, 0.8), "model": "box"},
            "Gym":                         {"pos": (8,  20, F2),  "connections": ["Goda_Uda_Canteen"],                                  "size": (0.8, 0.8, 0.8), "model": "box"},

            # === MAIN PATHS ===
            "Path_3":                      {"pos": (0,  20, G),  "connections": ["Path_2"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_4":                      {"pos": (12, 20, G),  "connections": ["Path_3", "Path_5", "Path_6"],                         "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_5":                      {"pos": (12, 10, G),  "connections": ["Path_4"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_6":                      {"pos": (12, 26, G),  "connections": ["Path_4", "Path_7"],                                   "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_7":                      {"pos": (20, 26, G),  "connections": ["Path_6", "Path_8", "Path_10"],                        "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_8":                      {"pos": (20, 18, G),  "connections": ["Path_7", "Path_9"],                                   "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_9":                      {"pos": (24, 18, G),  "connections": ["Path_8", "Medical_Faculty"],                          "size": (0.5, 0.5, 0.5), "model": "circle"},

            # === MEDICAL FACULTY ===
            "Medical_Faculty":             {"pos": (24, 14, G),  "connections": ["Path_9"],                                             "size": (0.8, 0.8, 0.8), "model": "box"},
            "Path_11":                     {"pos": (24, 10, G),  "connections": ["Medical_Faculty", "MF_Dean_Office",
                                                                                    "MF_Meating_Room", "MF_Stare_Case_Floor_2"],        "size": (0.5, 0.5, 0.5), "model": "circle"},
            "MF_Dean_Office":              {"pos": (20, 10, G),  "connections": ["Path_11"],                                            "size": (0.8, 0.8, 0.8), "model": "box"},
            "MF_Meating_Room":             {"pos": (28, 10, G),  "connections": ["Path_11"],                                            "size": (0.8, 0.8, 0.8), "model": "box"},
            "MF_Stare_Case_Floor_2":       {"pos": (24, 6, G),  "connections": ["Path_11", "MF_Stare_Case_Floor_1"],                    "size": (0.8, 0.8, 0.8), "model": "box"},
            
            "Path_12":                     {"pos": (24, 10, G1),  "connections": ["MF_Physiology_Lab", "MF_Skill_Lab", 
                                                                                    "MF_Stare_Case_Floor_1"],                           "size": (0.5, 0.5, 0.5), "model": "circle"},
            "MF_Physiology_Lab":           {"pos": (20, 10, G1),  "connections": ["Path_12"],                                           "size": (0.8, 0.8, 0.8), "model": "box"},
            "MF_Skill_Lab":                {"pos": (28, 10, G1),  "connections": ["Path_12"],                                           "size": (0.8, 0.8, 0.8), "model": "box"},
            "MF_Stare_Case_Floor_1":       {"pos": (24, 6, G1),  "connections": ["MF_Stare_Case_Floor_2", "Path_12",
                                                                                    "MF_Stare_Case_Ground_Floor"],                      "size": (0.8, 0.8, 0.8), "model": "box"},
            
            "Deseption_Hall":              {"pos": (24, 10, G2),  "connections": ["MF_Stare_Case_Ground_Floor"],                        "size": (0.8, 0.8, 0.8), "model": "box"},
            "MF_Stare_Case_Ground_Floor":  {"pos": (24, 6, G2),  "connections": ["MF_Stare_Case_Floor_1", "Deseption_Hall"],            "size": (0.8, 0.8, 0.8), "model": "box"},

            # === IT FACULTY AREA ===
            "Path_10":                     {"pos": (28, 26, G),  "connections": ["Path_7"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Faculty_of_IT":               {"pos": (28, 22, G),  "connections": ["Path_10", "Path_9",
                                                                               "IT_Lecture_Hall_1"],                                    "size": (0.8, 0.8, 0.8), "model": "box"},

            # === GROUND FLOOR — IT BUILDING ===
            "IT_Lecture_Hall_1":           {"pos": (34, 22, G),  "connections": ["Faculty_of_IT", "IT_Lecture_Hall_2"],                 "size": (0.6, 0.6, 0.6), "model": "box"},
            "IT_Lecture_Hall_2":           {"pos": (34, 18, G),  "connections": ["IT_Lecture_Hall_1", "IT_Stare_Case_Ground_Floor"],    "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_Stare_Case_Ground_Floor":  {"pos": (40, 18, G),  "connections": ["IT_Lecture_Hall_2", "IT_Stare_Case_Floor_1"],         "size": (0.8, 0.8, 0.8), "model": "box"},

            # === 1ST FLOOR — IT BUILDING ===
            "IT_Stare_Case_Floor_1":       {"pos": (40, 18, F1), "connections": ["IT_Stare_Case_Ground_Floor", "IT_Stare_Case_Floor_2",
                                                                               "IT_Lab_1"],                                             "size": (0.6, 0.6, 0.6), "model": "box"},
            "IT_Lab_1":                    {"pos": (34, 18, F1), "connections": ["IT_Stare_Case_Floor_1"],                              "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_Lecture_Hall_3":           {"pos": (34, 22, F1), "connections": ["IT_Lab_1"],                                           "size": (0.8, 0.8, 0.8), "model": "box"},

            # === 2ND FLOOR — IT BUILDING ===
            "IT_Stare_Case_Floor_2":       {"pos": (40, 18, F2), "connections": ["IT_Stare_Case_Floor_1", "IT_Lab_2"],                  "size": (0.6, 0.6, 0.6), "model": "box"},
            "IT_Lab_2":                    {"pos": (34, 18, F2), "connections": ["IT_Stare_Case_Floor_2"],                              "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_Lecture_Hall_4":           {"pos": (34, 22, F2), "connections": ["IT_Lab_2"],                                          "size": (0.8, 0.8, 0.8), "model": "box"},
        }

        # 2. Visually create the nodes
        self.visual_nodes = {}
        for name, data in self.graph.items():
            model_name = data['model']
            if model_name == 'circle':
                node = self.make_circle(pos=data["pos"], radius=0.8, color=(0.2, 0.2, 0.8, 1))
            else:
                node = self.loader.loadModel("models/box")
                node.setPos(data['pos'])
                node.setScale(data["size"])
                # Color by floor: ground=dark grey, floor1=blue, floor2=green
                z = data["pos"][2]
                if z == 0:
                    node.setColor(0.2, 0.2, 0.2, 1)
                elif z == 5:
                    node.setColor(0.1, 0.3, 0.8, 1)
                else:
                    node.setColor(0.1, 0.7, 0.2, 1)

            node.reparentTo(self.render)
            self.visual_nodes[name] = node

            # Label
            text = TextNode(name)
            text.setText(name.replace("_", " "))
            text.setTextColor(0, 0, 0, 1)
            text.setAlign(TextNode.ACenter)
            text_path = self.render.attachNewNode(text)
            text_path.setPos(data["pos"][0], data["pos"][1], data["pos"][2] + 1.5)
            text_path.setScale(0.7)
            text_path.setBillboardPointEye()

        # 3. Draw edges dynamically from connections
        lines = LineSegs()
        lines.setThickness(2.5)
        lines.setColor(1, 0.6, 0, 1)  # Orange lines

        drawn = set()
        for name, data in self.graph.items():
            for neighbor in data["connections"]:
                edge = tuple(sorted([name, neighbor]))
                if edge not in drawn:
                    lines.moveTo(self.graph[name]["pos"])
                    lines.drawTo(self.graph[neighbor]["pos"])
                    drawn.add(edge)

        line_node = lines.create()
        NodePath(line_node).reparentTo(self.render)

    def make_circle(self, pos, radius=1.0, color=(1, 1, 1, 1), segments=32):
        """Draw a circle ring using LineSegs."""
        ls = LineSegs()
        ls.setThickness(3.0)
        ls.setColor(*color)
        x, y, z = pos
        for i in range(segments + 1):
            angle = (i / segments) * 2 * math.pi
            cx = x + radius * math.cos(angle)
            cy = y + radius * math.sin(angle)
            if i == 0:
                ls.moveTo(cx, cy, z)
            else:
                ls.drawTo(cx, cy, z)
        return NodePath(ls.create())


app = FlatMap()
app.run()
