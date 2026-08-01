from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, LineSegs, TextNode
import math

class FlatMap(ShowBase):
    def __init__(self):
        super().__init__()
        
        # --- CAMERA SETUP ---
        # 1. Disable the default mouse camera control so we can manually position it
        self.disableMouse() 
        
        # 2. Move the camera back (Y=-20) and up into the sky (Z=15)
        self.camera.setPos(5, -20, 15)
        
        # 3. Tell the camera to look down at the center of your map (X=5, Y=5)
        self.camera.lookAt(5, 5, 0)
        # --------------------

        self.setBackgroundColor(1, 1, 1, 1)

        # 1. Store your graph data
        self.graph = {
            "Entering_Gate":                  {"pos": (0, 0, 0),     "connections": ["Path_1"],                                             "size": (0.5, 0.5, 0.5), "model": "box"},
            "Path_1":                         {"pos": (0, 2, 0),     "connections": ["Entering_Gate", "Main_Divition_buildings", "Path_2"], "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Main_Divition_buildings":        {"pos": (10, 2, 0),    "connections": ["Path_1"],                                             "size": (0.5, 0.5, 0.5), "model": "box"},
            
            "Path_2":                         {"pos": (0, 6, 0),     "connections": ["Path_1"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Goda_Canteen":                   {"pos": (5, 6, 0.5),   "connections": ["Path_2"],                                             "size": (0.5, 0.5, 0.5), "model": "box"},
            "Goda_Uda_Canteen":               {"pos": (5, 6, 1),     "connections": ["Goda_Canteen"],                                       "size": (0.5, 0.5, 0.5), "model": "box"},
            "Gym":                            {"pos": (5, 6, 1.5),   "connections": ["Goda_Uda_Canteen"],                                   "size": (0.5, 0.5, 0.5), "model": "box"},

            "Path_3":                         {"pos": (0, 8, 0),     "connections": ["Path_2"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_4":                         {"pos": (10, 8, 0),     "connections": ["Path_3"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_5":                         {"pos": (10, 6, 0),     "connections": ["Path_4"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_6":                         {"pos": (10, 10, 0),     "connections": ["Path_4"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_7":                         {"pos": (12, 10, 0),     "connections": ["Path_6"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_8":                         {"pos": (12, 7, 0),     "connections": ["Path_7"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_9":                         {"pos": (14, 7, 0),     "connections": ["Path_8"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
            "Path_10":                        {"pos": (15, 10, 0),     "connections": ["Path_7"],                                             "size": (0.5, 0.5, 0.5), "model": "circle"},
        }
        
        # 2. Visually create the nodes
        self.visual_nodes = {}
        for name, data in self.graph.items():
            model_name = data['model']
            if model_name == 'circle':
                node = self.make_circle(pos=data["pos"], radius=0.5, color=(0, 0, 0, 1))
            else:
                node = self.loader.loadModel(f"models/{model_name}")
                node.setPos(data['pos'])
                node.setScale(data["size"])
                node.setColor(0, 0, 0, 1)

            node.reparentTo(self.render)
            self.visual_nodes[name] = node

            text = TextNode(name)
            text.setText(name.replace("_", " "))
            text.setTextColor(0, 0, 0, 1)
            text.setAlign(TextNode.ACenter)
            text_path = self.render.attachNewNode(text)
            text_path.setPos(data["pos"][0], data["pos"][1], data["pos"][2] + 1.0)
            text_path.setScale(0.8)
            text_path.setBillboardPointEye()
            
        # 3. Draw the edges (Hallways/Paths) dynamically from connections
        lines = LineSegs()
        lines.setThickness(3.0)
        lines.setColor(1, 1, 0, 1)  # Yellow lines

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
