from user import EMPLOYEE, MANAGER
from flask_restful import Resource, abort, reqparse
from user_repository import UserRepository

class RegisterService(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('login', type=str)
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('user_type', type=int)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('managerId', type=int)
        self.user_repo = UserRepository()
        return
        
    '''
    '''
    def check_condition(self, login, password, name, usertype, managerId):
        if (len(login) < 5):
            return False, "Can't register user. Login is small, please, enter 5 or more symbols"
        if (len(password) < 8):
            return False, "Can't register user. Password is small, please, enter 8 or more symbols"
        if (len(name) < 3):
            return False, "Can't register user. Name is small, please, enter 3 or more symbols"
        if (usertype != MANAGER and usertype != EMPLOYEE):
            return False, "Can't register user. Error user type"
        if (usertype == EMPLOYEE and managerId <= 0):
            return False, "Can't regiseter user. Error id manager"
        return True, ''

    '''
    '''
    def put(self):
        args = self.parser.parse_args()
        login = args['login']
        password = args['password']
        usertype = args['user_type']
        name = args['name']
        managerId = args['managerId']
        
        if (login == None or password == None or usertype == None or name == None or managerId == None):
            return {'stat': 'FAIL', 'message': 'Invalid getting data'}, 204

        succ, message = self.check_condition(login, password, name, usertype, managerId)
        if (succ == False):
            return {'stat': 'FAIL', 'message': message}, 204
        
    
        if usertype != EMPLOYEE:
            managerId = 0

        register_status = self.user_repo.register_user(login, password, name, usertype, managerId)
        if (register_status == False):    
            return {'stat': 'FAIL', 'message': "Can't register user with login={}".format(login)}, 204

        return {'stat': 'OK'}, 200

    '''
    '''
    def get(self):
        res, managers = self.user_repo.get_managers()
        if (res == False):
            return {'stat': 'FAIL', 'message': 'Error no managers in database'}, 204
        
        result = {}
        for i in range(len(managers)):
            result[i] = {'id': managers[i].get_id(), 'name': managers[i].get_name()}

        return result, 200 

        
class AuthorizationService(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('login', type=str)
        self.parser.add_argument('password', type=str)
        self.user_repo = UserRepository()
        return

    '''
    '''
    def check_condition(self, login, password):
        if (len(login) < 5):
            return False, "Can't define login user. Login is small, please, enter 5 or more symbols"
        if (len(password) < 8):
            return False, "Can't define password user. Password is small, please, enter 8 or more symbols"
        return True, ''

    '''
    '''
    def get(self):
        args = self.parser.parse_args()
        login = args['login']
        password = args['password']
        succ, message = self.check_condition(login, password)
        if (succ == False):
            return {'stat': 'FAIL', 'message': message}, 204

        succ, user = self.user_repo.get_user_data_auth(login, password)
        if (succ == False):
            return {'stat': 'FAIL', 'message': 'User not found'}, 203

        result = {'id': user.get_id(), 'name': user.get_name(), 
                  'user_type':user.get_user_type(), 'login':user.get_login()}

        return result, 200