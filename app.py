import sys, getopt
from server_data import app, api, db_user, db_pass
from register_service import RegisterService, AuthorizationService
from user_service import UserEmployeeService, TaskEmployeeService
from task_service import AddTaskService, HandleTaskService


def server_init():
    api.add_resource(RegisterService, '/', '/register', endpoint='register')
    api.add_resource(UserEmployeeService, '/', '/employees', endpoint='employees')
    api.add_resource(AddTaskService, '/', '/task', endpoint='task')
    api.add_resource(TaskEmployeeService, '/', '/employee/task', endpoint='employee/task')
    api.add_resource(HandleTaskService, '/', '/employee/taskcheck', endpoint='employee/taskcheck')
    api.add_resource(AuthorizationService, '/', '/authorization', endpoint='authorization')
    return


def arg_parse(argv):
    global db_user, db_pass
    server_port = 5000
    server_address = '0.0.0.0'
    try:
      opts, args = getopt.getopt(argv,"ha:p:n:s:",["address=","port=","db_user=", "db_pass="])
    except getopt.GetoptError:
      print('app.py -a <address> -p <port> -n <db_user_name> -s <db_user_password>')
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('app.py -a <address> -p <port> -n <db_user_name> -s <db_user_password>')
            sys.exit()
        elif opt in ("-a", "--address"):
            server_address = arg
        elif opt in ("-p", "--port"):
            server_port = arg
        elif opt in ("-n", "--db_user"):
            db_user = arg
        elif opt in ("-s", "--db_pass"):
            db_pass = arg
    return server_address, server_port

if __name__ == '__main__':
    server_address, server_port = arg_parse(sys.argv[1:])
    server_init()
    app.run(host=server_address, port=server_port, debug=True)
    


