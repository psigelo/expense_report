import glob
import json


def check_user_exists(username):
    pass


def create_user(username, password):
    pass


def connect_user(username, password):
    user_id = ""
    return user_id


def create_receipt(user_id):
    pass


def test_accuracy(test_user_name, receipt_images_folder, json_test_images_crop_areas):
    # CHECK IF USER EXISTS, IF EXISTS JUST END WITH ERROR.
    check_user_exists(username=test_user_name)

    # CREATE USER
    password = "testing"
    create_user(test_user_name, password)

    # CONNECT USER
    user_id = connect_user(test_user_name, password)

    # CREATE RECEIPT
    create_receipt(user_id)

    # LOAD RECEIPT IMAGES
    image_files = glob.glob(receipt_images_folder)
    file = open(json_test_images_crop_areas)
    crop_areas_images = json.load(file)

    # TODO usage of AI system


if __name__ == "__main__":
    test_username = "test1234"
    receipt_images_folder_g = "./test_receipts_imgs/*.jpeg"
    json_test_images_crop_areas_g = "./test_receipts_imgs/test_images_crop_areas.json"
    test_accuracy(test_username, receipt_images_folder_g, json_test_images_crop_areas_g)
