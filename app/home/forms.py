from wtforms import Form
from wtforms.fields import simple,core,html5
from wtforms import widgets
from wtforms import  validators

from app.models import Admin
from app import models
from app import db


class RegForm(Form):
    name = simple.StringField(
        validators=[
            validators.DataRequired(message='会员昵称不能为空')
        ],
        widget=widgets.TextInput(),
        render_kw={'class': "form-control input-lg", 'placeholder': "请输入会员昵称！",'id':"input_name"}
    )

    pwd = simple.StringField(
        validators=[
            validators.DataRequired(message='密码不能为空')
        ],
        render_kw={'class': "form-control input-lg", 'placeholder': "请输入密码!", 'id': "input_password"},
        widget=widgets.PasswordInput()
    )

    confirmpwd = simple.StringField(
        label='确认密码',
        validators=[
            validators.DataRequired(message='重复密码不能为空'),
            validators.EqualTo('pwd',message='两次输入密码不一致')
        ],
        render_kw={'class': "form-control", 'placeholder': "请输入确认密码!",'id':'input_repassword'},
        widget=widgets.PasswordInput()
    )

    email = html5.EmailField(
        validators=[
            validators.DataRequired(message='邮箱不能为空'),
            validators.Email(message='邮箱格式不正确')
        ],
        widget=widgets.TextInput(),
        render_kw={"class": "form-control input-lg",'placeholder': "请输入邮箱!",'id':"input_email"}
    )

    phone=simple.StringField(
        validators=[
            validators.DataRequired(message='请输入手机号码'),
            validators.Regexp('^[1][3,4,5,7,8][0-9]{9}$',message='手机号码格式不正确')
        ],
        widget=widgets.TextInput(),
        render_kw={'id':"input_phone","class": "form-control input-lg",'placeholder': "请输入手机号码!"}
    )

    def validate_name(self, field):
        count = db.session.query(models.User).filter_by(name=field.data).count()
        if count:
            raise validators.StopValidation('该名称已经被占用')





class LoginForm(Form):
    '''
    会员登录
    '''
    name = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired(message='用户名不能为空')
        ],
        render_kw={'class': "form-control", 'placeholder': "请输入用户名!",'id':'input_contact'},
        widget=widgets.TextInput()
    )

    pwd = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空')
        ],
        render_kw={'class': "form-control", 'placeholder': "请输入密码!",'id':'input_password'},
        widget=widgets.TextInput()
    )

    def validate_name(self, field):
        name = field.data
        print(name, '-----')
        count =models.User.query.filter_by(name=name).count()
        if count == 0:
            raise validators.StopValidation('用户名不存在')



class UserForm(Form):
    name = simple.StringField(
        validators=[
            validators.DataRequired(message='会员昵称不能为空')
        ],
        widget=widgets.TextInput(),
        render_kw={'class': "form-control input-lg", 'placeholder': "请输入会员昵称！", 'id': "input_name"}
    )

    email = html5.EmailField(
        validators=[
            validators.DataRequired(message='邮箱不能为空'),
            validators.Email(message='邮箱格式不正确')
        ],
        widget=widgets.TextInput(),
        render_kw={"class": "form-control input-lg", 'placeholder': "请输入邮箱!", 'id': "input_email"}
    )

    phone = simple.StringField(
        validators=[
            validators.DataRequired(message='请输入手机号码'),
            validators.Regexp('^[1][3,4,5,7,8][0-9]{9}$', message='手机号码格式不正确')
        ],
        widget=widgets.TextInput(),
        render_kw={'id': "input_phone", "class": "form-control input-lg", 'placeholder': "请输入手机号码!"}
    )

    avatar=simple.FileField(
        label='头像',
        validators=[
            validators.DataRequired(message='头像不能为空')
        ],
        widget=widgets.FileInput(),
        render_kw={'id':"avatar_file"}

    )
    info = simple.TextAreaField(
        label='简介',
        validators={
            validators.DataRequired(message='简介不能为空')
        },
        widget=widgets.TextArea(),
        render_kw={'class': "form-control", 'rows': "10", 'id': "input_info"}
    )
