import argparse
import json
from json import JSONDecodeError
from typing import Optional, Awaitable

from bson import ObjectId
from pymongo import MongoClient

import tornado.ioloop
import tornado.web
import tornado.escape


class UploadImageHandler(tornado.web.RequestHandler):
    config_data = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self, user_id: int):
        self.write({"test": "to implement"})


class UploadImageAreaHandler(tornado.web.RequestHandler):
    config_data = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self, user_id: int):
        data = {}
        try:
            if len(self.request.body) != 0:
                data = tornado.escape.json_decode(self.request.body)

        except JSONDecodeError as e:
            self.write({"error": "BAD json format in body"})
            return None
        self.write({"test": "to implement"})


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


class ReceiptHandler(tornado.web.RequestHandler):
    config_data = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get_all_receipts_from_user(self, user_id, data):
        self.write({"test": "to implement"})

    def get_receipt(self, receipt_id, data):
        self.write({"test": "to implement"})

    def post(self):
        self.write({"test": "to implement"})

    def get(self, id_wildcard):
        data = {}
        try:
            if len(self.request.body) != 0:
                data = tornado.escape.json_decode(self.request.body)

        except JSONDecodeError as e:
            self.write({"error": "BAD json format in body"})
            return None

        if isinstance(id_wildcard, str):
            self.get_all_receipts_from_user(id_wildcard, data)
        else:
            self.get_receipt(id_wildcard, data)


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
        (r"/upload_image/(\d{0,10})", UploadImageHandler),
        (r"/upload_image_area/(\d{0,10})/(\d{0,10})/(\w{1,30})", UploadImageAreaHandler),
        (r"/create_user/(\w{1,30})/(\w{1,30})", UserHandler),  # TODO: change user manage to one more secure
        (r"/get_user/(\w{1,30})/(\w{1,30})", UserHandler),  # TODO: change user manage to one more secure
        (r"/get_receipts_of_user/(\w{1,30})", ReceiptHandler),
        (r"/get_receipt/(\d{0,10})", ReceiptHandler),
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

    app = make_app()
    app.listen(config_data['port'])
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file', help="path to config file", required=True, type=str)
    cmd_args = parser.parse_args()
    main(cmd_args.config_file)
