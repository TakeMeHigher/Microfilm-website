#coding:utf8
from flask import render_template,redirect,url_for,request,session,flash
from . import admin
from  app.admin.forms import LoginForm
from  app.models import Admin
from  app import db


@admin.before_request
def check_is_login():

    if request.path=='/admin/login':
        return None



    if not session.get('admin'):
        return redirect(url_for('admin.login'))



@admin.route("/")
def index():
    return render_template('admin/index.html')


@admin.route("/login",methods=['GET','POST'])
def login():
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
    session['admin']=''
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


@admin.route("/commentlist")
def commentlist():
    return render_template('admin/comment_list.html')


@admin.route("/moviecol_list")
def moviecol_list():
    return render_template('admin/moviecol_list.html')

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