from flask import Flask, redirect, url_for, request

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security, current_user
from flask_security.forms import RegisterForm

from wtforms import StringField
from wtforms.validators import InputRequired

from flask_admin import Admin, expose
from flask_admin import AdminIndexView, BaseView
from flask_admin.contrib.sqla import ModelView

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from models import *


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


def get_comment(comment_id):
    return comments.query.filter(comments.id == comment_id)


class MyHomeView(AdminIndexView):
    @expose('/', methods=['POST', 'GET'])
    def index(self):
        if request.method == 'POST':
            if 'btn-block' in request.form:
                comment = get_comment(request.form['btn-block']).first()
                comment.is_active = False
            elif 'btn-allow' in request.form:
                comment = get_comment(request.form['btn-allow']).first()
                comment.is_active = True
            elif 'btn-delete' in request.form:
                comment = get_comment(request.form['btn-delete']).delete()
            db.session.commit()
            return redirect(url_for('admin.index'))
        users_comments = comments.query.all()
        users_comments.reverse()
        return self.render('admin/index.html', users_comments=users_comments)


admin = Admin(app,
              'CRUD Comment Admin',
              url='/',
              index_view=MyHomeView(name='Home'),
              template_mode='bootstrap3')

admin.add_view(AdminView(comments, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Roles, db.session))


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Name', [InputRequired()])


user_datastore = SQLAlchemyUserDatastore(db, User, Roles)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)
