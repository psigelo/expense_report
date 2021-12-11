import argparse
import base64
import json
import uuid
from os.path import join, dirname
from typing import Optional, Awaitable

from bson import ObjectId
from pymongo import MongoClient

import tornado.ioloop
import tornado.web
import tornado.escape

from ai.ai_receipt import get_data_from_area_receipt
from backend_common.user_utils import insert_new_user, check_user
from web_handlers.web_handlers import LoginHandler, MainHandler, RegisterHandler, LogoutHandler, NewReceiptHandler, \
    BrowserUploadHandler, TestSeeReceiptHandler


class UploadImageHandler(tornado.web.RequestHandler):
    config_data = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self, user_id: str, receipt_id: str):
        self.write("not implemented")


class UploadImageAreaHandler(tornado.web.RequestHandler):
    config_data = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self, user_id: str, receipt_id: str, area_name: str):
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]

        b64_encoded_receipt = self.request.body
        receipt_oid = ObjectId(receipt_id)
        receipt_dict = table.find_one({"_id": receipt_oid})

        if receipt_dict is None:
            self.write({"error": "receipt id does not exists"})
            return None

        if receipt_dict["user_id"] != user_id:
            self.write({"error": "user does not match"})
            return None

        receipt_dict[area_name] = b64_encoded_receipt

        table.update_one({'_id': receipt_oid}, {"$set": receipt_dict}, upsert=False)
        self.write({"Status": "image uploaded"})


class UserHandler(tornado.web.RequestHandler):
    config_data = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self, user_name: str, password: str):
        response = insert_new_user(user_name, password, self.config_data)
        self.write(response)

    def get(self, user_name: str, password: str):
        response = check_user(user_name, password, self.config_data)
        self.write(response)


class ReceiptHandlerUser(tornado.web.RequestHandler):
    config_data = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self, user_id):
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]

        cursor = table.find({"user_id": user_id})
        response = []
        for it in cursor:
            it["_id"] = str(it["_id"])
            it["comment"] = "to download the images in some columns use the get_receipt specific."
            if "rut" in it.keys():
                it["rut"] = "img bin"
            if "total_amount" in it.keys():
                it["total_amount"] = "img bin"
            if "receipt_number" in it.keys():
                it["receipt_number"] = "img bin"
            if "b64_encoded_receipt" in it.keys():
                it["b64_encoded_receipt"] = "img bin"
            response.append(it)
        self.write(json.dumps(response))


def get_receipt_field(user_id: str, receipt_id: str, specific_field: str, db_name: str):
    client = MongoClient()
    db = client[db_name]
    table = db["receipts_info"]

    receipt_obj = table.find_one({"_id": ObjectId(receipt_id)})
    if receipt_obj is None:
        return {"error": "receipt id not exists"}

    if receipt_obj["user_id"] != user_id:
        return {"error": "user and receipt combination not match"}

    if specific_field == "fields":
        return {"fields": list(receipt_obj.keys())}

    if specific_field not in receipt_obj.keys():
        return {"error": f"field {specific_field} not exists in this receipt, "
                         f"try request with fields as field to get a list of all fields in this receipt"}

    return receipt_obj[specific_field]


class ReceiptHandler(tornado.web.RequestHandler):
    config_data = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self, user_id: str, receipt_id: str, specific_field: str) -> None:
        response = get_receipt_field(user_id, receipt_id, specific_field, self.config_data["db_name"])
        self.write(response)


class CreateReceiptHandler(tornado.web.RequestHandler):
    config_data = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self, user_id):
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]
        result = table.insert_one({"user_id": user_id})
        self.write({"receipt_id": str(result.inserted_id)})


class CalcAreaReceipt(tornado.web.RequestHandler):
    config_data = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self, user_id: str, receipt_id: str, specific_field: str):
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]
        receipt_oid = ObjectId(receipt_id)

        receipt_dict = table.find_one({"_id": receipt_oid})

        if receipt_dict is None:
            self.write({"error": "receipt id does not exists"})
            return None

        if receipt_dict["user_id"] != user_id:
            self.write({"error": "user does not match"})
            return None

        response = get_receipt_field(user_id, receipt_id, specific_field, self.config_data["db_name"])
        if type(response) is dict:
            if "error" in response.keys():
                self.write(response)
        data_from_area = get_data_from_area_receipt(specific_field, response)

        receipt_dict[specific_field + "_data"] = data_from_area

        table.update_one({'_id': receipt_oid}, {"$set": receipt_dict}, upsert=False)
        self.write({"Status": "image uploaded"})


def make_app():
    settings = {
        "template_path": join(dirname(__file__), "templates"),
        "static_path": join(dirname(__file__), "static"),
        "cookie_secret": base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
        "login_url": "/login",
    }

    return tornado.web.Application([
        (r"/upload_image/(\w{1,30})/(\w{1,30})", UploadImageHandler),
        (r"/upload_image_area/(\w{1,30})/(\w{1,30})/(\w{1,30})", UploadImageAreaHandler),
        (r"/create_user/(\w{1,30})/(\w{1,30})", UserHandler),  # TODO: change user manage to one more secure
        (r"/get_user/(\w{1,30})/(\w{1,30})", UserHandler),  # TODO: change user manage to one more secure
        (r"/get_receipts_of_user/(\w{1,30})", ReceiptHandlerUser),
        (r"/get_receipt_field/(\w{1,30})/(\w{1,30})/(\w{1,30})", ReceiptHandler),
        (r"/create_receipt/(\w{1,30})", CreateReceiptHandler),
        (r"/calculate_data_from_area_receipt/(\w{1,30})/(\w{1,30})/(\w{1,30})", CalcAreaReceipt),
        (r"/login", LoginHandler),
        (r"/register", RegisterHandler),
        (r"/logout", LogoutHandler),
        (r"/upload_browser", BrowserUploadHandler),
        (r"/new_receipt", NewReceiptHandler),
        (r"/test_receipt", TestSeeReceiptHandler),
        (r"/", MainHandler),

    ], **settings)


def main(config_file: str):
    """
    :param config_file: path to configuration file
    """

    with open(config_file) as json_data:
        config_data = json.load(json_data)

    UploadImageHandler.config_data = config_data
    UploadImageAreaHandler.config_data = config_data
    UserHandler.config_data = config_data
    CreateReceiptHandler.config_data = config_data
    ReceiptHandlerUser.config_data = config_data
    ReceiptHandler.config_data = config_data
    CalcAreaReceipt.config_data = config_data
    LoginHandler.config_data = config_data
    RegisterHandler.config_data = config_data
    BrowserUploadHandler.config_data = config_data
    TestSeeReceiptHandler.config_data = config_data

    app = make_app()
    app.listen(config_data['port'])
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file', help="path to config file", required=True, type=str)
    cmd_args = parser.parse_args()
    main(cmd_args.config_file)
