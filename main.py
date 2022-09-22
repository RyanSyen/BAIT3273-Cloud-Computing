from flask import Flask, render_template, request, url_for, redirect, flash
from admin.EmpAppUpdated import adminBlueprint

app = Fapp = Flask(__name__)
app.register_blueprint(adminBlueprint, url_prefix="/admin")
app.secret_key = "abc"


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/login", methods=['POST'])
def login():
    error = None
    if request.method == "POST":
        empid = request.form['id']
        password = request.form['password']
        print("id=" + empid + ', pw=' + password)
        if empid != 9999 and password != 'Bait3273':
            flash('Login unsuccessful! Please try again.💪')
            error = "invalid password!"
        else:
            flash('Login successful! 🌟')
            return redirect(url_for('admin.index'))
    return render_template('index.html', error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=100, debug=True)
