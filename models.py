from datetime import datetime

from flask_security import UserMixin, RoleMixin

from app import db

roles_users = db.Table(
    'roles_users', db.Column('user_id', db.Integer(),
                             db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    comment = db.Column(db.String(200))
    created = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __init__(self, *args, **kwargs):
        super(comments, self).__init__(*args, **kwargs)

    #def __init__(self, *args, **kwargs):
    #    super(comments, self).__init__(*args, **kwargs)
    #    self.slug = slugify(self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    avatar = db.Column(db.String(255), default="default.jpg")
    active = db.Column(db.Boolean())
    comments = db.relationship('comments', backref='user')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User id: {}, email: {}, password: {}, active: {}>'.format(
            self.id, self.email, self.password, self.active)

    roles = db.relationship('Roles',
                            secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, *args, **kwargs):
        super(Roles, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Role id: {}, name: {}, description: {}>'.format(
            self.id, self.name, self.description)
