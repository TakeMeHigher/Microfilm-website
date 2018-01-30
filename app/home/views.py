#coding:utf8
from . import home
from flask import render_template,redirect,url_for,request


from .forms import RegForm
from app import models
from  app import db

def getUser():
    pass

@home.route("/")
def index():
    return render_template('/home/index.html')

@home.route('/login/')
def login():
    return  render_template('home/login.html')

@home.route('/logout/')
def logout():
    return  redirect(url_for('home.login'))


@home.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method=='POST':
        form =RegForm(request.form)
        if form.validate():
            data=form.data
            user=models.User(
                name=data.get('name'),
                pwd=data.get('pwd'),
                email=data.get('email'),
                phone=data.get('phone')
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home.login'))
        return render_template('/home/register.html', form=form)
    form=RegForm()
    return  render_template('/home/register.html',form=form)


@home.route('/user/')
def user():
    return  render_template('/home/user.html')

@home.route('/changpwd/')
def changpwd():
    return  render_template('/home/changpwd.html')

@home.route('/comments/')
def comments():
    return  render_template('/home/comments.html')

@home.route('/loginlog/')
def loginlog():
    return  render_template('/home/loginlog.html')


@home.route('/moviecol/')
def moviecol():
    return  render_template('/home/moviecol.html')

