from pymongo import MongoClient


def insert_new_user(user_name: str, password: str, config_data):
    client = MongoClient()
    db = client[config_data["db_name"]]
    table = db["users"]

    if table.find_one({"username": user_name}) is not None:
        return {"status": "error", "error_message": "username was picked"}

    data_row = {"username": user_name, "password": password}
    result_insert = table.insert_one(data_row)
    return {"status": "ok", "user_id": str(result_insert.inserted_id)}


def check_user(user_name, password, config_data):
    client = MongoClient()
    db = client[config_data["db_name"]]
    table = db["users"]

    user = table.find_one({"username": user_name, "password": password})
    if user is None:
        return {"status": "error", "error_message": "user not found"}
    return {"status": "ok", "user_id": str(user["_id"])}
