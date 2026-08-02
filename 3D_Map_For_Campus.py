from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, LineSegs, TextNode
import math

class FlatMap(ShowBase):
    def __init__(self):
        super().__init__()
        
        # --- CAMERA SETUP ---
        self.disableMouse()
        # Wide top-down view to show full campus: ME dept (X=-36) to IT building (X=70)
        self.camera.setPos(17, -110, 95)
        self.camera.lookAt(17, 20, 0)
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
            "Path_1":                      {"pos": (0,  8,  G),  "connections": ["Entering_Gate", "Main_Divition_buildings", "Path_2"], "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Main_Divition_buildings":     {"pos": (16, 8,  G),  "connections": ["Path_1"],                                             "size": (0.8, 0.8, 0.8), "model": "box"},

            # === CANTEEN / GYM AREA ===
            "Path_2":                      {"pos": (0,  16, G),  "connections": ["Path_1", "Path_3"],                                   "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Goda_Canteen":                {"pos": (10, 16, G),  "connections": ["Path_2"],                                             "size": (0.8, 0.8, 0.8), "model": "box"},
            "Goda_Uda_Canteen":            {"pos": (10, 20, F1), "connections": ["Goda_Canteen"],                                       "size": (0.8, 0.8, 0.8), "model": "box"},
            "Gym":                         {"pos": (10, 24, F2), "connections": ["Goda_Uda_Canteen"],                                   "size": (0.8, 0.8, 0.8), "model": "box"},

            # === MAIN JUNCTION PATH ===
            "Path_3":                      {"pos": (0,  26, G),  "connections": ["Path_2", "Path_4",
                                                                                  "Machanical_Department_Entenrence",
                                                                                  "Electrical_Department_Entenrence"],                  "size": (0.5, 0.5, 0.5), "model": "circle"},

            # === MECHANICAL ENGINEERING ===
            "Machanical_Department_Entenrence": {"pos": (-28, 26, G), "connections": ["Path_3", "Path_16"],                             "size": (0.8, 0.8, 0.8), "model": "box"},
            "Path_16":                     {"pos": (-28, 20, G), "connections": ["Machanical_Department_Entenrence",
                                                                                  "MD_Stare_Case_Ground_Floor",
                                                                                  "MD_Lab_1", "MD_Lab_2"],                              "size": (0.5, 0.5, 0.5), "model": "circle"},
            "MD_Lab_1":                    {"pos": (-36, 20, G), "connections": ["Path_16"],                                            "size": (0.8, 0.8, 0.8), "model": "box"},
            "MD_Lab_2":                    {"pos": (-20, 20, G), "connections": ["Path_16"],                                            "size": (0.8, 0.8, 0.8), "model": "box"},
            "MD_Stare_Case_Ground_Floor":  {"pos": (-28, 14, G), "connections": ["Path_16", "MD_Stare_Case_Floor_1"],                   "size": (0.8, 0.8, 0.8), "model": "box"},

            # === MECHANICAL ENGINEERING — 1ST FLOOR ===
            "Path_15":                     {"pos": (-28, 20, F1),"connections": ["MD_Stare_Case_Floor_1",
                                                                                  "MD_Lecture_Hall_1", "MD_Lecture_Hall_2"],            "size": (0.5, 0.5, 0.5), "model": "circle"},
            "MD_Lecture_Hall_1":           {"pos": (-36, 20, F1),"connections": ["Path_15"],                                            "size": (0.8, 0.8, 0.8), "model": "box"},
            "MD_Lecture_Hall_2":           {"pos": (-20, 20, F1),"connections": ["Path_15"],                                            "size": (0.8, 0.8, 0.8), "model": "box"},
            "MD_Stare_Case_Floor_1":       {"pos": (-28, 14, F1),"connections": ["MD_Stare_Case_Ground_Floor", "Path_15"],              "size": (0.8, 0.8, 0.8), "model": "box"},

            # === ELECTRICAL DEPARTMENT ===
            "Electrical_Department_Entenrence": {"pos": (0,  34, G),  "connections": ["Path_3", "ED_Lecture_Hall_1",
                                                                                        "ED_Lecture_Hall_2", "ED_Stare_Case_Ground_Floor"], "size": (0.8, 0.8, 0.8), "model": "box"},
            "ED_Lecture_Hall_1":           {"pos": (-6,  34, G), "connections": ["Electrical_Department_Entenrence"],                   "size": (0.8, 0.8, 0.8), "model": "box"},
            "ED_Lecture_Hall_2":           {"pos": (6,   34, G), "connections": ["Electrical_Department_Entenrence"],                   "size": (0.8, 0.8, 0.8), "model": "box"},
            "ED_Stare_Case_Ground_Floor":  {"pos": (0,   40, G), "connections": ["Electrical_Department_Entenrence", "CS_Stare_Case_Floor_1"], "size": (0.8, 0.8, 0.8), "model": "box"},

            # === ELECTRICAL DEPT — 1ST FLOOR (CS) ===
            "CS_Lecture_Hall_1":           {"pos": (-6,  34, F1),"connections": ["Path_13"],                                            "size": (0.8, 0.8, 0.8), "model": "box"},
            "CS_Lecture_Hall_2":           {"pos": (6,   34, F1),"connections": ["Path_13"],                                            "size": (0.8, 0.8, 0.8), "model": "box"},
            "CS_Stare_Case_Floor_1":       {"pos": (0,   40, F1),"connections": ["ED_Stare_Case_Ground_Floor", "EF_Stare_Case_Floor_2",
                                                                                   "Path_13"],                                           "size": (0.8, 0.8, 0.8), "model": "box"},
            "Path_13":                     {"pos": (0,   34, F1),"connections": ["CS_Stare_Case_Floor_1", "CS_Lecture_Hall_1",
                                                                                   "CS_Lecture_Hall_2"],                                 "size": (0.5, 0.5, 0.5), "model": "circle"},

            # === ELECTRICAL DEPT — 2ND FLOOR (EF) ===
            "EF_Lecture_Hall_1":           {"pos": (-6,  34, F2),"connections": ["Path_14"],                                            "size": (0.8, 0.8, 0.8), "model": "box"},
            "EF_Lecture_Hall_2":           {"pos": (6,   34, F2),"connections": ["Path_14"],                                            "size": (0.8, 0.8, 0.8), "model": "box"},
            "EF_Stare_Case_Floor_2":       {"pos": (0,   40, F2),"connections": ["CS_Stare_Case_Floor_1", "Path_14"],                   "size": (0.8, 0.8, 0.8), "model": "box"},
            "Path_14":                     {"pos": (0,   34, F2),"connections": ["EF_Stare_Case_Floor_2", "EF_Lecture_Hall_2",
                                                                                   "EF_Lecture_Hall_1"],                                 "size": (0.5, 0.5, 0.5), "model": "circle"},

            "Path_4":                      {"pos": (16, 26, G),  "connections": ["Path_3", "Path_5", "Path_6"],                         "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_5":                      {"pos": (16, 14, G),  "connections": ["Path_4"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_6":                      {"pos": (16, 34, G),  "connections": ["Path_4", "Path_7"],                                   "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_7":                      {"pos": (26, 34, G),  "connections": ["Path_6", "Path_8", "Path_10"],                        "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_8":                      {"pos": (26, 24, G),  "connections": ["Path_7", "Path_9"],                                   "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_9":                      {"pos": (32, 24, G),  "connections": ["Path_8", "Medical_Faculty"],                          "size": (0.5, 0.5, 0.5), "model": "circle"},

            # === MEDICAL FACULTY ===
            "Medical_Faculty":             {"pos": (32, 20, G),  "connections": ["Path_9"],                                             "size": (0.8, 0.8, 0.8), "model": "box"},
            "Path_11":                     {"pos": (32, 14, G),  "connections": ["Medical_Faculty", "MF_Dean_Office",
                                                                                    "MF_Meating_Room", "MF_Stare_Case_Floor_2"],        "size": (0.5, 0.5, 0.5), "model": "circle"},
            "MF_Dean_Office":              {"pos": (26, 14, G),  "connections": ["Path_11"],                                            "size": (0.8, 0.8, 0.8), "model": "box"},
            "MF_Meating_Room":             {"pos": (38, 14, G),  "connections": ["Path_11"],                                            "size": (0.8, 0.8, 0.8), "model": "box"},
            "MF_Stare_Case_Floor_2":       {"pos": (32,  8, G),  "connections": ["Path_11", "MF_Stare_Case_Floor_1"],                   "size": (0.8, 0.8, 0.8), "model": "box"},

            "Path_12":                     {"pos": (32, 14, G1), "connections": ["MF_Physiology_Lab", "MF_Skill_Lab",
                                                                                    "MF_Stare_Case_Floor_1"],                           "size": (0.5, 0.5, 0.5), "model": "circle"},
            "MF_Physiology_Lab":           {"pos": (26, 14, G1), "connections": ["Path_12"],                                           "size": (0.8, 0.8, 0.8), "model": "box"},
            "MF_Skill_Lab":                {"pos": (38, 14, G1), "connections": ["Path_12"],                                           "size": (0.8, 0.8, 0.8), "model": "box"},
            "MF_Stare_Case_Floor_1":       {"pos": (32,  8, G1), "connections": ["MF_Stare_Case_Floor_2", "Path_12",
                                                                                    "MF_Stare_Case_Ground_Floor"],                      "size": (0.8, 0.8, 0.8), "model": "box"},

            "Deseption_Hall":              {"pos": (32, 14, G2), "connections": ["MF_Stare_Case_Ground_Floor"],                        "size": (0.8, 0.8, 0.8), "model": "box"},
            "MF_Stare_Case_Ground_Floor":  {"pos": (32,  8, G2), "connections": ["MF_Stare_Case_Floor_1", "Deseption_Hall"],           "size": (0.8, 0.8, 0.8), "model": "box"},

            # === IT FACULTY AREA ===
            "Path_10":                     {"pos": (48, 34, G),  "connections": ["Path_7"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Faculty_of_IT":               {"pos": (54, 28, G),  "connections": ["Path_10", "Path_9",
                                                                               "IT_Lecture_Hall_1"],                                    "size": (0.8, 0.8, 0.8), "model": "box"},

            # === GROUND FLOOR — IT BUILDING ===
            "IT_Lecture_Hall_1":           {"pos": (62, 28, G),  "connections": ["Faculty_of_IT", "IT_Lecture_Hall_2"],                 "size": (0.6, 0.6, 0.6), "model": "box"},
            "IT_Lecture_Hall_2":           {"pos": (62, 22, G),  "connections": ["IT_Lecture_Hall_1", "IT_Stare_Case_Ground_Floor",
                                                                                   "IT_G_Lecture_Hall_3"],                               "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_G_Lecture_Hall_3":         {"pos": (56, 22, G),  "connections": ["IT_Lecture_Hall_2", "IT_G_Lecture_Hall_4"],           "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_G_Lecture_Hall_4":         {"pos": (56, 16, G),  "connections": ["IT_G_Lecture_Hall_3", "IT_G_Lab_1"],                  "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_G_Lab_1":                  {"pos": (56, 10, G),  "connections": ["IT_G_Lecture_Hall_4", "IT_G_Lab_2"],                  "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_G_Lab_2":                  {"pos": (50, 10, G),  "connections": ["IT_G_Lab_1", "IT_G_Lab_3"],                           "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_G_Lab_3":                  {"pos": (50, 16, G),  "connections": ["IT_G_Lab_2", "IT_G_Lecture_Hall_5"],                  "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_G_Lecture_Hall_5":         {"pos": (50, 22, G),  "connections": ["IT_G_Lab_3", "IT_G_Lecture_Hall_6"],                  "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_G_Lecture_Hall_6":         {"pos": (44, 22, G),  "connections": ["IT_G_Lecture_Hall_5"],                                "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_Stare_Case_Ground_Floor":  {"pos": (70, 22, G),  "connections": ["IT_Lecture_Hall_2", "IT_Stare_Case_Floor_1"],         "size": (0.8, 0.8, 0.8), "model": "box"},

            # === 1ST FLOOR — IT BUILDING ===
            "IT_Stare_Case_Floor_1":       {"pos": (70, 22, F1), "connections": ["IT_Stare_Case_Ground_Floor", "IT_Stare_Case_Floor_2",
                                                                                   "IT_Lab_1"],                                          "size": (0.6, 0.6, 0.6), "model": "box"},
            "IT_Lab_1":                    {"pos": (62, 22, F1), "connections": ["IT_Stare_Case_Floor_1", "IT_Lecture_Hall_3",
                                                                                   "IT_F1_Lab_2"],                                       "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F1_Lab_2":                 {"pos": (56, 22, F1), "connections": ["IT_Lab_1", "IT_F1_Lab_3"],                           "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F1_Lab_3":                 {"pos": (56, 16, F1), "connections": ["IT_F1_Lab_2", "IT_F1_Lecture_Hall_7"],               "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F1_Lecture_Hall_7":        {"pos": (56, 10, F1), "connections": ["IT_F1_Lab_3", "IT_F1_Lab_4"],                        "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F1_Lab_4":                 {"pos": (50, 10, F1), "connections": ["IT_F1_Lecture_Hall_7", "IT_F1_Lab_5"],               "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F1_Lab_5":                 {"pos": (50, 16, F1), "connections": ["IT_F1_Lab_4", "IT_F1_Lecture_Hall_8"],               "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F1_Lecture_Hall_8":        {"pos": (50, 22, F1), "connections": ["IT_F1_Lab_5", "IT_F1_Lecture_Hall_9"],               "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F1_Lecture_Hall_9":        {"pos": (44, 22, F1), "connections": ["IT_F1_Lecture_Hall_8"],                              "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_Lecture_Hall_3":           {"pos": (62, 28, F1), "connections": ["IT_Lab_1"],                                           "size": (0.8, 0.8, 0.8), "model": "box"},

            # === 2ND FLOOR — IT BUILDING ===
            "IT_Stare_Case_Floor_2":       {"pos": (70, 22, F2), "connections": ["IT_Stare_Case_Floor_1", "IT_Lab_2"],                  "size": (0.6, 0.6, 0.6), "model": "box"},
            "IT_Lab_2":                    {"pos": (62, 22, F2), "connections": ["IT_Stare_Case_Floor_2", "IT_Lecture_Hall_4",
                                                                                   "IT_F2_Lab_6"],                                       "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F2_Lab_6":                 {"pos": (56, 22, F2), "connections": ["IT_Lab_2", "IT_F2_Lab_7"],                           "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F2_Lab_7":                 {"pos": (56, 16, F2), "connections": ["IT_F2_Lab_6", "IT_F2_Lecture_Hall_10"],              "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F2_Lecture_Hall_10":       {"pos": (56, 10, F2), "connections": ["IT_F2_Lab_7", "IT_F2_Lab_8"],                        "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F2_Lab_8":                 {"pos": (50, 10, F2), "connections": ["IT_F2_Lecture_Hall_10", "IT_F2_Lab_9"],              "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F2_Lab_9":                 {"pos": (50, 16, F2), "connections": ["IT_F2_Lab_8", "IT_F2_Lecture_Hall_11"],              "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F2_Lecture_Hall_11":       {"pos": (50, 22, F2), "connections": ["IT_F2_Lab_9", "IT_F2_Lecture_Hall_12"],              "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_F2_Lecture_Hall_12":       {"pos": (44, 22, F2), "connections": ["IT_F2_Lecture_Hall_11"],                             "size": (0.8, 0.8, 0.8), "model": "box"},
            "IT_Lecture_Hall_4":           {"pos": (62, 28, F2), "connections": ["IT_Lab_2"],                                          "size": (0.8, 0.8, 0.8), "model": "box"},
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
