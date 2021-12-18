import json
import os
import pickle
import random
import string

import tornado.web
import tornado.escape
import socket

from bson import ObjectId
from pymongo import MongoClient

from ai.CRAFT.file_utils import image_suggested_areas
from ai.ai_receipt import get_suggestions_area_receipt, get_data_from_area_receipt
from ai.area_suggestion import AreaSuggestion
from backend_common.user_utils import check_user, insert_new_user

import cv2
import numpy as np


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.render("dashboard.html", name=name)


class LoginHandler(BaseHandler):
    config_data = None

    def get(self):
        self.render("login.html")

    def post(self):
        response = check_user(self.get_argument("name"), self.get_argument("passwd"), self.config_data)
        if response["status"] == "ok":
            self.set_secure_cookie("user", self.get_argument("name"))
            self.set_secure_cookie("hostname", tornado.escape.json_encode(socket.gethostname()))
            self.redirect("/")
        else:
            self.redirect("/login")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.clear_cookie("hostname")
        self.redirect("/")


class RegisterHandler(BaseHandler):
    config_data = None

    def get(self):
        self.render("register.html")

    def post(self):
        response = insert_new_user(self.get_argument("name"), self.get_argument("passwd"), self.config_data)
        if response["status"] == "ok":
            self.redirect("/")
        else:
            self.redirect("/register")


class NewReceiptHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.render("new_receipt.html", name=name)


class BrowserUploadHandler(BaseHandler):
    config_data = None

    @tornado.web.authenticated
    def post(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        file1 = self.request.files['file1'][0]

        img = cv2.imdecode(np.fromstring(file1.body, np.uint8), cv2.IMREAD_COLOR)

        _, poligons = get_suggestions_area_receipt(AreaSuggestion.net, img)

        img_jpg = cv2.imencode('.jpg', img)[1].tobytes()

        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]
        result = table.insert_one({"username": name, "img": img_jpg, "area_suggestions": pickle.dumps(poligons,
                                                                                                      protocol=2)})
        print(result)
        self.redirect(f"/edit_receipt/{str(result.inserted_id)}")


class ListReceiptsHandler(BaseHandler):
    config_data = None
    def get(self):
        # name = tornado.escape.xhtml_escape(self.current_user)
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]
        cursor = table.find()
        receipts = []
        for data in cursor:
            receipts.append(str(data["_id"]))
        self.render("list_receipts.html", receipts=receipts)
        # self.write("fda")

class EditReceiptsHandler(BaseHandler):
    config_data = None

    def get(self, receipt_id):
        # name = tornado.escape.xhtml_escape(self.current_user)
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]
        cursor = table.find()
        self.render("edit_receipt.html", receipt_id=receipt_id)
        # self.write("fda")


class SeeReceiptHandler(BaseHandler):
    config_data = None

    def get(self, receipt_id):
        self.set_header("Content-type", "image/jpg")
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]
        receipt = table.find_one({"_id": ObjectId(receipt_id)})
        img = cv2.imdecode(np.fromstring(receipt["img"], np.uint8), cv2.IMREAD_COLOR)
        polygons = pickle.loads( receipt["area_suggestions"])
        suggested_img = image_suggested_areas(img[:,:,::-1], polygons, verticals=None, texts=None)
        self.write(cv2.imencode('.jpg', suggested_img)[1].tobytes())


class GetPolygonsHandler(BaseHandler):
    config_data = None

    def get(self, receipt_id):
        self.set_header("Content-type", "image/jpg")
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]
        receipt = table.find_one({"_id": ObjectId(receipt_id)})
        polygons = pickle.loads(receipt["area_suggestions"])
        response = []
        for points in polygons:
            x_min = points[:, 0].min()
            x_max = points[:, 0].max()
            y_min = points[:, 1].min()
            y_max = points[:, 1].max()
            response.append({
                "cv_coord1_min": int(y_min),
                "cv_coord1_max": int(y_max),
                "cv_coord2_min": int(x_min),
                "cv_coord2_max": int(x_max),
            })
        self.write(json.dumps(response))


class ExtractAreaInfo(BaseHandler):
    config_data = None

    def get(self, area_name, receipt_id, list_of_polygons_indices):
        polygons_indices = []
        for index in list_of_polygons_indices.split("T"):
            if index != "":
                polygons_indices.append(index)


        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]
        receipt = table.find_one({"_id": ObjectId(receipt_id)})

        img = cv2.imdecode(np.fromstring(receipt["img"], np.uint8), cv2.IMREAD_COLOR)
        polygons = pickle.loads(receipt["area_suggestions"])

        poligonos_cuadrados = []
        for points in polygons:
            x_min = points[:, 0].min()
            x_max = points[:, 0].max()
            y_min = points[:, 1].min()
            y_max = points[:, 1].max()
            poligonos_cuadrados.append({
                "cv_coord1_min": int(y_min),
                "cv_coord1_max": int(y_max),
                "cv_coord2_min": int(x_min),
                "cv_coord2_max": int(x_max),
            })


        # TODO: obtener el mejor ordenamiento posible de los indices.
        extractos = ""
        for it in polygons_indices:
            polygon = poligonos_cuadrados[int(it)]

            img_area = img[polygon["cv_coord1_min"]:polygon["cv_coord1_max"],
                           polygon["cv_coord2_min"]:polygon["cv_coord2_max"]]
            if extractos != "":
                extractos = extractos + " " + get_data_from_area_receipt(img_area)
            else:
                extractos = get_data_from_area_receipt(img_area)

        self.write(json.dumps({"result": extractos}))


class SendAreaInfo(BaseHandler):
    config_data = None

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        area_name = data["name_area"]
        receipt_id = data["receipt_id"]
        text = data["text"]
        # TODO: implement user requirement
        polygons_indices = []
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]
        receipt_oid = ObjectId(receipt_id)
        receipt_dict = table.find_one({"_id": receipt_oid})

        if receipt_dict is None:
            self.write({"error": "receipt id does not exists"})
            return None

        # TODO : check user
        # if receipt_dict["user_id"] != user_id:
        #     self.write({"error": "user does not match"})
        #     return None

        receipt_dict[area_name + "_data"] = text

        table.update_one({'_id': receipt_oid}, {"$set": receipt_dict}, upsert=False)
        self.write({"Status": "image uploaded"})
