import argparse
import os
import time
import numpy as np
import cv2
import json

points = []


def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if len(points) < 4:
            points.append((x, y))


def add_new_receipt_image_to_test(img_filepath, json_test_images_crop_areas):
    # TODO: la mayor parte del codigo esta repetido 4 veces, pasarlo a funcion!
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    data_to_insert = dict()

    file = open(json_test_images_crop_areas)
    crop_areas_images = json.load(file)
    file.close()

    img = cv2.imread(img_filepath)
    print("select 4 points for rut area")
    print("to start again press r")
    print("to quit again press q")
    print("to accept ")
    exit_program = False
    global points
    while True:
        time.sleep(0.1)  # to prevent overload of cpu
        draw_image = img.copy()
        if len(points) >= 4:
            data = np.array(points)
            x_min = data[:, 0].min()
            x_max = data[:, 0].max()
            y_min = data[:, 1].min()
            y_max = data[:, 1].max()
            cv2.imshow('img', img[y_min:y_max, x_min:x_max])
            k = cv2.waitKey(1)
            if k == ord('q'):
                exit_program = True
                break
            elif k == ord('r'):
                points = []

            elif k == ord('c'):
                break
        else:
            for point in points:
                cv2.circle(draw_image, (point[0], point[1]), 2, (0, 255, 0), -1)
            cv2.imshow('img', draw_image)
            cv2.setMouseCallback('img', draw_circle)
            k = cv2.waitKey(1)
            if k == ord('q'):
                exit_program = True
                break

            elif k == ord('r'):
                points = []

    if exit_program:
        cv2.destroyAllWindows()
        exit(1)

    data = np.array(points)
    x_min = data[:, 0].min()
    x_max = data[:, 0].max()
    y_min = data[:, 1].min()
    y_max = data[:, 1].max()

    data_to_insert["rut_area"] = {
        "cv_coord1_min": int(y_min),
        "cv_coord1_max": int(y_max),
        "cv_coord2_min": int(x_min),
        "cv_coord2_max": int(x_max),
    }

    points = []
    print("select 4 points for name")
    print("to start again press r")
    print("to quit again press q")
    print("to accept ")

    while True:
        time.sleep(0.1)  # to prevent overload of cpu
        draw_image = img.copy()
        if len(points) >= 4:
            data = np.array(points)
            x_min = data[:, 0].min()
            x_max = data[:, 0].max()
            y_min = data[:, 1].min()
            y_max = data[:, 1].max()
            cv2.imshow('img', img[y_min:y_max, x_min:x_max])
            k = cv2.waitKey(1)
            if k == ord('q'):
                exit_program = True
                break
            elif k == ord('r'):
                points = []

            elif k == ord('c'):
                break
        else:
            for point in points:
                cv2.circle(draw_image, (point[0], point[1]), 2, (0, 255, 0), -1)
            cv2.imshow('img', draw_image)
            cv2.setMouseCallback('img', draw_circle)
            k = cv2.waitKey(1)
            if k == ord('q'):
                exit_program = True
                break

            if k == ord('r'):
                points = []

    if exit_program:
        cv2.destroyAllWindows()
        exit(1)

    data = np.array(points)
    x_min = data[:, 0].min()
    x_max = data[:, 0].max()
    y_min = data[:, 1].min()
    y_max = data[:, 1].max()

    data_to_insert["name_area"] = {
        "cv_coord1_min": int(y_min),
        "cv_coord1_max": int(y_max),
        "cv_coord2_min": int(x_min),
        "cv_coord2_max": int(x_max),
    }

    points = []
    print("select 4 points for total amount")
    print("to start again press r")
    print("to quit again press q")
    print("to accept ")

    while True:
        time.sleep(0.1)  # to prevent overload of cpu
        draw_image = img.copy()
        if len(points) >= 4:
            data = np.array(points)
            x_min = data[:, 0].min()
            x_max = data[:, 0].max()
            y_min = data[:, 1].min()
            y_max = data[:, 1].max()
            cv2.imshow('img', img[y_min:y_max, x_min:x_max])
            k = cv2.waitKey(1)
            if k == ord('q'):
                exit_program = True
                break
            elif k == ord('r'):
                points = []

            elif k == ord('c'):
                break
        else:
            for point in points:
                cv2.circle(draw_image, (point[0], point[1]), 2, (0, 255, 0), -1)
            cv2.imshow('img', draw_image)
            cv2.setMouseCallback('img', draw_circle)
            k = cv2.waitKey(1)
            if k == ord('q'):
                exit_program = True
                break

            if k == ord('r'):
                points = []

    if exit_program:
        cv2.destroyAllWindows()
        exit(1)

    data = np.array(points)
    x_min = data[:, 0].min()
    x_max = data[:, 0].max()
    y_min = data[:, 1].min()
    y_max = data[:, 1].max()

    data_to_insert["total_amount"] = {
        "cv_coord1_min": int(y_min),
        "cv_coord1_max": int(y_max),
        "cv_coord2_min": int(x_min),
        "cv_coord2_max": int(x_max),
    }

    crop_areas_images[os.path.basename(img_filepath)] = data_to_insert
    out_file = open(json_test_images_crop_areas, "w")
    json.dump(crop_areas_images, out_file)
    out_file.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--img", help="image file path", required=True, type=str)
    cmd_args = parser.parse_args()
    img_filepath_g = cmd_args.img

    json_test_images_crop_areas_g = "./test_receipts_imgs/test_images_crop_areas.json"
    add_new_receipt_image_to_test(img_filepath_g, json_test_images_crop_areas_g)
