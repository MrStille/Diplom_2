import random

import allure
import requests
import os
import sys

sys.path.append(os.getcwd())

from data import Data


class Steps:

    @staticmethod
    @allure.step("Get user info")
    def get_user_info(user_with_access_token):
        headers = {'Authorization': user_with_access_token["access_token"]}
        return requests.get(Data.USER_URL, headers=headers)

    @staticmethod
    @allure.step("Delete user")
    def delete_user(user_with_access_token):
        headers = {'Authorization': user_with_access_token["access_token"]}
        return requests.delete(Data.USER_URL, headers=headers)

    @staticmethod
    @allure.step("Send request to create user")
    def create_user(payload):
        response = requests.post(Data.REGISTER_URL, data=payload)
        return response

    @staticmethod
    @allure.step("Send update user request")
    def patch_user(user_with_access_token, payload):
        headers = {'Authorization': user_with_access_token["access_token"]}
        response = requests.patch(Data.USER_URL, data=payload, headers=headers)
        return response

    @staticmethod
    @allure.step("Login user")
    def login_user(user):
        payload = {
            "email": user["email"],
            "password": user["password"],
        }
        response = requests.post(Data.LOGIN_URL, data=payload)
        return response

    @staticmethod
    @allure.step("Create new order")
    def create_order(user, payload):
        headers = {'Authorization': user["access_token"]}
        response = requests.post(Data.ORDER_URL, data=payload, headers=headers)
        return response

    @staticmethod
    @allure.step("Get all ingredients")
    def get_ingredients():
        response = requests.get(Data.INGREDIENTS_URL)
        return response

    @staticmethod
    @allure.step("Create new random order")
    def create_new_order(new_user, all_ingredients):
        bun = Steps.get_random_ingredient("bun", all_ingredients)
        meat = Steps.get_random_ingredient("main", all_ingredients)
        sauce = Steps.get_random_ingredient("sauce", all_ingredients)
        payload = {
            "ingredients": [bun.get("_id"), sauce.get("_id"), meat.get("_id")],
        }
        response = Steps.create_order(new_user, payload)
        return response

    @staticmethod
    @allure.step("Create new random order")
    def get_orders(user):
        if len(user["access_token"])>0:
            headers = {'Authorization': user["access_token"]}
            response = requests.get(Data.ORDER_URL, headers=headers)
        else:
            response = requests.get(Data.ORDER_URL)

        return response

    @staticmethod
    def get_random_ingredient(i_type, ingredients):
        allure.step(f"Get random ingredient of {i_type}")
        return random.choice(ingredients[i_type])
