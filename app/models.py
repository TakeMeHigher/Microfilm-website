from flask import Flask
from  flask_sqlalchemy import SQLAlchemy
import  datetime

#创建app对象
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URL"]="mysql://root:root@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True

#实例化SQLAlchemy
db=SQLAlchemy(app)


#会员
class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True)#id
    name=db.Column(db.String(100),unique=True)
    pwd=db.Column(db.String(100))
    email=db.Column(db.String(100),unique=True)
    phone=db.Column(db.String(11),unique=True)
    info=db.Column(db.Text)#个人简介个性签名
    face=db.Column(db.String(255),unique=True)#头像
    addtime=db.Column(db.DateTime,index=True,default=datetime.utcnow)#注册时间
    uuid=db.Column(db.String(255),unique=True)#唯一标识符
    userlogs=db.relationship("Userlog",backref="user")#会员日志外键关系


    def __repr__(self):
        return "<User %s>"%self.name

#会员日志
class Userlog(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))#关联的user
    ip=db.Column(db.String(255))
    addtime=db.Column(db.DateTime,index=True,default=datetime.utcnow)#添加日志的时间


    def __repr__(self):
        return "<Userlog %r>"%self.id