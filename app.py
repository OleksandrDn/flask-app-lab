from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def main():
    return render_template("hello.html")


@app.route('/homepage')
def home():
    """View foe the Home page of your website"""
    agent = request.user_agent


    return render_template("hello.html", agent=agent)

@app.route('/user/<string:name>')
def greeting(name):
    name = name.upper()
    age = request.args.get('age', 0, int)
    year = 2024 - age
    return f'Welcome, {name} - {year}!'


@app.route('/admin')
def admin():
    to_url = url_for("greeting", name='administrator', age=30, _external=True)
    print(to_url)
    return redirect(to_url)


if __name__ == '__main__':
    app.run(debug=True)
