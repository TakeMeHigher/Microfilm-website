#coding:utf8
from . import admin

@admin.route("/")
def home():
    return "<h3 style='color:blue'>this is admin</h3>"