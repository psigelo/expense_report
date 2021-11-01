import base64
import numpy as np


def get_data_from_area_receipt(area_name, b64_encoded_roi):
    jpg_original = base64.b64decode(b64_encoded_roi)
    img_npy = np.frombuffer(jpg_original, dtype=np.uint8)

    # TODO: implement AI
    print(area_name, img_npy)

    return "not implemented yet!"
