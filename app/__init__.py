#coding:utf8
from flask import Flask
from  flask_sqlalchemy import SQLAlchemy


from app.admin import admin as admin_blueprint
from  app.home import  home as home_blue_print


#创建app对象
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URL"]="mysql://root:root@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
app.config['SECRET_KEY']='CTZ'

#实例化SQLAlchemy
db=SQLAlchemy(app)

app=Flask(__name__)
app.debug=True
app.register_blueprint(admin_blueprint,url_prefix="/admin")
app.register_blueprint(home_blue_print)