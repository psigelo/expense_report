import base64
import numpy as np


def get_data_from_area_receipt(img_area):
    return "not implemented yet!"


def get_data_from_area_receipt_b64(b64_encoded_roi):
    jpg_original = base64.b64decode(b64_encoded_roi)
    img_npy = np.frombuffer(jpg_original, dtype=np.uint8)

    return get_data_from_area_receipt(img_npy)
