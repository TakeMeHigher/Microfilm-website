#coding:utf8
import os
import uuid
import datetime

from flask import render_template,redirect,url_for,request,session,flash
from werkzeug.utils import secure_filename

import app
from . import admin
from  app.admin.forms import LoginForm,MovieForm,TagForm,PwdForm
from  app.models import Admin
from app import models
from  app import db
from  app.utils.pager import Pagination

up_url=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static/uploads/')
@admin.before_request
def check_is_login():
    '''
    检测是否登录了
    :return:
    '''
    if request.path=='/admin/login':
        return None
    if not session.get('admin'):
        return redirect(url_for('admin.login'))

def changeFilename(filename):
    '''
    获取上传文件的名称
    :param filename:
    :return:
    '''
    fileinfo=os.path.splitext(filename)
    filename=datetime.datetime.now().strftime('%Y%m%d%H%M%S')+str(uuid.uuid4().hex)+fileinfo[-1]
    return filename

@admin.route("/")
def index():
    '''
    首页
    :return:
    '''
    return render_template('admin/index.html')


@admin.route("/login",methods=['GET','POST'])
def login():
    '''
    登录
    :return:
    '''
    if request.method=='GET':
        form=LoginForm()
        return render_template('admin/login.html',form=form)
    else:
        form=LoginForm(request.form)
        if form.validate():
            data=form.data
            #pwd=Admin.query(Admin.pwd).filter_by(name=data.get('account'))
            pwd=db.session.query(Admin.pwd).filter_by(name=data.get('account')).first()
            print(pwd[0],'-----')
            if pwd[0] !=data.get('pwd'):
                flash('密码错误')
                return redirect(url_for('admin.login'))
            session['admin']=data.get('account')
            return redirect(url_for('admin.index'))
        return render_template('admin/login.html', form=form)


@admin.route("/logout")
def logout():
    '''
    注销
    :return:
    '''
    session['admin']=''
    return redirect(url_for('admin.login'))


@admin.route("/changepwd")
def changepwd():
    '''
    修改密码
    :return:
    '''
    form=PwdForm()
    return render_template('admin/changepwd.html',form=form)


@admin.route("/addtag",methods=['GET','POST'])
def addtag():
    '''
    添加标签
    :return:
    '''
    if request.method=='POST':
        form=TagForm(request.form)
        tag=models.Tag(
            name=form.data.get('name')
        )
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('admin.taglist'))
    form=TagForm()
    return render_template('admin/tag_add.html',form=form)

@admin.route("/taglist")
def taglist():
    '''
    标签列表
    :return:
    '''
    tags=db.session.query(models.Tag).all()
    return render_template('admin/tag_list.html',tags=tags)

@admin.route('/edittag/<int:id>',methods=['GET','POST'])
def edittag(id):
    '''
    编辑标签
    :param id:
    :return:
    '''
    if request.method=='POST':
        form=TagForm(request.form)
        db.session.query(models.Tag).filter_by(id=id).update({'name':form.data.get('name')})
        db.session.commit()
        return redirect(url_for('admin.taglist'))
    tag=db.session.query(models.Tag).filter_by(id=id).first()
    form=TagForm(data={'name':tag.name})
    return render_template('admin/tag_add.html',form=form)

@admin.route('/deltag/<int:id>')
def deltag(id):
    '''
    删除标签
    :param id:
    :return:
    '''
    db.session.query(models.Tag).filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('admin.taglist'))


@admin.route("/addmovie",methods=['GET','POST'])
def addmovie():
    '''
    添加电影
    :return:
    '''
    if request.method=='POST':
        form =MovieForm(request.form)
        if form.validate():
            data =form.data

            file_url=secure_filename(form.url.data)
            file_logo=secure_filename(form.logo.data)

            if not os.path.exists(up_url):
                os.makedirs(up_url)
                os.chmod(up_url,'rw')
            url=changeFilename(file_url)
            logo=changeFilename(file_logo)
            movie=models.Movie(
                title=data.get('title'),
                url=url,
                info=data.get('info'),
                logo=logo,
                star=int(data.get('star')),
                playnum=0,
                ommentnum=0,
                tag_id=int(data.get('tag')),
                area=data.get('area'),
                release_time=data.get('release_time'),
                length=data.get('length'),

            )
            db.session.add(movie)
            db.session.commit()
            flash('添加电影成功','ok')
            return redirect(url_for('admin.movielist'))


        return render_template('admin/movie_add.html', form=form)
    form=MovieForm()
    return render_template('admin/movie_add.html',form=form)


