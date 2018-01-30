#coding:utf8
from . import home
from flask import render_template,redirect,url_for,request,session


from .forms import RegForm,LoginForm
from app import models
from  app import db

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

@home.route('/login/',methods=['GET','POST'])
def login():
    '''
    会员登录
    :return:
    '''
    if request.method=='POST':
        form =LoginForm(request.form)
        if form.validate():
            data=form.data
            user=db.session.query(models.User).filter_by(name=data.get('name'),pwd=data.get('pwd')).first()
            if user:
                session['user']=data.get('name')
                user=getUser()
                userlog=models.Userlog(ip=request.remote_addr,user_id=user.id)
                db.session.add(userlog)
                db.session.commit()
                return redirect(url_for('home.index'))
            else:
                msg='密码错误'
                return render_template('home/login.html', form=form,msg=msg)
        return render_template('home/login.html', form=form)
    form=LoginForm()
    return  render_template('home/login.html',form=form)

@home.route('/logout/')
def logout():
    '''
    会员注销
    :return:
    '''
    session['user']=''
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

