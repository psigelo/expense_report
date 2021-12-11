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

        while True:
            c1_min = image_info["rut_area"]["cv_coord1_min"]
            c1_max = image_info["rut_area"]["cv_coord1_max"]
            c2_min = image_info["rut_area"]["cv_coord2_min"]
            c2_max = image_info["rut_area"]["cv_coord2_max"]
            cv2.imshow('img', img[c1_min:c1_max, c2_min:c2_max])
            k = cv2.waitKey(1)
            if k == ord('q'):
                break

        while True:
            c1_min = image_info["name_area"]["cv_coord1_min"]
            c1_max = image_info["name_area"]["cv_coord1_max"]
            c2_min = image_info["name_area"]["cv_coord2_min"]
            c2_max = image_info["name_area"]["cv_coord2_max"]
            cv2.imshow('img', img[c1_min:c1_max, c2_min:c2_max])
            k = cv2.waitKey(1)
            if k == ord('q'):
                break

        while True:
            c1_min = image_info["total_amount"]["cv_coord1_min"]
            c1_max = image_info["total_amount"]["cv_coord1_max"]
            c2_min = image_info["total_amount"]["cv_coord2_min"]
            c2_max = image_info["total_amount"]["cv_coord2_max"]
            cv2.imshow('img', img[c1_min:c1_max, c2_min:c2_max])
            k = cv2.waitKey(1)
            if k == ord('q'):
                break


if __name__ == '__main__':
    json_test_images_crop_areas_g = "./test_receipts_imgs/test_images_crop_areas.json"  # TODO: to argument with this value by default
    see_img_from_test_images(json_test_images_crop_areas_g)
