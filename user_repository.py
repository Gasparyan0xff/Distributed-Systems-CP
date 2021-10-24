from user import EMPLOYEE, MANAGER, Employee, Manager, User
from task import Task
from database import *


class UserRepository(object):
    def __init__(self):
        return

    '''
    '''
    def register_user(self, login, password, name, usertype, managerId):
        logins = UserEntity.query.filter_by(login=login).first()
        
        if (logins != None):
            return False
        
        newuser = UserEntity(login=login, password=password, name=name, UserType=usertype)
        DBTasker.session.add(newuser)
        DBTasker.session.flush()
        DBTasker.session.commit()
        
        status = newuser != None
        if (status == False):
            return False

        if managerId >= 1:
            newempl = EmployeeManagerEntity(idManager=managerId, idEmpl=newuser.id)
            DBTasker.session.add(newempl)
            DBTasker.session.commit()
            print(newempl.id)
            status = newempl != None
            if (status == False):
                return False

        return True

    '''
    '''
    def get_managers(self):
        db_managers = UserEntity.query.filter_by(UserType=MANAGER).all()
        if (len(db_managers) == 0):
            return False, []

        managers = []
        for man in db_managers:
            manager = Manager(man.id, man.name, MANAGER, man.login)
            managers.append(manager)
        return True, managers

    '''
    '''
    def get_employees_by_manager(self, managerId):
        db_employees = EmployeeManagerEntity.query.filter_by(idManager=managerId).all()

        if (len(db_employees) == 0):
            return False, []

        emp_idxs = []
        for db_e in db_employees:
            emp_idxs.append(db_e.idEmpl)
        
        db_employees = UserEntity.query.filter(UserEntity.id.in_(emp_idxs)).all()        
        
        if (len(db_employees) == 0):
            return False, []
        
        employees = []
        for emp in db_employees:
            employee = Employee(emp.id, emp.name, EMPLOYEE, emp.login)
            employees.append(employee)
        
        return True, employees
    
    '''
    '''
    def add_task(self, employeeId, content, priority):
        emp_rec = UserEntity.query.filter_by(id=employeeId).first()
        if (emp_rec == None):
            return False
        
        newtask = TaskEntity(priority=priority, completed=False, mark_complete=False, content=content)
        DBTasker.session.add(newtask)
        DBTasker.session.flush()
        DBTasker.session.commit()
        
        newemptask = EmployeeTaskEntity(idEmployee=employeeId, idTask=newtask.id)
        DBTasker.session.add(newemptask)
        DBTasker.session.commit()
    
        return True
        
    '''
    '''
    def get_tasks(self, employeeId):
        db_task_idxs = EmployeeTaskEntity.query.filter_by(idEmployee=employeeId).all()
        if (len(db_task_idxs) == 0):
            return False, []

        task_idxs = []
        for db_e in db_task_idxs:
            task_idxs.append(db_e.idTask)

        db_tasks = TaskEntity.query.filter(TaskEntity.id.in_(task_idxs)).all()
        if (len(db_tasks) == 0):
            return False, []

        tasks = []
        for t in db_tasks:
            task = Task(t.id, t.content, t.priority, t.appDate)
            task.set_complete(t.completed)
            task.set_mark_complete(t.mark_complete)
            tasks.append(task)
        
        return True, tasks
    
    def set_task_flag(self, typeOp, taskId, flag):
        from task_service import MARK_OP
        if flag == 1: flag = True 
        else: flag = False

        task = TaskEntity.query.filter_by(id=taskId).first()
        if (task == None):
                return False
        
        if (typeOp == MARK_OP):
            task.mark_complete = flag
        else:
            task.completed = flag

        DBTasker.session.commit()

        return True
    
    def get_user_data_auth(self, login, password):
        rec = UserEntity.query.filter_by(login=login, password=password).first()

        if (rec == None):
            return False, None
    
        user = User(rec.id, rec.name, rec.UserType, rec.login)

        return True, user