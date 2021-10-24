from flask_restful import Resource, abort, reqparse
from user_repository import UserRepository



class UserEmployeeService(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('managerId', type=int)
        self.user_repo = UserRepository()
        return

    '''
    '''
    def get(self):
        args = self.parser.parse_args()
        managerId = args['managerId']
        if (managerId == None):
            return {'stat': 'FAIL', 'message': "Error: Parameter manager id is bad"}, 204

        if (managerId <= 0):
            return {'stat': 'FAIL', 'message': "Can't get employees for manager={}".format(managerId)}, 204

        res, employees = self.user_repo.get_employees_by_manager(managerId)

        if (res == False):
            return {'stat': 'FAIL', 'message': "Can't find employees for manager={}".format(managerId)}

        result = {}
        for i in range(len(employees)):
            result[i] = {'id': employees[i].get_id(), 'name': employees[i].get_name()}    

        return result, 200
    

class TaskEmployeeService(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('employeeId', type=int)
        self.user_repo = UserRepository()
    
    '''
    '''
    def get(self):
        args = self.parser.parse_args()
        employeeId = args['employeeId']

        if (employeeId <= 0):
            return {'stat' : 'FAIL', 'message': "Can't get tasks for employee ={}".format(employeeId)}, 204

        succ, tasks = self.user_repo.get_tasks(employeeId)
        if (succ == False):
            return {'stat' : 'FAIL', 'message': "Can't find tasks for employee={}".format(employeeId)}, 204

        result = {}
        for i in range(len(tasks)):
            result[i] = {'id' : tasks[i].get_id(),   
                         'content': tasks[i].get_content(), 
                         'priority' : tasks[i].get_priority(),
                         'date': tasks[i].get_timestamp().strftime("%d.%m.%Y, %H:%M:%S"),
                         'complete': tasks[i].get_completed(),
                         'mark_complete': tasks[i].get_mark_complete()}  
        
        return result, 200
    
