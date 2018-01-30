# coding:utf8
import os
import uuid
import datetime

from flask import render_template, redirect, url_for, request, session, flash
from werkzeug.utils import secure_filename

import app
from . import admin
from  app.admin.forms import LoginForm, MovieForm, TagForm, PwdForm,AuthForm,RoleForm,AdminForm
from  app.models import Admin
from app import models
from  app import db
from  app.utils.pager import Pagination

up_url = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/')


def getAdmin():
    '''
    获取当前登录的Admin对象
    :return:
    '''
    username = session.get('admin')
    admin = db.session.query(models.Admin).filter_by(name=username).first()
    return admin


def getOplog(ip, admin_id, reason):
    '''
    添加操作日志
    :param ip:
    :param admin_id:
    :param reasone:
    :return:
    '''
    oplog = models.Oplog(ip=ip, admin_id=admin_id, reason=reason)
    db.session.add(oplog)
    db.session.commit()


@admin.before_request
def check_is_login():
    '''
    检测是否登录了
    :return:
    '''
    if request.path == '/admin/login':
        return None
    if not session.get('admin'):
        return redirect(url_for('admin.login'))

    admin=db.session.query(models.Admin).filter_by(name=session.get('admin')).first()

    role=db.session.query(models.Role).filter_by(id=admin.role_id).first()

    if '-' in role.auths:
        auths=list(map(lambda x:int(x),role.auths.split('-')))
    else:
        auths=role.auths
    urls=[]
    for id in auths:
        url=db.session.query(models.Auth.url).filter_by(id=id).first()
        urls.append(url[0])

    print(request.url_rule,type(request.url_rule))
    print(request.path)
    print(urls)
    print(str(request.url_rule) in urls)
    if str(request.url_rule) not in urls:
        return '无权访问'






def changeFilename(filename):
    '''
    修改上传文件的名称
    :param filename:
    :return:
    '''
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admin.route("/index")
def index():
    '''
    首页
    :return:
    '''
    return render_template('admin/index.html')


@admin.route("/login", methods=['GET', 'POST'])
def login():
    '''
    登录
    :return:
    '''
    if request.method == 'GET':
        form = LoginForm()
        return render_template('admin/login.html', form=form)
    else:
        form = LoginForm(request.form)
        if form.validate():
            data = form.data
            # pwd=Admin.query(Admin.pwd).filter_by(name=data.get('account'))
            pwd = db.session.query(Admin.pwd).filter_by(name=data.get('account')).first()
            print(pwd[0], '-----')
            if pwd[0] != data.get('pwd'):
                flash('密码错误')
                return redirect(url_for('admin.login'))
            session['admin'] = data.get('account')
            admin = getAdmin()
            adminlog = models.Adminlog(ip=request.remote_addr, admin_id=admin.id)
            db.session.add(adminlog)
            db.session.commit()
            return redirect(url_for('admin.index'))
        return render_template('admin/login.html', form=form)


@admin.route("/logout")
def logout():
    '''
    注销
    :return:
    '''
    session['admin'] = ''
    return redirect(url_for('admin.login'))


@admin.route("/changepwd", methods=['GET', 'POST'])
def changepwd():
    '''
    修改密码
    :return:
    '''
    if request.method == 'POST':
        form = PwdForm(request.form)
        if form.validate():
            oldpwd = form.data.get('oldpwd')
            admin = db.session.query(models.Admin).filter_by(pwd=oldpwd).first()
            if admin:
                username = session.get('admin')
                db.session.query(models.Admin).filter_by(name=username).update({'pwd': form.data.get('newpwd')})
                getOplog(ip=request.remote_addr, admin_id=admin.id, reason='%s修改了密码' % admin.name)
                db.session.commit()
                session['admin'] = ''
                return redirect(url_for('admin.login'))
            else:
                msg = '旧密码输入错误'
                return render_template('admin/changepwd.html', form=form, msg=msg)
        return render_template('admin/changepwd.html', form=form)
    form = PwdForm()
    return render_template('admin/changepwd.html', form=form)


