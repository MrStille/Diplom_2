import os
import sys

import allure

sys.path.append(os.getcwd())

from helpers.steps import Steps

sys.path.append(os.getcwd())


@allure.epic('Customers get theirs orders')
class TestGetOrder:
    @allure.title('Get orders of logged in user')
    def test_logged_user_get_orders(self, new_user, all_ingredients):
        order = Steps.create_new_order(new_user, all_ingredients)
        last_orders = Steps.get_orders(new_user)
        assert last_orders.status_code == 200
        assert len(last_orders.json().get('orders')) ==1
        assert order.json()["order"]["number"] == last_orders.json()["orders"][0]["number"]

    @allure.title('Get orders of non-logged in user')
    def test_none_logged_user_get_orders(self, all_ingredients):
        user ={"access_token":""}
        Steps.create_new_order(user, all_ingredients)
        last_orders = Steps.get_orders(user)
        assert last_orders.status_code == 401
        assert last_orders.json()["message"] == "You should be authorised"
