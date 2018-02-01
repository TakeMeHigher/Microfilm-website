# coding:utf8
import os

from . import home
from flask import render_template, redirect, url_for, request, session
from werkzeug.utils import secure_filename

from .forms import RegForm, LoginForm, UserForm, PwdForm
from app import models
from  app import db

BASEDIR = os.path.abspath(os.path.dirname(__file__)).strip('\home')
print(BASEDIR)

file_dir = os.path.join(BASEDIR, 'static', 'avatar')

if not os.path.exists(file_dir):
    os.makedirs(file_dir)


def getUser():
    '''
    获取当前登录的会员
    :return:
    '''
    username = session.get('user')
    user = db.session.query(models.User).filter_by(name=username).first()
    return user


@home.route("/")
def index():
    '''
    首页
    :return:
    '''
    return render_template('/home/index.html')


@home.route('/login/', methods=['GET', 'POST'])
def login():
    '''
    会员登录
    :return:
    '''
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            data = form.data
            user = db.session.query(models.User).filter_by(name=data.get('name'), pwd=data.get('pwd')).first()
            if user:
                session['user'] = data.get('name')
                user = getUser()
                userlog = models.Userlog(ip=request.remote_addr, user_id=user.id)
                db.session.add(userlog)
                db.session.commit()
                return redirect(url_for('home.index'))
            else:
                msg = '密码错误'
                return render_template('home/login.html', form=form, msg=msg)
        return render_template('home/login.html', form=form)
    form = LoginForm()
    return render_template('home/login.html', form=form)


@home.route('/logout/')
def logout():
    '''
    会员注销
    :return:
    '''
    session['user'] = ''
    return redirect(url_for('home.login'))


@home.route('/regist/', methods=['GET', 'POST'])
def regist():
    '''
    会员注册
    :return:
    '''
    if request.method == 'POST':
        form = RegForm(request.form)
        if form.validate():
            data = form.data
            user = models.User(
                name=data.get('name'),
                pwd=data.get('pwd'),
                email=data.get('email'),
                phone=data.get('phone')
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home.login'))
        return render_template('/home/register.html', form=form)
    form = RegForm()
    return render_template('/home/register.html', form=form)


@home.route('/user/', methods=['GET', 'POST'])
def user():
    '''
    用户信息展示
    :return:
    '''
    if request.method == 'POST':
        form = UserForm(request.form)
        file = request.files['avatar']
        filename = secure_filename(file.filename)
        file.save(os.path.join(file_dir, filename))
        data = form.data
        avatar = data.get('avatar')
        user = getUser()
        db.session.query(models.User).filter_by(id=user.id).update({
            'name': data.get('name'),
            'pwd': data.get('pwd'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'avatar': data.get(avatar),
            'info': data.get('info')
        })
        db.session.commit()
        return redirect(url_for('home.user'))
    user = getUser()
    form = UserForm(
        data={'name': user.name, 'email': user.email, 'phone': user.phone, 'avatar': user.avatar, 'info': user.info})
    return render_template('/home/user.html', form=form)


@home.route('/changpwd/', methods=['GET', 'POST'])
def changpwd():
    '''
       修改密码
       :return:
       '''
    if request.method == 'POST':
        form = PwdForm(request.form)
        if form.validate():
            oldpwd = form.data.get('oldpwd')
            user = db.session.query(models.User).filter_by(pwd=oldpwd).first()
            if user:
                username = session.get('user')
                db.session.query(models.User).filter_by(name=username).update({'pwd': form.data.get('newpwd')})
                db.session.commit()
                session['user'] = ''
                return redirect(url_for('home.login'))
            else:
                msg = '旧密码输入错误'
                return render_template('/home/changpwd.html', form=form, msg=msg)
        return render_template('/home/changpwd.html', form=form)
    form = PwdForm()
    return render_template('/home/changpwd.html', form=form)


@home.route('/comments/')
def comments():
    return render_template('/home/comments.html')


@home.route('/loginlog/')
def loginlog():
    userlogs=db.session.query(models.Userlog).all()
    return render_template('/home/loginlog.html',userlogs=userlogs)


@home.route('/moviecol/')
def moviecol():
    return render_template('/home/moviecol.html')
