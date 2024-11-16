from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db, bcrypt, app
from app.models import User
from app.formes import RegistrationForm, LoginForm, EditProfileForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Хэширование пароля
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Сохранение пользователя
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        # Поиск пользователя в базе данных по email
        user = User.query.filter_by(email=form.email.data).first()
        # Проверка пароля
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Авторизация пользователя
            login_user(user, remember=form.remember.data)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неверный email или пароль.', 'danger')

    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)


@app.route('/account/edit', methods=['GET', 'POST'])
def edit_account():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = password

        db.session.commit()
        flash('Ваш профиль успешно обновлен!', 'success')
        return redirect(url_for('account'))

    # Предзаполнение формы текущими данными пользователя
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('edit_account.html', form=form)