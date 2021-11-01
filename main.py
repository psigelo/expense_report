import argparse
import json
from json import JSONDecodeError
from typing import Optional, Awaitable

from bson import ObjectId
from pymongo import MongoClient

import tornado.ioloop
import tornado.web
import tornado.escape
import base64
import numpy as np


class UploadImageHandler(tornado.web.RequestHandler):
    config_data = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self, user_id: str, receipt_id: str):
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]

        b64_encoded_receipt = self.request.body
        # jpg_original = base64.b64decode(b64_encoded_receipt)
        # img_npy = np.frombuffer(jpg_original, dtype=np.uint8)
        receipt_oid = ObjectId(receipt_id)
        receipt_dict = table.find_one({"_id": receipt_oid})
        if receipt_dict is None:
            self.write({"error": "receipt id does not exists"})
            return None

        if receipt_dict["user_id"] != user_id:
            self.write({"error": "user does not match"})
            return None

        receipt_dict["b64_encoded_receipt"] = b64_encoded_receipt
        table.update_one({'_id': receipt_oid}, {"$set": receipt_dict}, upsert=False)
        self.write({"Status": "image uploaded"})


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
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["users"]

        if table.find_one({"username": user_name}) is not None:
            self.write({"error": "username was picked"})
            return None

        data_row = {"username": user_name, "password": password}
        result_insert = table.insert_one(data_row)
        self.write({"user_id": str(result_insert.inserted_id)})

    def get(self, user_name: str, password: str):
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["users"]

        user = table.find_one({"username": user_name, "password": password})
        if user is None:
            self.write({"error": "user not found"})
            return None
        self.write({"user_id": str(user["_id"])})


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


class ReceiptHandler(tornado.web.RequestHandler):
    config_data = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self, user_id: str, receipt_id: str, specific_field: str) -> None:
        print("dfa")
        client = MongoClient()
        db = client[self.config_data["db_name"]]
        table = db["receipts_info"]

        receipt_obj = table.find_one({"_id": ObjectId(receipt_id)})
        if receipt_obj is None:
            self.write({"error": "receipt id not exists"})
            return None

        if receipt_obj["user_id"] != user_id:
            self.write({"error": "user and receipt combination not match"})
            return None

        if specific_field == "fields":
            self.write({"fields": list(receipt_obj.keys())})
            return None

        if specific_field not in receipt_obj.keys():
            self.write({"error": f"field {specific_field} not exists in this receipt, try request with fields as field to get a list of all fields in this receipt"})
            return None

        self.write(receipt_obj[specific_field])


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


def make_app():
    return tornado.web.Application([
        (r"/upload_image/(\w{1,30})/(\w{1,30})", UploadImageHandler),
        (r"/upload_image_area/(\w{1,30})/(\w{1,30})/(\w{1,30})", UploadImageAreaHandler),
        (r"/create_user/(\w{1,30})/(\w{1,30})", UserHandler),  # TODO: change user manage to one more secure
        (r"/get_user/(\w{1,30})/(\w{1,30})", UserHandler),  # TODO: change user manage to one more secure
        (r"/get_receipts_of_user/(\w{1,30})", ReceiptHandlerUser),
        (r"/get_receipt_field/(\w{1,30})/(\w{1,30})/(\w{1,30})", ReceiptHandler),
        (r"/create_receipt/(\w{1,30})", CreateReceiptHandler),
    ])


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


    app = make_app()
    app.listen(config_data['port'])
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file', help="path to config file", required=True, type=str)
    cmd_args = parser.parse_args()
    main(cmd_args.config_file)
