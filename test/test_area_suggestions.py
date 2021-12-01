import json
import os
import cv2
from ai.ai_receipt import get_suggestions_area_receipt


def show_img_with_suggestions(img_total, title="imagen con sugerencias"):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    while True:
        cv2.imshow(title, img_total)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
    cv2.destroyAllWindows()


def test_accuracy(json_test_images_crop_areas):
    file = open(json_test_images_crop_areas)
    test_images = json.load(file)

    for image_name, image_info in test_images.items():
        img = cv2.imread(os.path.join("./test_receipts_imgs/", image_name))
        print("to exit press q")
        img_name_with_suggestions = get_suggestions_area_receipt(img)
        show_img_with_suggestions(img_name_with_suggestions)


if __name__ == "__main__":
    json_test_images_crop_areas_g = "./test_receipts_imgs/test_images_crop_areas.json"
    test_accuracy(json_test_images_crop_areas_g)