@admin.route("/addtag", methods=['GET', 'POST'])
def addtag():
    '''
    添加标签
    :return:
    '''
    if request.method == 'POST':
        form = TagForm(request.form)
        tag = models.Tag(
            name=form.data.get('name')
        )
        db.session.add(tag)
        admin = getAdmin()
        getOplog(ip=request.remote_addr, admin_id=admin.id, reason='%s添加了%s标签' % (admin.name, form.data.get('name')))
        db.session.commit()
        return redirect(url_for('admin.taglist'))
    form = TagForm()
    return render_template('admin/tag_add.html', form=form)


@admin.route("/taglist")
def taglist():
    '''
    标签列表
    :return:
    '''
    tags = db.session.query(models.Tag).all()
    current_page = request.args.get('page', 1)
    total_count = len(tags)
    base_url = request.path
    parmas = request.args.to_dict()
    pageObj = Pagination(current_page, total_count, base_url, parmas)
    tags = tags[pageObj.start:pageObj.end]
    return render_template('admin/tag_list.html', tags=tags,pageObj=pageObj)


@admin.route('/edittag/<int:id>', methods=['GET', 'POST'])
def edittag(id):
    '''
    编辑标签
    :param id:
    :return:
    '''
    if request.method == 'POST':
        form = TagForm(request.form)
        tag = db.session.query(models.Tag).filter_by(id=id).first()
        db.session.query(models.Tag).filter_by(id=id).update({'name': form.data.get('name')})
        admin = getAdmin()
        getOplog(ip=request.remote_addr, admin_id=admin.id,
                 reason='%s将标签%s修改为了%s' % (admin.name, tag.name, form.data.get('name')))
        db.session.commit()
        return redirect(url_for('admin.taglist'))
    tag = db.session.query(models.Tag).filter_by(id=id).first()
    form = TagForm(data={'name': tag.name})
    return render_template('admin/tag_add.html', form=form)


@admin.route('/deltag/<int:id>')
def deltag(id):
    '''
    删除标签
    :param id:
    :return:
    '''
    tag = db.session.query(models.Tag).filter_by(id=id)
    db.session.query(models.Tag).filter_by(id=id).delete()
    admin = getAdmin()
    getOplog(ip=request.remote_addr, admin_id=admin.id,
             reason='%s将%s标签删除了' % (admin.name, tag.name))
    db.session.commit()

    return redirect(url_for('admin.taglist'))


