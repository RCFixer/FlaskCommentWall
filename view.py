from re import compile
from os import path, remove

from flask import render_template, request, redirect, url_for, flash
from flask_security import current_user
from flask_security.utils import hash_password, verify_password
from flask_security import login_required

from werkzeug.utils import secure_filename

from models import comments
from app import app, db


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        comment = request.form.get('text')
        if comment == '':
            flash('Заполните поле "Сообщение"', 'post_message')
        else:
            add_comment = comments(name=current_user.username,
                                   comment=comment,
                                   is_active=True,
                                   user=current_user)
            db.session.add(add_comment)
            db.session.commit()
            flash('Комментарий успешно добавлен', 'view_comment')
        return redirect(url_for('index'))
    users_comments = comments.query.all()
    users_comments.reverse()
    return render_template('index.html', users_comments=users_comments)


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    if request.method == 'POST':
        if request.form['btn'] == 'info':
            email_pattern = compile(
                '(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
            name = request.form.get('name')
            email = request.form.get('email')
            image = request.files["image"]
            if bool(image.filename):
                filename = secure_filename(image.filename)
                filename = str(current_user.id) + '.' + filename.split('.')[-1]
                remove(app.config['UPLOAD_FOLDER'] + '/' + current_user.avatar)
                image.save(path.join(app.config['UPLOAD_FOLDER'], filename))
                image.close()
                current_user.avatar = filename
            email_is_valid = email_pattern.match(email)
            if name == '' or email == '':
                if email == '':
                    flash('Заполните поле "Email"', 'profile_email')
                if name == '':
                    flash('Заполните поле "Name"', 'profile_name')
            else:
                if email_is_valid:
                    current_user.username = name
                    current_user.email = email
                else:
                    flash('Ошибка валидации', 'profile_email')

            db.session.commit()
            flash('Профиль успешно обновлен', 'profile_messages')

            return redirect(url_for('profile'))
        if request.form['btn'] == 'pass':
            current = request.form.get('current')
            password = request.form.get('password')
            password_confirmation = request.form.get('password_confirmation')
            true_current = current_user.password
            if current == '' or password == '' or password_confirmation == '':
                if current == '':
                    flash('Заполните поле "Текущий пароль"', 'sec_current')
                if password == '':
                    flash('Заполните поле "Новый пароль"', 'sec_password')
                if password_confirmation == '':
                    flash('Заполните поле "Новый пароль ещё раз"',
                          'sec_pass_conf')
            else:
                if len(current) < 6 or len(password) < 6 or len(
                        password_confirmation) < 6:
                    if len(current) < 6:
                        flash(
                            'В поле "Текущий пароль" должно быть не меньше 6-ти символов',
                            'sec_current')
                    if len(password) < 6:
                        flash(
                            'В поле "Новый пароль" должно быть не меньше 6-ти символов',
                            'sec_password')
                    if len(password_confirmation) < 6:
                        flash(
                            'В поле  "Новый пароль ещё раз" должно быть не меньше 6-ти символов',
                            'sec_pass_conf')
                else:
                    if verify_password(current, true_current):
                        if password == password_confirmation:
                            current_user.password = hash_password(password)
                            db.session.commit()
                            flash('Пароль успешно обновлен', 'pass_change')
                        else:
                            flash(
                                '"Новый пароль" и "Новый пароль ещё раз" должны совпадать',
                                'sec_current')
                    else:
                        flash('Текущий пароль введён не верно', 'sec_current')
            return redirect(url_for('profile'))
    return render_template('profile.html')
