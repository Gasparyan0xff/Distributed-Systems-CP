
## enum
MANAGER = 1
EMPLOYEE = 2

###-------------------- User ----------------------
class User:
    def __init__(self, id, name, user_type, login):
        self.id = id
        self.name = name
        self.user_type = user_type
        self.login = login
    '''
    '''
    def get_id(self):
        return self.id

    '''
    '''
    def get_name(self):
        return self.name

    '''
    '''
    def get_user_type(self):
        return self.user_type

    '''
    '''    
    def get_login(self):
        return self.login

    '''
    '''
    def set_name(self, name):
        self.name = name

    '''
    '''
    def set_user_type(self, user_type):
        self.user_type = user_type



###-------------------- Employee ----------------------
class Employee(User):
    def __init__(self, id, name, user_type, login):
        User.__init__(self, id, name, user_type, login)
        self.tasks = []

    '''
    '''
    def get_list_tasks(self):
        return self.tasks

    '''
    '''
    def get_task(self, id):
        return self.tasks[id]

    '''
    '''
    def add_task(self, task):
        self.tasks.append(task)

    '''
    '''
    def set_mark_complete_task(self, id, completed):
        self.tasks[id].set_mark_complete(completed)
    


###-------------------- Manager ----------------------
class Manager(User):
    def __init__(self, id, name, user_type, login):
        User.__init__(self, id, name, user_type, login)
        self.employees = []

    '''
    '''
    def get_employee(self, id_emp):
        return self.employees[id_emp]

    '''
    '''
    def add_employee(self, employee):
        self.employees.append(employee)

    '''
    '''
    def check_task(self, id_emp, id_task, complete):
        employee = self.get_employee(id_emp)
        task = employee.get_task(id_task)
        task.set_complete(complete)

    '''
    '''
    def get_employees(self):
        return self.employees    
