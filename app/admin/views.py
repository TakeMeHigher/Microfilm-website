#coding:utf8
from . import admin

@admin.route("/")
def index():
    return "<h3 style='color:blue'>this is admin</h3>"