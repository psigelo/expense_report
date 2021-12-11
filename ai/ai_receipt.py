import base64
import numpy as np
from ai.CRAFT.try_test import test_net
import ai.CRAFT.imgproc as imgproc
from ai.CRAFT.file_utils import image_suggested_areas


# class CnnHandler():
#     cnn =


def get_data_from_area_receipt(net, img_area):

    return "not implemented yet!"


def get_data_from_area_receipt_b64(net, b64_encoded_roi):
    jpg_original = base64.b64decode(b64_encoded_roi)
    img_npy = np.frombuffer(jpg_original, dtype=np.uint8)

    return get_data_from_area_receipt(net, img_npy)


def get_suggestions_area_receipt(net, img):
    """

    :param net: pre trained model
    :param img: image to analyze
    :return: suggested_img: image with borders in text
    :return: polys: polygons of recognize text
    :return: bboxes: polygons of recognize text. Is almost the same with polys
    """
    bboxes, polys, score_text = test_net(net,
                                         img,
                                         text_threshold=0.7,
                                         link_threshold=0.4,
                                         low_text=0.4,
                                         cuda=False,
                                         poly=False,
                                         refine_net=None)

    suggested_img = image_suggested_areas(img[:,:,::-1], polys, verticals=None, texts=None)

    return suggested_img, polys

