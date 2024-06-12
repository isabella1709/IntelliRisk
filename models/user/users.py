#users.py
from models.db import db
from models.user.roles import Role
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__= "users"
    id = db.Column("id", db.Integer(), primary_key=True)
    role_id = db.Column( db.Integer, db.ForeignKey(Role.id))
    username= db.Column(db.String(45) , nullable=False, unique=True)
    email= db.Column(db.String(30), nullable=False, unique=True)
    password= db.Column(db.String(256) , nullable=False)

    def save_user(role_type_, username, email, password):
        role = Role.get_single_role(role_type_)
        user = User(role_id = role.id, username = username, email = email,
        password = generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
    
    def get_users():
        users = User.query.join(Role, Role.id == User.role_id)\
        .add_columns(Role.id, Role.name,
        Role.description, User.username,
        User.email, User.password).all()
        return users
    
    def get_single_user(email):
        user = User.query.filter(User.email == email).first()

        if user is not None:
            user = User.query.filter(User.email == email)\
            .join(Role).add_columns(Role.id, Role.name, Role.description,
            User.role_id, User.username, User.email, User.password).first()

            return [user]
        
    def update_user(role_type_, username, email, password):
        role = Role.get_single_role(role_type_)
        user = User.query.filter(User.email == email).first()
        if role is not None:
            user.role_id = role.id
            user.username = username
            user.email = email
            user.password = password
            db.session.commit()
            
            return User.get_users()
        
    def delete_user(email):
        adm = Role.get_single_role("Admin")
        user = User.query.filter(User.email == email).first()

        if user.role_id != adm.id:
            db.session.delete(user)
            db.session.commit()
        
        return User.get_users()

    def get_user_id(user_id):
        id = User.query.filter_by(id = user_id).first()
        if id is not None:
            return id

    def validate_user(email,password):
        user = User.query.filter(User.email == email).first()
        if(user==None or not check_password_hash(user.password,password)):
            return None
        else:
            return user
        
    def get_user_role(user):
        user = User.query.filter(User.email == user.email).first()
        return user.role_id
