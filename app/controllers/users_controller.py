from flask import Blueprint, request, render_template, redirect, url_for
from models.user.users import User
from models.user.roles import Role
import flask_login
from flask_login import current_user

user = Blueprint("user",__name__, template_folder="views")

@user.route('/register_user')
@flask_login.login_required
def register_user():
    roles = Role.get_role()
    return render_template("register_user.html", role=roles, roles=current_user.role_id)

@user.route('/add_user', methods=['POST'])
@flask_login.login_required
def add_user():
    if request.method == 'POST':
        role_name = request.form['role_type_']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        User.save_user(role_name, username, email, password)

        users = User.get_users()
        return render_template("users.html", devices = users, roles=current_user.role_id)

@user.route('/users')
@flask_login.login_required
def users():
    users = User.get_users()
    return render_template("users.html", devices = users, roles=current_user.role_id)

@user.route('/edit_user')
@flask_login.login_required
def edit_user():
    email = request.args.get('email', None)
    user = User.get_single_user(email)
    roles = Role.get_role()
    return render_template("update_user.html", users = user, role = roles, roles=current_user.role_id)

@user.route('/update_user', methods=['POST'])
@flask_login.login_required
def update_user():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    role_type_ = request.form.get("role_type_")

    users = User.update_user(role_type_, username, email, password)
    
    return render_template("users.html", devices = users, roles=current_user.role_id)

@user.route('/del_user', methods=['GET'])
@flask_login.login_required
def del_user():
    email = request.args.get('email', None)
    users = User.delete_user(email)
    return render_template("users.html", devices = users, roles=current_user.role_id)