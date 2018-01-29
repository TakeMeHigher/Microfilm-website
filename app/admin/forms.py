from wtforms import Field
from  wtforms import Form
from wtforms.fields import simple
from  wtforms.fields import html5
from wtforms.fields import core
from wtforms import validators
from wtforms import widgets

from app.models import Admin
from app import models
from app import db

class LoginForm(Form):
    account=simple.StringField(
        label='账号',
        validators=[
            validators.DataRequired(message='账号不能为空')
        ],
        render_kw={'class':"form-control",'placeholder':"请输入账号!"},
        widget=widgets.TextInput()
    )

    pwd=simple.PasswordField(
       label='密码',
       validators=[
           validators.DataRequired(message='密码不能为空')
       ],
       render_kw={'class':"form-control" ,'placeholder':"请输入密码!"},
       widget=widgets.TextInput()
    )

    submit=simple.SubmitField(
        label='提交',
        widget=widgets.SubmitInput(),
        render_kw={'id':"btn-sub",'class':'btn btn-primary btn-block btn-flat'}
    )



    def validate_account(self,field):
        name=field.data
        print(name,'-----')
        count=Admin.query.filter_by(name=name).count()
        if count==0:
            raise validators.StopValidation('用户名不存在')


class MovieForm(Form):
    title = simple.StringField(
        label='片名',
        validators=[
            validators.DataRequired(message='片名不能为空')
        ],
        render_kw={'class': "form-control", 'placeholder': "请输入片名!",'id':"input_title" },
        widget=widgets.TextInput()
    )
    url=simple.FileField(
        label='文件',
        validators={
            validators.DataRequired(message='文件不能为空')
        },
        widget=widgets.FileInput(),
        render_kw={'id':"input_url"}
    )
    info=simple.TextAreaField(
        label='简介',
        validators={
            validators.DataRequired(message='简介不能为空')
        },
        widget=widgets.TextArea(),
        render_kw={'class':"form-control" ,'rows':"10",'id':"input_info"}
    )

    logo = simple.FileField(
        label='封面',
        validators={
            validators.DataRequired(message='封面不能为空')
        },
        widget=widgets.FileInput(),
        render_kw={'id': "nput_logo"}
    )
    star=core.SelectField(
        label='星级',
        choices=(
            (1,'1星'),
            (2,'2星'),
            (3,'3星'),
            (4,'4星'),
            (5,'5星')
        ),
        coerce=int
    )
    tag=core.SelectField(
        label='类型',
        # choices=(
        #     (1, '科幻'),
        #     (2, '冒险'),
        #     (3, '爱情'),
        #     (4, '动作'),
        #     (5, '战争')
        # ),
        choices='',
        coerce=int

    )

    area=simple.StringField(
        label='地区',
        validators={
            validators.DataRequired(message='地区不能为空')
        },
        widget=widgets.TextInput(),
        render_kw={'class':"form-control", 'id':"input_area" ,'placeholder':"请输入地区！"}
    )

    length = simple.StringField(
        label='片长',
        validators={
            validators.DataRequired(message='片长不能为空')
        },
        widget=widgets.TextInput(),
        render_kw={'class': "form-control", 'id': "input_length", 'placeholder': "请输入片长！"}
    )

    release_time = simple.StringField(
        label='上映时间',
        validators={
            validators.DataRequired(message='片长不能为空')
        },
        widget=widgets.TextInput(),
        render_kw={'class': "form-control", 'id': "input_release_time", 'placeholder': "请输入上映时间！"}
    )

    submit = simple.SubmitField(
        label='提交',
        widget=widgets.SubmitInput(),
        render_kw={'id': "btn-sub", 'class': 'btn btn-primary btn-block btn-flat'}
    )



    def __init__(self,*args,**kwargs):
        super(MovieForm,self).__init__(*args,**kwargs)
        self.tag.choices=db.session.query(models.Tag.id,models.Tag.name).all()


class TagForm(Form):
    name = simple.StringField(
        label='标签名',
        validators=[
            validators.DataRequired(message='标签名不能为空')
        ],
        render_kw={'class': "form-control", 'placeholder': "请输入标签名!", 'id': "input_name"},
        widget=widgets.TextInput()
    )







