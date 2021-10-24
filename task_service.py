from task import MAX_PRIORITY
from flask_restful import Resource, abort, reqparse
from user_repository import UserRepository

MARK_OP = 1
CHECK_OP = 2


class AddTaskService(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('employeeId', type=int)
        self.parser.add_argument('content', type=str)
        self.parser.add_argument('priority', type=int)
        self.user_repo = UserRepository()

    '''
    '''
    def check_content(self, employeeId, content, priority):
        if (employeeId <= 0):
            return False, "Can't add task. Employee doesn't exist"
        if (len(content) < 8):
            return False, "Can't add task. Content of task is small, please, enter more than 16 symbols"
        if (priority <= 0 or priority > MAX_PRIORITY):
            return False, "Can't add task. This priotity value is not allowed"
        return True, ''

    '''
    '''
    def put(self):
        args = self.parser.parse_args()
        employeeId = args['employeeId']
        content = args['content']
        priority = args['priority']
        
        if (employeeId == None or content == None or priority == None):
        	return {'stat': 'FAIL', 'message': 'Error! Invalid arguments'}, 203
        	

        succ, message = self.check_content(employeeId, content, priority)
        if (succ == False):
        	return {'stat': 'FAIL', 'message': message}, 203
       

        succ = self.user_repo.add_task(employeeId, content, priority)
        if (succ == False):
        	return {'stat': 'FAIL', 'message': 'Error! Cannot add task to this employee'}, 203
        

        return {'stat': 'OK'}, 200
    

class HandleTaskService(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('typeOp', type=int)
        self.parser.add_argument('taskId', type=int)
        self.parser.add_argument('flag', type=int)
        self.user_repo = UserRepository()  

    '''
    '''
    def check_content(self, typeOp, taskId):
        if (taskId <= 0):
            return False, "Can't perfom operation with task. Task id error"
        if (typeOp != MARK_OP and typeOp != CHECK_OP):
            return False, "Can't perfom operation with task. Type operation error"
        return True, ''

    '''
    '''
    def put(self):
        args = self.parser.parse_args()
        typeOp = args['typeOp']
        taskId = args['taskId']
        flag = args['flag']
        
        if (typeOp == None or taskId == None or flag == None):
        	return {'stat': 'FAIL', 'message': 'Error! Invalid arguments'}, 203
        
        succ, message = self.check_content(typeOp, taskId)
        if (succ == False):
        	return {'stat': 'FAIL', 'message': message}, 203
            

        succ = self.user_repo.set_task_flag(typeOp, taskId, flag)
        if (succ == False):
        	return {'stat': 'FAIL', 'message': 'Error! Cannot check task for this user'}, 203
            

        return {'stat': 'OK'}, 200   

