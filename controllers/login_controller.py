from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from models.user.users import User
import flask_login
from flask_login import LoginManager, logout_user, current_user

login_ = Blueprint("login", __name__, template_folder="templates")

@login_.route('/validated_user', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.validate_user(email, password)

        if user is None:
            flash('Usuário e/ou senha incorreta!', category='danger')
            return render_template('login.html')
        else:
            flask_login.login_user(user)
            user_role_id = User.get_user_role(user)

            if user_role_id == 1:
                return render_template('adm.html', roles=user_role_id)
            elif user_role_id == 1 or user_role_id == 2:
                return render_template('estatistico.html', roles=user_role_id)
            elif user_role_id == 1 or user_role_id == 3:
                return render_template('operador.html', roles=user_role_id)
            else:
                return render_template('login.html')
    else:
        return render_template('login.html')

@login_.route('/logoff')
def logoff():
    logout_user()
    return render_template("login.html")


