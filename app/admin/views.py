#coding:utf8
from flask import render_template,redirect,url_for
from . import admin

@admin.route("/")
def index():
    return render_template('admin/index.html')


@admin.route("/login")
def login():
    return render_template('admin/login.html')

@admin.route("/logout")
def logout():
    return redirect(url_for('admin.login'))


@admin.route("/changepwd")
def changepwd():
    return render_template('admin/changepwd.html')


@admin.route("/addtag")
def addtag():
    return render_template('admin/tag_add.html')

@admin.route("/taglist")
def taglist():
    return render_template('admin/tag_list.html')


@admin.route("/addmovie")
def addmovie():
    return render_template('admin/movie_add.html')


@admin.route("/movielist")
def movielist():
    return render_template('admin/movie_list.html')



@admin.route("/previewadd")
def previewadd():
    return render_template('admin/preview_add.html')


@admin.route("/previewlist")
def previewlist():
    return render_template('admin/preview_list.html')



@admin.route("/userlist")
def userlist():
    return render_template('admin/user_list.html')


@admin.route("/userview")
def userview():
    return render_template('admin/user_view.html')