@admin.route("/addmovie", methods=['GET', 'POST'])
def addmovie():
    '''
    添加电影
    :return:
    '''
    if request.method == 'POST':
        form = MovieForm(request.form)
        if form.validate():
            data = form.data

            file_url = secure_filename(form.url.data)
            file_logo = secure_filename(form.logo.data)

            if not os.path.exists(up_url):
                os.makedirs(up_url)
                os.chmod(up_url, 'rw')
            url = changeFilename(file_url)
            logo = changeFilename(file_logo)
            movie = models.Movie(
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
            admin = getAdmin()
            getOplog(ip=request.remote_addr, admin_id=admin.id,
                     reason='%s添加了电影%s' % (admin.name, data.get('title')))
            db.session.commit()
            flash('添加电影成功', 'ok')
            return redirect(url_for('admin.movielist'))

        return render_template('admin/movie_add.html', form=form)
    form = MovieForm()
    return render_template('admin/movie_add.html', form=form)


@admin.route("/movielist")
def movielist():
    '''
    电影列表
    :return:
    '''
    movielist = db.session.query(models.Movie).all()
    tag_names = {}
    for movie in movielist:
        tag_name = db.session.query(models.Tag.name).filter_by(id=movie.tag_id).first()
        tag_names[movie.id] = tag_name[0]
    current_page = request.args.get('page', 1)
    total_count = len(movielist)
    base_url = request.path
    parmas = request.args.to_dict()
    pageObj = Pagination(current_page, total_count, base_url, parmas)
    movielist = movielist[pageObj.start:pageObj.end]
    return render_template('admin/movie_list.html', movielist=movielist, tag_names=tag_names,pageObj=pageObj)


@admin.route('/editmovie/<int:id>', methods=['GET', 'POST'])
def editmovie(id):
    '''
    修改电影
    :param id:
    :return:
    '''
    if request.method == 'POST':
        form = MovieForm(request.form)
        if form.validate():
            data = form.data
            db.session.query(models.Movie).filter_by(id=id).update({
                'title': data.get('title'),
                'url': data.get('url'),
                'info': data.get('info'),
                'logo': data.get('logo'),
                'star': int(data.get('star')),
                'playnum': 0,
                'ommentnum': 0,
                'tag_id': int(data.get('tag')),
                'area': data.get('area'),
                'release_time': data.get('release_time'),
                'length': data.get('length')})

            admin = getAdmin()
            getOplog(ip=request.remote_addr, admin_id=admin.id,
                     reason='%s修改了电影%s' % (admin.name, data.get('title')))
            db.session.commit()
            return redirect(url_for('admin.movielist'))

    movie = db.session.query(models.Movie).filter_by(id=id).first()
    movie_dic = {
        'title': movie.title,
        'url': movie.url,
        'info': movie.info,
        'logo': movie.logo,
        'star': movie.star,
        'playnum': movie.playnum,
        'ommentnum': movie.ommentnum,
        'tag_id': movie.tag_id,
        'area': movie.area,
        'release_time': movie.release_time,
        'length': movie.length
    }
    form = MovieForm(data=movie_dic)
    return render_template('admin/movie_add.html', form=form)


@admin.route('/delmovie/<int:id>')
def delmovie(id):
    '''
    删除电影
    :param id:
    :return:
    '''
    movie = db.session.query(models.Movie).filter_by(id=id)
    db.session.query(models.Movie).filter_by(id=id).delete()
    admin = getAdmin()
    getOplog(ip=request.remote_addr, admin_id=admin.id,
             reason='%s删除了电影%s' % (admin.name, movie.title))
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
    users = db.session.query(models.User).all()

    current_page = request.args.get('page', 1)
    total_count = len(users)
    base_url = request.path
    parmas = request.args.to_dict()
    pageObj = Pagination(current_page, total_count, base_url, parmas)
    users = users[pageObj.start:pageObj.end]
    return render_template('admin/user_list.html', users=users, pageObj=pageObj)


@admin.route("/userview/<int:id>")
def userview(id):
    '''
    会员详细界面
    :return:
    '''
    user = db.session.query(models.User).filter_by(id=id).first()
    return render_template('admin/user_view.html', user=user)


@admin.route("/commentlist")
def commentlist():
    '''
    评论列表管理
    :return:
    '''
    comments = db.session.query(models.Comment).join(models.User).join(
        models.Movie).filter(models.Comment.user_id == models.User.id).filter(
        models.Comment.movie_id == models.Movie.id
    ).all()
    current_page = request.args.get('page', 1)
    total_count = len(comments)
    base_url = request.path
    parmas = request.args.to_dict()
    pageObj = Pagination(current_page, total_count, base_url, parmas)
    comments = comments[pageObj.start:pageObj.end]
    return render_template('admin/comment_list.html', comments=comments,pageObj=pageObj)


@admin.route('/delcomment/<int:id>')
def delcomment(id):
    '''
    删除评论
    :param id:
    :return:
    '''
    con = db.session.query(models.Comment).filter_by(id=id)
    db.session.query(models.Comment).filter_by(id=id).delete()
    admin = getAdmin()
    getOplog(ip=request.remote_addr, admin_id=admin.id,
             reason='%s删除了评论%s' % (admin.name, con.content))
    db.session.commit()
    return redirect(url_for('admin.commentlist'))


@admin.route("/moviecol_list")
def moviecol_list():
    '''
    电影收藏列表
    :return:
    '''

    moviecols = db.session.query(models.MovieCol).join(models.User).join(models.Movie).filter(
        models.MovieCol.movie_id == models.Movie.id
    ).filter(models.MovieCol.user_id == models.User.id).order_by(models.MovieCol.addtime.desc()).all()
    current_page = request.args.get('page', 1)
    total_count = len(moviecols)
    base_url = request.path
    parmas = request.args.to_dict()
    pageObj = Pagination(current_page, total_count, base_url, parmas)
    moviecols = moviecols[pageObj.start:pageObj.end]
    return render_template('admin/moviecol_list.html', moviecols=moviecols,pageObj=pageObj)


@admin.route('/delmoviecol/<int:id>')
def delmoviecol(id):
    '''
    删除电影收藏
    :param id:
    :return:
    '''

    moviecol = db.session.query(models.MovieCol).filter_by(id=id).first()
    movie = db.session.query(models.Movie).filter_by(id=moviecol.movie_id).first()
    db.session.query(models.MovieCol).filter_by(id=id).delete()
    admin = getAdmin()
    getOplog(ip=request.remote_addr, admin_id=admin.id,
             reason='%s删除了电影%s' % (admin.name, movie.title))
    db.session.commit()
    return redirect(url_for('admin.moviecol_list'))


@admin.route('/oplog_list')
def oplog_list():
    '''
    操作日志列表
    :return:
    '''
    oplogs = db.session.query(models.Oplog).all()

    current_page = request.args.get('page', 1)
    total_count = len(oplogs)
    base_url = request.path
    parmas = request.args.to_dict()
    pageObj = Pagination(current_page, total_count, base_url, parmas)
    oplogs = oplogs[pageObj.start:pageObj.end]
    return render_template('admin/oplog_list.html', oplogs=oplogs,pageObj=pageObj)


@admin.route('/adminloginlog_list')
def adminloginlog_list():
    '''
    管理员登录日志列表
    :return:
    '''
    adminlogs=db.session.query(models.Adminlog).all()

    current_page = request.args.get('page', 1)
    total_count = len(adminlogs)
    base_url = request.path
    parmas = request.args.to_dict()
    pageObj = Pagination(current_page, total_count, base_url, parmas)
    adminlogs = adminlogs[pageObj.start:pageObj.end]
    return render_template('admin/adminloginlog_list.html',adminlogs=adminlogs,pageObj=pageObj)


@admin.route('/userloginlog_list')
def userloginlog_list():
    '''
    会员登录日志列表
    :return:
    '''
    userlogs=db.session.query(models.Userlog).all()
    return render_template('admin/userloginlog_list.html',userlogs=userlogs)


@admin.route('/addAuth',methods=['GET', 'POST'])
def addAuth():
    '''
    添加权限
    :return:
    '''
    if request.method=='POST':
        form=AuthForm(request.form)
        if form.validate():
            data=form.data
            auth=models.Auth(name=data.get('name'),url=data.get('url'))
            db.session.add(auth)

            admin = getAdmin()
            getOplog(ip=request.remote_addr, admin_id=admin.id,
                     reason='%s增加了权限%s' % (admin.name,data.get('name')))
            db.session.commit()
            return redirect(url_for('admin.authlist'))
        return render_template('admin/addAuth.html', form=form)
    form=AuthForm()
    return render_template('admin/addAuth.html',form=form)

@admin.route('/authlist')
def authlist():
    '''
    权限列表
    :return:
    '''
    auths=db.session.query(models.Auth).all()
    current_page = request.args.get('page', 1)
    total_count = len(auths)
    base_url = request.path
    parmas = request.args.to_dict()
    pageObj = Pagination(current_page, total_count, base_url, parmas)
    auths = auths[pageObj.start:pageObj.end]
    return render_template('admin/authlist.html',auths=auths,pageObj=pageObj)

@admin.route('/editauth/<int:id>',methods=['GET', 'POST'])
def editauth(id):
    '''
    编辑权限
    :param id:
    :return:
    '''
    if request.method=='POST':
        form=AuthForm(request.form)
        if form.validate():
            data=form.data
            db.session.query(models.Auth).filter_by(id=id).update({'name':data.get('name'),'url':data.get('url')})
            admin = getAdmin()
            getOplog(ip=request.remote_addr, admin_id=admin.id,
                     reason='%s修改了权限%s' % (admin.name, data.get('name')))
            db.session.commit()
            return redirect(url_for('admin.authlist'))
        return render_template('admin/addAuth.html', form=form)
    auth=db.session.query(models.Auth).filter_by(id=id).first()
    form=AuthForm(data={'name':auth.name,'url':auth.url})
    return render_template('admin/addAuth.html',form=form)

@admin.route('/delauth/<int:id>')
def delauth(id):
    '''
    删除权限
    :param id:
    :return:
    '''
    auth=db.session.query(models.Auth).filter_by(id=id)
    db.session.query(models.Auth).filter_by(id=id).delete()
    admin = getAdmin()
    getOplog(ip=request.remote_addr, admin_id=admin.id,
             reason='%s删除了权限%s' % (admin.name, auth.name))
    db.session.commit()
    return redirect(url_for('admin.authlist'))


@admin.route('/addrole',methods=['GET','POST'])
def addrole():
    '''
    添加角色
    :return:
    '''
    if request.method=='POST':
        form=RoleForm(request.form)
        if form.validate():
            data=form.data
            role=models.Role(
                name=data.get('name'),
                auths='-'.join(map(lambda x:str(x),data.get('auths')))
            )
            db.session.add(role)
            admin = getAdmin()
            getOplog(ip=request.remote_addr, admin_id=admin.id,
                     reason='%s添加了角色%s' % (admin.name, data.get('name')))
            db.session.commit()
            return redirect(url_for('admin.rolelist'))
        return render_template('admin/addrole.html', form=form)
    form=RoleForm()
    return render_template('admin/addrole.html',form=form)

@admin.route('/editrole/<int:id>',methods=['GET','POST'])
def editrole(id):
    if request.method=='POST':
        form=RoleForm(request.form)
        if form.validate():
            data=form.data
            db.session.query(models.Role).filter_by(id=id).update({'name':data.get('name'),
                                                                   'auths':'-'.join(map(lambda x:str(x),data.get('auths') ))})
            admin = getAdmin()
            getOplog(ip=request.remote_addr, admin_id=admin.id,
                     reason='%s修改了角色%s' % (admin.name, data.get('name')))
            db.session.commit()
            return redirect(url_for('admin.rolelist'))
        return render_template('admin/addrole.html', form=form)
    role=db.session.query(models.Role).filter_by(id=id).first()

    if '-' in role.auths:
        auths=list(map(lambda x:int(x),role.auths.split('-')))
    else:
        auths=role.auths
    form=RoleForm(data={'name':role.name,'auths':auths})
    return render_template('admin/addrole.html', form=form)

@admin.route('/delrole/<int:id>')
def delrole(id):
    pass

@admin.route('/rolelist')
def rolelist():
    '''
    角色列表
    :return:
    '''
    roles=db.session.query(models.Role).all()
    current_page = request.args.get('page', 1)
    total_count = len(roles)
    base_url = request.path
    parmas = request.args.to_dict()
    pageObj = Pagination(current_page, total_count, base_url, parmas)
    roles = roles[pageObj.start:pageObj.end]
    return  render_template('admin/rolelist.html',roles=roles,pageObj=pageObj)


@admin.route('/admin_add',methods=['GET','POST'])
def admin_add():
    if request.method=='POST':
        form=AdminForm(request.form)
        print(form.data)
        if form.validate():
            data=form.data
            print(data)
            admin=models.Admin(name=data.get('name'),pwd=data.get('pwd'),role_id=int(data.get('role')))
            db.session.add(admin)
            admin = getAdmin()
            getOplog(ip=request.remote_addr, admin_id=admin.id,
                     reason='%s添加了管理员%s' % (admin.name, data.get('name')))
            db.session.commit()
            return redirect(url_for('admin.admin_list'))
        return render_template('admin/admin_add.html', form=form)
    form=AdminForm()
    return render_template('admin/admin_add.html',form=form)


@admin.route('/admin_list')
def admin_list():
    admins=db.session.query(models.Admin).all()
    current_page = request.args.get('page', 1)
    total_count = len(admins)
    base_url = request.path
    parmas = request.args.to_dict()
    pageObj = Pagination(current_page, total_count, base_url, parmas)
    admins = admins[pageObj.start:pageObj.end]
    return render_template('admin/admin_list.html',admins=admins,pageObj=pageObj)
