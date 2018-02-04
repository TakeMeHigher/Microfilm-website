# coding:utf8
import os

from . import home
from flask import render_template, redirect, url_for, request, session
from werkzeug.utils import secure_filename

from .forms import RegForm, LoginForm, UserForm, PwdForm
from app import models
from  app import db
from app.utils.pager import Pagination

BASEDIR = os.path.abspath(os.path.dirname(__file__)).strip('\home')
print(BASEDIR)

file_dir = os.path.join(BASEDIR, 'static', 'avatar')

if not os.path.exists(file_dir):
    os.makedirs(file_dir)


@home.before_request
def check_is_login():
    '''
    检测是否登录了
    :return:
    '''
    if request.path == '/login/':
        return None
    if request.path == '/logout/':
        return None
    if request.path == '/regist/':
        return None
    if request.path=='/':
        return  None
    if session.get('user'):
        return None
    if not session.get('user'):
        return redirect(url_for('home.login'))




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
    previews = db.session.query(models.Preview).all()
    tags=db.session.query(models.Tag).all()
    tid=request.args.get("tid",0)
    star=request.args.get("star",0)
    time=request.args.get("time",0)
    pm=request.args.get("pm",0)
    cm=request.args.get("cm",0)
    p=dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm
    )
    movies=None
    if int(tid)!=0 and int(star)==0:
       movies=db.session.query(models.Movie).filter_by(tag_id=int(tid)).all()
       print(movies,'---------')
    if int(star)!=0 and int(tid)==0:
        movies=db.session.query(models.Movie).filter_by(star=int(star)).all()
    if int(star) != 0 and int(tid) != 0:
        movies = db.session.query(models.Movie).filter_by(star=int(star),tag_id=int(tid)).all()
    if int(tid)==0 and int(star)==0:
        movies=db.session.query(models.Movie).all()
    current_page = request.args.get('page', 1)
    total_count = len(movies)
    base_url = request.path
    parmas = request.args.to_dict()
    pageObj = Pagination(current_page, total_count, base_url, parmas)
    movies = movies[pageObj.start:pageObj.end]

    return render_template('/home/index.html',previews=previews,tags=tags,p=p,movies=movies,pageObj=pageObj)


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
    user=getUser()
    comments=db.session.query(models.Comment).join(models.User).filter(models.Comment.user_id==models.User.id).filter(models.User.id==user.id)
    return render_template('/home/comments.html',comments=comments)


@home.route('/loginlog/')
def loginlog():
    userlogs=db.session.query(models.Userlog).all()
    return render_template('/home/loginlog.html',userlogs=userlogs)


@home.route('/moviecol/')
def moviecol():
    return render_template('/home/moviecol.html')
