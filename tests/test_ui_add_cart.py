from time import sleep

import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser
from selene.support.conditions import have
import allure

LOGIN = "denisgaldin@mail.ru"
PASSWORD = "dr$YTade7Zjs@"
WEB_URL = "https://demowebshop.tricentis.com/"
API_URL = "https://demowebshop.tricentis.com/"


def test_login_with_api():
    with step("Логин с помощью API"):
        result = requests.post(
            url=API_URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
    with step("Получаем cookie через API"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")

    with step("Установили куки с помощью API"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(WEB_URL)

    with step("Проверяем что авторизация прошла"):
        browser.element(".account").should(have.text(LOGIN))

    with step("Добавляем товар в корзину"):
        requests.post(url="https://demowebshop.tricentis.com/addproducttocart/catalog/31/1/1")
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})

    with step("Проверяем что товар добавлен в корзину"):
        browser.open("https://demowebshop.tricentis.com/cart")
        browser.element(".product-name").should(have.text("Build your own computer"))
