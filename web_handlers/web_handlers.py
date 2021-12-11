import tornado.web
import tornado.escape
from backend_common.user_utils import check_user, insert_new_user


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)


class LoginHandler(BaseHandler):
    config_data = None

    def get(self):
        self.render("login.html")

    def post(self):
        response = check_user(self.get_argument("name"), self.get_argument("passwd"), self.config_data)
        if response["status"] == "ok":
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")
        else:
            self.redirect("/login")


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
