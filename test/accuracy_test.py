import json
import os
import cv2
from ai.ai_receipt import get_data_from_area_receipt


def get_name_image(img, area, image_info):
    c1_min = image_info[area]["cv_coord1_min"]
    c1_max = image_info[area]["cv_coord1_max"]
    c2_min = image_info[area]["cv_coord2_min"]
    c2_max = image_info[area]["cv_coord2_max"]
    return img[c1_min:c1_max, c2_min:c2_max]


def show_img(result_text: str, img_total):
    cv2.namedWindow(result_text, cv2.WINDOW_NORMAL)
    while True:
        cv2.imshow(result_text, img_total)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
    cv2.destroyAllWindows()


def test_accuracy( json_test_images_crop_areas):
    file = open(json_test_images_crop_areas)
    test_images = json.load(file)

    for image_name, image_info in test_images.items():
        img = cv2.imread(os.path.join("./test_receipts_imgs/", image_name))
        img_name = get_name_image(img, "name_area", image_info)
        img_rut = get_name_image(img, "rut_area", image_info)
        img_total = get_name_image(img, "total_amount", image_info)

        print("see title to view the AI result")

        result_name = get_data_from_area_receipt(img_name)
        show_img(result_name, img_name)

        result_rut = get_data_from_area_receipt(img_rut)
        show_img(result_rut, img_rut)

        result_total = get_data_from_area_receipt(img_total)
        show_img(result_total, img_total)


if __name__ == "__main__":
    json_test_images_crop_areas_g = "./test_receipts_imgs/test_images_crop_areas.json"
    test_accuracy(json_test_images_crop_areas_g)
