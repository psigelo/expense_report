import os
import random
import string

import tornado.web
import tornado.escape
import socket

from bson import ObjectId
from pymongo import MongoClient

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
        img_jpg = cv2.imencode('.jpg', img)[1].tobytes()

        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]
        result = table.insert_one({"username": name, "img": img_jpg})
        print(result)
        self.redirect("/")  # TODO: redirect to edit this receipt directly when that endpoint exists


class TestSeeReceiptHandler(BaseHandler):
    config_data = None

    def get(self):
        self.set_header("Content-type", "image/jpg")
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]
        receipt = table.find_one()
        # img = cv2.imdecode(np.fromstring(receipt["img"], np.uint8), cv2.IMREAD_COLOR)
        self.write(receipt["img"])
