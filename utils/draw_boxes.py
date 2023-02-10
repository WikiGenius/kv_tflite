import cv2
import numpy as np
import utils
import random
from collections import deque

random.seed(0)

palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)
data_deque = {}

def draw_boxes(img, ratio, dwdh, output_data, conf_thres=0.25, filter_classes=None):
    for i,(batch_id,x0,y0,x1,y1,cls_id,score) in enumerate(output_data):
        cls_id = int(cls_id)
        name = utils.NAMES[cls_id]
        score = round(float(score),3)
        
        if filter_classes and name in filter_classes and score > conf_thres:
            box = np.array([x0,y0,x1,y1])
            box -= np.array(dwdh*2)
            box /= ratio
            box = box.round().astype(np.int32).tolist()
            color = utils.COLORS[name]
            # cv2.rectangle(img,box[:2],box[2:],color,2)
            # cv2.putText(img,name,(box[0], box[1] - 2),cv2.FONT_HERSHEY_SIMPLEX,0.75,[225, 255, 255],thickness=2)  
            draw_ui_box(box, img, label=name, color=color, line_thickness=2)
    return img




def draw_ui_box(x, img, label=None, color=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(
        0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
        
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(str(label), 0, fontScale=tl / 3, thickness=tf)[0]
        # c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        img = draw_border(img, (c1[0], c1[1] - t_size[1] - 3),
                          (c1[0] + t_size[0], c1[1]+3), color, 1, 8, 2)

        # cv2.line(img, c1, c2, color, 30)
        # cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, str(label), (c1[0], c1[1] - 2), 0, tl / 3,
                    [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1, y1 = pt1
    x2, y2 = pt2
    # Top leftfrom collections import deque (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

    cv2.rectangle(img, (x1 + r, y1), (x2 - r, y2), color, -1, cv2.LINE_AA)
    cv2.rectangle(img, (x1, y1 + r), (x2, y2 - r - d), color, -1, cv2.LINE_AA)

    cv2.circle(img, (x1 + r, y1+r), 2, color, 12)
    cv2.circle(img, (x2 - r, y1+r), 2, color, 12)
    cv2.circle(img, (x1 + r, y2-r), 2, color, 12)
    cv2.circle(img, (x2 - r, y2-r), 2, color, 12)

    return img



def drawtrails(data_deque, id, color, img):
    # draw trail
    for i in range(1, len(data_deque[id])):
        # check if on buffer value is none
        if data_deque[id][i - 1] is None or data_deque[id][i] is None:
            continue

        # generate dynamic thickness of trails
        thickness = int(np.sqrt(64 / float(i + i)) * 1.5)
        
        # draw trails
        cv2.line(img, data_deque[id][i - 1], data_deque[id][i], color, thickness)



def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    if label == 0:  # person  #BGR
        color = (85, 45, 255)
    elif label == 2:  # Car
        color = (222, 82, 175)
    elif label == 3:  # Motobike
        color = (0, 204, 255)
    elif label == 5:  # Bus
        color = (0, 149, 255)
    else:
        color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)