@admin.route("/movielist")
def movielist():
    '''
    电影列表
    :return:
    '''
    movielist=db.session.query(models.Movie).all()
    tag_names={}
    for movie in movielist:
        tag_name=db.session.query(models.Tag.name).filter_by(id=movie.tag_id).first()
        tag_names[movie.id]=tag_name[0]
    return render_template('admin/movie_list.html',movielist=movielist,tag_names=tag_names)

@admin.route('/editmovie/<int:id>',methods=['GET','POST'])
def editmovie(id):
    '''
    修改电影
    :param id:
    :return:
    '''
    if request.method=='POST':
        form =MovieForm(request.form)
        if form.validate():
            data=form.data
            db.session.query(models.Movie).filter_by(id=id).update({
            'title':data.get('title'),
            'url':data.get('url'),
            'info':data.get('info'),
            'logo':data.get('logo'),
            'star':int(data.get('star')),
            'playnum':0,
            'ommentnum':0,
            'tag_id':int(data.get('tag')),
            'area':data.get('area'),
            'release_time':data.get('release_time'),
            'length':data.get('length')})

            db.session.commit()
            return redirect(url_for('admin.movielist'))

    movie = db.session.query(models.Movie).filter_by(id=id).first()
    movie_dic={
        'title':movie.title,
        'url':movie.url,
        'info':movie.info,
        'logo':movie.logo,
        'star':movie.star,
        'playnum':movie.playnum,
        'ommentnum':movie.ommentnum,
        'tag_id':movie.tag_id,
        'area':movie.area,
        'release_time':movie.release_time,
        'length':movie.length
    }
    form=MovieForm(data=movie_dic)
    return render_template('admin/movie_add.html', form=form)

@admin.route('/delmovie/<int:id>')
def delmovie(id):
    '''
    删除电影
    :param id:
    :return:
    '''
    db.session.query(models.Movie).filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('admin.movielist'))

@admin.route("/previewadd")
def previewadd():
    return render_template('admin/preview_add.html')


@admin.route("/previewlist")
def previewlist():
    return render_template('admin/preview_list.html')



@admin.route("/userlist")
def userlist():
    '''
    会员列表
    :return:
    '''
    users=db.session.query(models.User).all()

    current_page = request.args.get('page', 1)
    total_count = len(users)
    base_url = request.path
    parmas = request.args.to_dict()
    pageObj=Pagination(current_page,total_count,base_url,parmas)
    users=users[pageObj.start:pageObj.end]
    return render_template('admin/user_list.html',users=users,pageObj=pageObj)


@admin.route("/userview/<int:id>")
def userview(id):
    '''
    会员详细界面
    :return:
    '''
    user=db.session.query(models.User).filter_by(id=id).first()
    return render_template('admin/user_view.html',user=user)


@admin.route("/commentlist")
def commentlist():
    '''
    评论列表管理
    :return:
    '''
    comments=db.session.query(models.Comment).join(models.User).join(
        models.Movie).filter(models.Comment.user_id==models.User.id).filter(
        models.Comment.movie_id==models.Movie.id
    ).all()
    print(len(comments))
    return render_template('admin/comment_list.html',comments=comments)
@admin.route('/delcomment/<int:id>')
def delcomment(id):
    '''
    删除评论
    :param id:
    :return:
    '''
    db.session.query(models.Comment).filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('admin.commentlist'))

@admin.route("/moviecol_list")
def moviecol_list():
    '''
    电影收藏列表
    :return:
    '''

    moviecols=db.session.query(models.MovieCol).join(models.User).join(models.Movie).filter(
        models.MovieCol.movie_id==models.Movie.id
    ).filter(models.MovieCol.user_id==models.User.id).order_by(models.MovieCol.addtime.desc())
    return render_template('admin/moviecol_list.html',moviecols=moviecols)

@admin.route('/delmoviecol/<int:id>')
def delmoviecol(id):
    '''
    删除电影收藏
    :param id:
    :return:
    '''
    db.session.query(models.MovieCol).filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('admin.moviecol_list'))



@admin.route('/oplog_list')
def oplog_list():
    return render_template('admin/oplog_list.html')


@admin.route('/adminloginlog_list')
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')

@admin.route('/userloginlog_list')
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')

@admin.route('/admin_add')
def admin_add():
    return render_template('admin/admin_add.html')


@admin.route('/admin_list')
def admin_list():
    return render_template('admin/admin_list.html')