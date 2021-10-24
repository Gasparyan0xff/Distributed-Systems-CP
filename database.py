from user import EMPLOYEE, MANAGER, User
from flask_sqlalchemy import SQLAlchemy
from server_data import DBTasker



class UserEntity(DBTasker.Model):
    __tablename__ = "User"
    id = DBTasker.Column(DBTasker.Integer, primary_key=True)
    login = DBTasker.Column(DBTasker.String(255), nullable=False)
    password = DBTasker.Column(DBTasker.String(255), nullable=False)
    name = DBTasker.Column(DBTasker.Text, nullable=False)
    UserType = DBTasker.Column(DBTasker.Integer, nullable=False)
    
    def __repr__(self):
        return '%r; %r; %r; %r' % (self.id, self.login, self.name, self.UserType) 


class UserTypeEntity(DBTasker.Model):
    __tablename__ = "UserType"
    id = DBTasker.Column(DBTasker.Integer, primary_key=True)
    TypeName = DBTasker.Column(DBTasker.Text, nullable=False)

    def __repr__(self):
        return self.TypeName


class TaskEntity(DBTasker.Model):
    __tablename__ = "Task"
    id = DBTasker.Column(DBTasker.Integer, primary_key=True)
    appDate = DBTasker.Column(DBTasker.DateTime(timezone=True), nullable=False, default=DBTasker.func.now())
    priority = DBTasker.Column(DBTasker.Integer, nullable=False)
    completed = DBTasker.Column(DBTasker.Boolean, nullable=False)
    mark_complete = DBTasker.Column(DBTasker.Boolean, nullable=False)
    content = DBTasker.Column(DBTasker.Text, nullable=False)

    def __repr__(self):
        return '%r; %r; %r; %r; %r; %r' % (self.id, self.appDate, self.priority, self.completed, self.mark_complete, self.content)

class EmployeeManagerEntity(DBTasker.Model):
    __tablename__ = "EmployeeManager"
    id = DBTasker.Column(DBTasker.Integer, primary_key=True)
    idManager = DBTasker.Column(DBTasker.Integer, nullable=False)
    idEmpl = DBTasker.Column(DBTasker.Integer, nullable=False)

    def __repr__(self):
        return '(%r; %r; %r;)' % (self.id, self.idManager, self.idEmpl) 

class EmployeeTaskEntity(DBTasker.Model):
    __tablename__ = "EmployeeTask"
    id = DBTasker.Column(DBTasker.Integer, primary_key=True)
    idEmployee = DBTasker.Column(DBTasker.Integer, nullable=False)
    idTask = DBTasker.Column(DBTasker.Integer, nullable=False)

    def __repr__(self):
        return '%r; %r; %r' % (self.id, self.idEmployee, self.idTask) 
