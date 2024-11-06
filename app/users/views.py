from flask import render_template, request, redirect, url_for, make_response, session, flash
from . import user_bp  # Можливо, ім'я Blueprint вказане як users у вашому __init__.py
from datetime import timedelta

@user_bp.route('/set_theme/<theme>')
def set_theme(theme):
    if theme in ['light', 'dark']:  # Дозволяємо тільки два варіанти
        response = make_response(redirect('/user/profile'))  # Перенаправляємо на сторінку профілю
        response.set_cookie('theme', theme)  # Зберігаємо вибір користувача в куці
        flash(f'Тема змінена на {theme}.', 'success')  # Виводимо повідомлення
        return response
    flash('Невірна тема.', 'danger')
    return redirect('/profile')




@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        flash('Будь ласка, увійдіть у систему.', 'danger')
        return redirect('/login')

    theme = request.cookies.get('theme', 'light')  # Витягуємо тему з куки або ставимо 'light' за замовчуванням

    if request.method == 'POST':
        action = request.form.get('action')
        cookie_key = request.form.get('cookie_key')
        cookie_value = request.form.get('cookie_value')

        if action == 'add':
            expires = request.form.get('expires')
            response = make_response(redirect('/profile'))
            response.set_cookie(cookie_key, cookie_value, max_age=int(expires) if expires else None)
            flash(f'Кукі "{cookie_key}" успішно додано.', 'success')
            return response

        elif action == 'delete':
            response = make_response(redirect('/profile'))
            response.delete_cookie(cookie_key)
            flash(f'Кукі "{cookie_key}" успішно видалено.', 'success')
            return response

    cookies = request.cookies  # Отримати всі кукі
    return render_template('profile.html', username=session['username'], cookies=cookies, theme=theme)



# Зазначаємо правильні дані для входу
VALID_USERNAME = "testuser"
VALID_PASSWORD = "password123"

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Перевірка правильності даних
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username  # Зберігаємо користувача в сесію
            flash("Вхід успішний!", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Невірні дані для входу. Спробуйте ще раз.", "danger")
            return redirect(url_for("users.login"))
    
    return render_template("login.html")

@user_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Видаляємо ім'я користувача з сесії
    flash("Ви вийшли з системи.", "success")
    return redirect(url_for('users.login'))



@user_bp.route('/hi/<string:name>')
def greeting(name):
    name = name.upper()
    age = request.args.get('age', 0, int)
    return render_template('users/hi.html', name=name, age=age)

@user_bp.route('/admin')
def admin():
    to_url = url_for("users.greeting", age=45,
                     name='administrator', external=True)  # Змінили на users.greeting
    print(to_url)
    return redirect(to_url)

@user_bp.route('/set_cookie') 
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    response.set_cookie('color', '', max_age=timedelta(seconds=60))
    return response

@user_bp.route('/get_cookie') 
def get_cookie():
    username = request.cookies.get('username') 
    return f'Користувач: {username}'

@user_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) 
    return response
