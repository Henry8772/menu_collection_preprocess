# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y



# class BoundingBox:
#     def __init__(self, vertices,text):
#         self.vertices = vertices
#         self.text = text
#         self.x_min = min(v.x for v in vertices)
#         self.x_max = max(v.x for v in vertices)
#         self.y_min = min(v.y for v in vertices)
#         self.y_max = max(v.y for v in vertices)

#     def is_overlapping(self, other):
#         return not (self.x_max < other.x_min or
#                     self.x_min > other.x_max or
#                     self.y_max < other.y_min or
#                     self.y_min > other.y_max)

#     def is_close_enough(self, other, threshold=5):
#         return not (self.x_max + threshold < other.x_min or
#                     self.x_min - threshold > other.x_max or
#                     self.y_max + threshold < other.y_min or
#                     self.y_min - threshold > other.y_max)

#     def merge(self, other):
#         x_min = min(self.x_min, other.x_min)
#         x_max = max(self.x_max, other.x_max)
#         y_min = min(self.y_min, other.y_min)
#         y_max = max(self.y_max, other.y_max)

#         # Determine the order of the text based on positioning
#         # if self.x_min < other.x_min or (self.x_min == other.x_min and self.y_min < other.y_min):
#         #     self.text += other.text
#         # else:
#         #     self.text = other.text + self.text

#         self.text += other.text

#         self.vertices = [
#             Point(x_min, y_min),
#             Point(x_max, y_min),
#             Point(x_max, y_max),
#             Point(x_min, y_max),
#         ]
#         self.x_min = x_min
#         self.x_max = x_max
#         self.y_min = y_min
#         self.y_max = y_max

from enum import Enum
from PIL import Image, ImageDraw, ImageFont




class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y



class BoundingBox:
    def __init__(self, vertices,text):
        self.vertices = [{'x': v.get('x', 0), 'y': v.get('y', 0)} for v in vertices]
        
        self.text = text
        self.x_min = min(v.get('x', 0) for v in vertices)
        self.x_max = max(v.get('x', 0) for v in vertices)
        self.y_min = min(v.get('y', 0) for v in vertices)
        self.y_max = max(v.get('y', 0) for v in vertices)

    def is_overlapping(self, other):
        return not (self.x_max < other.x_min or
                    self.x_min > other.x_max or
                    self.y_max < other.y_min or
                    self.y_min > other.y_max)

    # def is_close_enough(self, other, threshold=0):
    #     return not (self.x_max + threshold < other.x_min or
    #                 self.x_min - threshold > other.x_max or
    #                 self.y_max + threshold < other.y_min or
    #                 self.y_min - threshold > other.y_max)

    def merge(self, other):
        x_min = min(self.x_min, other.x_min)
        x_max = max(self.x_max, other.x_max)
        y_min = min(self.y_min, other.y_min)
        y_max = max(self.y_max, other.y_max)

        # Determine the order of the text based on positioning
        # if self.x_min < other.x_min or (self.x_min == other.x_min and self.y_min < other.y_min):
        #     self.text += other.text
        # else:
        #     self.text = other.text + self.text

        self.text += other.text

        self.vertices = [
            {"x": x_min, "y": y_min},
            {"x": x_max, "y": y_min},
            {"x": x_max, "y": y_max},
            {"x": x_min, "y": y_max},
        ]
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    @staticmethod
    def compute_edge_distance(vertex, edge):
        """Compute distance from vertex to edge. Edge is represented as a tuple of two points."""
        A, B = edge
        # vector from A to B
        AB = {'x': B['x'] - A['x'], 'y': B['y'] - A['y']}
        # vector from A to vertex
        AV = {'x': vertex['x'] - A['x'], 'y': vertex['y'] - A['y']}
        # scalar projection of AV onto AB
        t = (AV['x']*AB['x'] + AV['y']*AB['y']) / (AB['x']*AB['x'] + AB['y']*AB['y'])
        # find the point on AB closest to the vertex
        if t <= 0:
            # point A is closest to vertex
            return ((vertex['x'] - A['x'])**2 + (vertex['y'] - A['y'])**2)**0.5
        elif t >= 1:
            # point B is closest to vertex
            return ((vertex['x'] - B['x'])**2 + (vertex['y'] - B['y'])**2)**0.5
        else:
            # point on the segment is closest to vertex
            closest = {'x': A['x'] + t*AB['x'], 'y': A['y'] + t*AB['y']}
            return ((vertex['x'] - closest['x'])**2 + (vertex['y'] - closest['y'])**2)**0.5

    def compute_distance_to(self, other_bbox):
        min_distance = float('inf')
        # Create edges from vertices
        edges1 = [(self.vertices[i], self.vertices[(i+1)%4]) for i in range(4)]
        edges2 = [(other_bbox.vertices[i], other_bbox.vertices[(i+1)%4]) for i in range(4)]
        
        # For each vertex in self, compute its distance to each edge of other_bbox
        for v in self.vertices:
            for e in edges2:
                min_distance = min(min_distance, BoundingBox.compute_edge_distance(v, e))
                
        # For each vertex in other_bbox, compute its distance to each edge of self
        for v in other_bbox.vertices:
            for e in edges1:
                min_distance = min(min_distance, BoundingBox.compute_edge_distance(v, e))
        
        return min_distance

    
    def is_close_enough(self, other_bbox):
        return self.compute_distance_to(other_bbox) < 7.5


class DSU:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            else:
                self.parent[rootX] = rootY
                if self.rank[rootX] == self.rank[rootY]:
                    self.rank[rootY] += 1