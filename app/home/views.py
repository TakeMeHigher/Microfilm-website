#coding:utf8
from . import home

@home.route("/")
def home():
    return "<h3 style='color:green'>this is home</h3>"