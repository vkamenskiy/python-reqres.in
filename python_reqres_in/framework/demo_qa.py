
from config import Hosts
from python_reqres_in.utils.base_session import BaseSession


class DemoQaWithEnv:
    def __init__(self, env):
        self.demoqa = BaseSession(url=Hosts(env).demoqa)
        self.reqres = BaseSession(url=Hosts(env).reqres)
        self._authorization_cookie = None

    def login(self, email, password):
        return self.demoqa.post(
            url="/login",
            params={'Email': email, 'Password': password},
            headers={'content-type': "application/x-www-form-urlencoded; charset=UTF-8"},
            allow_redirects=False
        )

    @property
    def authorization_cookie(self):
        return self._authorization_cookie

    @authorization_cookie.setter
    def authorization_cookie(self, response):
        self._authorization_cookie = {"NOPCOMMERCE.AUTH": response.cookies.get("NOPCOMMERCE.AUTH")}

    def add_product_to_cart(self):
        self.demoqa.post(
            "/addproducttocart/details/72/1",
            data={
                "product_attribute_72_5_18": 53,
                "product_attribute_72_6_19": 54,
                "product_attribute_72_3_20": 57,
                "addtocart_72.EnteredQuantity": 1,
            }
        )

    def add_product_to_wishlist(self):
        self.demoqa.post(
            '/addproducttocart/details/43/2',
            data={
                'addtocart_43.EnteredQuantity': 1
            }
        )

    @property
    def session_reqres(self):
        return self.reqres
