from wtforms import Field
from  wtforms import Form
from wtforms.fields import simple
from  wtforms.fields import html5
from wtforms.fields import core
from wtforms import validators
from wtforms import widgets

from app.models import Admin

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


