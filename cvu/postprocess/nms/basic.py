"""Original Code Taken from https://github.com/rbgirshick/fast-rcnn/blob/master/lib/utils/nms.py

"""
import numpy as np


def nms_np(dets, scores, thresh, max_det):
    '''
    dets is a numpy array : num_dets, 4
    scores ia  nump array : num_dets,
    thresh : iou threshold
    max_det : maximum detections to pick
    '''
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]  # get boxes with more ious first

    keep = []

    while order.size > 0 and len(keep) < max_det:
        # pick maxmum iou box
        i = order[0]
        keep.append(i)

        # get iou
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)  # maximum width
        h = np.maximum(0.0, yy2 - yy1 + 1)  # maxiumum height
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        # drop overlaping boxes
        inds = np.where(ovr <= thresh)[0]
        order = order[inds + 1]

    return np.array(keep)
