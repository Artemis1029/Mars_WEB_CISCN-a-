import tornado.web
import yaml
import time
from sqlalchemy.orm.exc import NoResultFound
from sshop.base import BaseHandler
from sshop.models import Commodity, User
from sshop.settings import limit


class ShopIndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.redirect('/login')


class ShopListHandler(BaseHandler):
    def get(self):
        try:
            user = self.orm.query(User).filter(User.username == self.current_user).one()
        except:
            return self.redirect('/login') 
        page = self.get_argument('page', 1)
        page = int(page) if int(page) else 1
        commoditys = self.orm.query(Commodity) \
            .filter(Commodity.amount > 0) \
            .order_by(Commodity.price.desc()) \
            .limit(limit).offset((page - 1) * limit).all()
        return self.render('index.html', commoditys=commoditys, preview=page - 1, next=page + 1, limit=limit)
        


class ShopDetailHandler(BaseHandler):
    def get(self, id=1):
        try:
            user = self.orm.query(User).filter(User.username == self.current_user).one()
        except:
            return self.redirect('/login') 
        try:
            commodity = self.orm.query(Commodity) \
                .filter(Commodity.id == int(id) and Commodity).one()
        except NoResultFound:
            return self.redirect('/')
        return self.render('info.html', commodity=commodity)


class ShopPayHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        try:
            user = self.orm.query(User).filter(User.username == self.current_user).one()
        except:
            return self.redirect('/login') 
        success = "worry"     
        out = "\" \' , curl wget"#os cat tail head nl tac more less rm reboot init poweroff od mk"
        out = out.split(" ")
        try:
            price = self.get_argument('price')
            for i in out: 
                if(i in price):
                    self.render('pay.html', success="worry parmas")      
            price = yaml.load(price)
            success = price
            if(type(price) != dict):
                price_ = float(price)
                things = ""
            else:
                price_ = price.values()[0]
                id = price.keys()[0]
                commodity = self.orm.query(Commodity).filter(Commodity.id == id).one()
                things = commodity.name
                commodity.amount -= 1
            tmp = user.pay(price_)
            if(tmp >= 0):
                user.integral = tmp
            else:
                return self.render('pay.html', danger="your moneny is too less to buy it")
            self.orm.commit()
            return self.render('pay.html', success=things + " cost $" + str(price_))
        except:
            success = yaml.load(price)
            return self.render('pay.html', danger=success)
            


class ShopCarHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        try:
            user = self.orm.query(User).filter(User.username == self.current_user).one()
        except:
            return self.redirect('/login') 
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        if not user.in_shop:
            return self.render('shopcar.html')
        prodects = user.in_shop.split("||")[1:]
        commoditys = []
        price = 0
        for id_ in prodects:
            commodity = self.orm.query(Commodity).filter(Commodity.id == id_).one()
            commoditys.append(commodity)
            price+=float(commodity.price)
            print commodity.price
        return self.render('shopcar.html', commodity=commoditys, price=price)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        try:
            user = self.orm.query(User).filter(User.username == self.current_user).one()
        except:
            return self.redirect('/login') 
        success = "worry"
        try:
            price = self.get_argument('price')
            price = yaml.safe_load(price)
            success = price
            if(type(price) != dict):
                price_ = float(price)
                things = ""
            else:
                price_ = price.values()[0]
                things = price.keys()[0]
            user = self.orm.query(User).filter(User.username == self.current_user).one()
            tmp = user.pay(price_)
            if(tmp >= 0):
                user.integral = tmp
            else:
                return self.render('pay.html', danger="your moneny is too less to buy it")
            user.integral = tmp
            user.in_shop = ""      #clear shop car
            self.orm.commit()
            return self.render('shopcar.html', success=things + " cost $" + str(price_))
        except Exception as ex:
            return self.render('shopcar.html', danger = success)


class ShopCarAddHandler(BaseHandler):
    def post(self, *args, **kwargs):
        try:
            user = self.orm.query(User).filter(User.username == self.current_user).one()
        except:
            return self.redirect('/login') 
        id = self.get_argument('id')
        commodity = self.orm.query(Commodity).filter(Commodity.id == id).one()
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        user.in_shop += "||"
        user.in_shop += id
        commodity.amount -= 1
        self.orm.commit()
        return self.redirect('/shopcar')


class SecKillHandler(BaseHandler):
    def get(self, *args, **kwargs):
        try:
            user = self.orm.query(User).filter(User.username == self.current_user).one()
        except:
            return self.redirect('/login') 
        seckill = self.orm.query(Commodity).filter(Commodity.id == 1).one()
        return self.render('seckill.html', seckill=seckill)

    def post(self, *args, **kwargs):
        try:
            user = self.orm.query(User).filter(User.username == self.current_user).one()
        except:
            return self.redirect('/login') 
        try:
            if time.localtime().tm_min == 0 and time.localtime().tm_sec == 0:
                user.seckill = 1
                # return self.render('seckill.html', danger="seckill will start at x:00", seckill="")
            if user.seckill == 0:
                return self.render('seckill.html', danger="you can not buy it now!",  seckill="")
            user.seckill = 0
            id = self.get_argument('id')
            seckill = self.orm.query(Commodity).filter(Commodity.id == id).one()
            user = self.orm.query(User).filter(User.username == self.current_user).one()
            if seckill.amount == 0:
                 return self.render('seckill.html', danger="you are late!!",  seckill="")
            seckill.amount -= 1
            user.integral -= seckill.price * 0.5
            self.orm.commit()
            return self.render('seckill.html', success="you get it", seckill=seckill)
        except:
            return self.render('seckill.html', danger="something worry",  seckill="")
