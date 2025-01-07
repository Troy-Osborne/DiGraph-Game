import networkx as nx
from PIL import Image,ImageDraw
import matplotlib.pyplot as plt
from random import random

DefaultRes=(1080,720)

class digraph:
    def __init__(self,vertices,edges):
        self.vertices=vertices
        self.edges=edges
        self.nx=nx.DiGraph()        
        #for i in vertices:
        self.nx.add_edges_from(self.edges)
    def draw(self, Res=DefaultRes):
        # Create the image with white background
        im = Image.new("RGB", Res, (255, 255, 255))
        dr = ImageDraw.Draw(im)

        # Layout for node positions using spring layout
        pos = nx.spring_layout(self.nx, seed=42)  # Using a fixed seed for reproducibility
        
        # Find the bounds of the layout (min and max values of x and y)
        min_x = min([p[0] for p in pos.values()])
        max_x = max([p[0] for p in pos.values()])
        min_y = min([p[1] for p in pos.values()])
        max_y = max([p[1] for p in pos.values()])

        # Scale the positions to fit within the image
        scale_x = (Res[0] - 100) / (max_x - min_x)  # 100px padding on the left and right
        scale_y = (Res[1] - 100) / (max_y - min_y)  # 100px padding on the top and bottom

        # Translate and scale the positions to fit inside the image
        for node, p in pos.items():
            pos[node] = ((p[0] - min_x) * scale_x + 50, (p[1] - min_y) * scale_y + 50)

        # Draw edges with arrows
        for edge in self.nx.edges():
            start, end = edge
            start_pos = pos[start]
            end_pos = pos[end]
            # Draw line from start to end (edge)
            dr.line([start_pos[0], start_pos[1], end_pos[0], end_pos[1]], fill="black", width=2)
            
            # Draw arrowhead (calculating direction of the arrow)
            arrow_size = 10
            dr.polygon(
                [
                    (end_pos[0], end_pos[1]),  # tip of the arrow
                    (end_pos[0] - arrow_size, end_pos[1] - arrow_size),  # left side
                    (end_pos[0] + arrow_size, end_pos[1] - arrow_size),  # right side
                ],
                fill="black"
            )

        # Draw nodes
        node_radius = 15
        for node, p in pos.items():
            x, y = p
            # Draw a circle for each node
            dr.ellipse(
                (x - node_radius, y - node_radius, x + node_radius, y + node_radius),
                fill="skyblue", outline="black"
            )
            # Draw node label
            dr.text((x - node_radius / 2, y - node_radius / 2), str(node), fill="black")

        # Return the generated image
        return im
