import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from sshop.base import BaseHandler
from sshop.models import User
import bcrypt


class UserLoginHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        return self.render('login.html', ques=self.application.question, uuid=self.application.uuid)

    def post(self):
        if not self.check_captcha():
            return self.render('login.html', danger="captcha is not right", ques=self.application.question, uuid=self.application.uuid)
        username = self.get_argument('username')
        password = self.get_argument('password')
        if username and password:
            try:
                user = self.orm.query(User).filter(User.username == username).one()
            except NoResultFound:
                return self.render('login.html', danger="user is not exist", ques=self.application.question, uuid=self.application.uuid)
            if user.check(password):
                self.set_secure_cookie('username', user.username)
                user.cookies = self.get_cookie('username')
                self.orm.commit()
                self.redirect('/user')
            else:
                return self.render('login.html', danger='password is worry', ques=self.application.question, uuid=self.application.uuid)


class RegisterHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        return self.render('register.html', ques=self.application.question, uuid=self.application.uuid)

    def post(self, *args, **kwargs):
        if not self.check_captcha():
            return self.render('register.html', danger="captcha is not right", ques=self.application.question, uuid=self.application.uuid)
        username = self.get_argument('username')
        mail = self.get_argument('mail')
        password = self.get_argument('password')
        password_confirm = self.get_argument('password_confirm')
        invite_user = self.get_argument('invite_user')

        if password != password_confirm:
            return self.render('register.html', danger="check your password", ques=self.application.question, uuid=self.application.uuid)
        if mail and username and password:
            try:
                user = self.orm.query(User).filter(User.username == username).one()
            except NoResultFound:
                self.orm.add(User(username=username, mail=mail,
                                  password=bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()), in_shop=""))
                self.orm.commit()
                try:
                    inviteUser = self.orm.query(User).filter(User.username == invite_user).one()
                    inviteUser.integral += 10
                    self.orm.commit()
                except NoResultFound:
                    pass
                self.redirect('/login')
        else:
            return self.render('register.html', danger="parmas worry", ques=self.application.question, uuid=self.application.uuid)


class ResetPasswordHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        return self.render('reset.html', ques=self.application.question, uuid=self.application.uuid)

    def post(self, *args, **kwargs):
        if not self.check_captcha():
            return self.render('reset.html', danger="captcha is not right", ques=self.application.question, uuid=self.application.uuid)
        return self.redirect('/login')


class changePasswordHandler(BaseHandler):
    def get(self):
        try:
            user = self.orm.query(User).filter(User.username == self.current_user).one()
        except:
            return self.redirect('/login') 
        return self.render('change.html')

    def post(self, *args, **kwargs):
        old_password = self.get_argument('old_password')
        password = self.get_argument('password')
        password_confirm = self.get_argument('password_confirm')
        print old_password, password, password_confirm
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        if password == password_confirm:
            if user.check(old_password):
                user.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
                self.orm.commit()
                #return self.render('change.html', danger="change failed")
                return self.render('shopcar.html', success="change success")
        return self.render('change.html', danger="change failed")


class UserInfoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        try:
            user = self.orm.query(User).filter(User.username == self.current_user).one()
        except:
            return self.redirect('/login') 
        return self.render('user.html', user=user)


class UserLogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.clear_cookie('username')
        try:
            user = self.orm.query(User).filter(User.username == self.current_user).one()
        except:
            return self.redirect('/login') 
        user.cookies = 0
        self.orm.commit()
        self.redirect('/login')
