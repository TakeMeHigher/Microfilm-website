#coding:utf8
from flask import Flask
from  flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
from app.admin import admin as admin_blueprint
from  app.home import  home as home_blue_print
import  settings


#创建app对象

app=Flask(__name__)
app.config.from_object('settings.BaseConfig')
app.debug=True
app.register_blueprint(admin_blueprint,url_prefix="/admin")
app.register_blueprint(home_blue_print)


#实例化SQLAlchemy

db.init_app(app)

