import os.path

import cv2
import json
import os


def see_img_from_test_images(json_test_images_crop_areas):
    file = open(json_test_images_crop_areas)
    test_images = json.load(file)
    for image_name, image_info in test_images.items():
        img = cv2.imread(os.path.join("./test_receipts_imgs/", image_name))
        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        while True:
            cv2.imshow('img', img)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break



if __name__ == '__main__':
    json_test_images_crop_areas_g = "./test_receipts_imgs/test_images_crop_areas.json"  # TODO: to argument with this value by default
    see_img_from_test_images( json_test_images_crop_areas_g)
