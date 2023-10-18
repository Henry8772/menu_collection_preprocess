import io
# from google.cloud import vision
import json
from PIL import Image, ImageDraw, ImageFont
from models.bounding_box import FeatureType, Point, BoundingBox, DSU

def draw_boxes(image, bounds, color):
    """Draws a border around the image using the hints in the vector list.

    Args:
        image: the input image object.
        bounds: list of coordinates for the boxes.
        color: the color of the box.

    Returns:
        An image with colored bounds added.
    """
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon(
            [
                bound.vertices[0].get('x', 0),
                bound.vertices[0].get('y', 0),
                bound.vertices[1].get('x', 0),
                bound.vertices[1].get('y', 0),
                bound.vertices[2].get('x', 0),
                bound.vertices[2].get('y', 0),
                bound.vertices[3].get('x', 0),
                bound.vertices[3].get('y', 0),
            ],
            None,
            color,
        )
    return image







def group_bounding_boxes(bounding_boxes):
    n = len(bounding_boxes)
    dsu = DSU(n)
    
    for i in range(n):
        for j in range(i+1, n):
            if bounding_boxes[i].is_close_enough(bounding_boxes[j]):
                dsu.union(i, j)

    groups = {}
    for i in range(n):
        root = dsu.find(i)
        if root not in groups:
            groups[root] = [bounding_boxes[i]]
        else:
            groups[root].append(bounding_boxes[i])

    # We're returning lists of bounding boxes for each group without merging
    return list(groups.values())

def merge_box_groups(groups):
    merged_boxes = []

    for group in groups:
        merged_box = group[0]
        for box in group[1:]:
            merged_box.merge(box)
        merged_boxes.append(merged_box)

    return merged_boxes



