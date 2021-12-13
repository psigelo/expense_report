import base64

import cv2
import numpy as np
from ai.CRAFT.try_test import test_net
import ai.CRAFT.imgproc as imgproc
from ai.CRAFT.file_utils import image_suggested_areas
from ai.extract_info.demo import redneuronal, directory_image


def get_data_from_area_receipt(img_area):
    # TODO: LOCK FOR OTHER THREADS
    cv2.imwrite(directory_image + "to_extract.jpg", img_area)
    return redneuronal("to_extract.jpg")


def get_suggestions_area_receipt(net, img):
    # TODO: LOCK FOR OTHER THREADS

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

