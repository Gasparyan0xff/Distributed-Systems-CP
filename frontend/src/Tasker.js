import React, { Component } from 'react';
import axios from 'axios';
import {Card} from "react-bootstrap";

const employees_route = '/employees';
const add_task_route = '/task';
const employee_task_route = '/employee/task';
const task_checker_route = '/employee/taskcheck';

const MANAGER = 1;
const EMPLOYEE = 2;
const MARK_OP = 1;
const CHECK_OP = 2;
const MAX_PRIORITY = 8;

function get_employee_list(obj, req_str, managerId) {
    axios.get(req_str, {params: {managerId: managerId}})
        .then(response => {
            if (response.status === 200){
                let temp = []; const objects = response.data;
                for(let i=0; i<Object.keys(objects).length; i++){
                    temp.push(response.data[i]);
                }
                obj.setState({employee_list : temp});
            } else {console.log(response.data.message);}
        }).catch(error => console.log(error))
}

function put_task_employee(req_str, emp_id, content, priority){
    const data = {
        employeeId: emp_id,
        content: content,
        priority : priority
    }
    axios.put(req_str, data)
        .then(function (response) {
            if (response.status === 203){
                alert('Ошибика добавления задачи ' + response.data.message);
            } else {
                alert('Задача успешно добавлена!')
            }
        })
        .catch(error => alert('Ошибка добавления задачи на сервере : ' + error))
}

function check_task(req_str, task_id, flag) {
    const data = {
        typeOp: CHECK_OP,
        taskId: task_id,
        flag : flag
    }
    axios.put(req_str, data)
        .then(function (response) {
            if (response.status === 203){
                alert('Ошибика подтверждения задачи ' + response.data.message);
            } else {
                if (flag)
                    alert('Выполнение задачи подтверждено!')
                else
                    alert('Подтверждение отменено');
            }
        })
        .catch(error => alert('Ошибка подтверждения задачи на сервере : ' + error))
}

function mark_task(req_str, task_id, flag) {
    const data = {
        typeOp: MARK_OP,
        taskId: task_id,
        flag : flag
    }
    axios.put(req_str, data)
        .then(function (response) {
            if (response.status === 203){
                alert('Ошибка отметки задачи ' + response.data.message);
            } else {
                if (flag)
                    alert('Задача помечена, что выполнена!')
                else
                    alert('Отметка убрана');
            }
        })
        .catch(error => alert('Ошибка подтверждения задачи на сервере : ' + error))
}


function get_list_tasks(obj, req_str, employeeId) {
    axios.get(req_str, { params: { employeeId: employeeId}}).then(response =>  {
        if (response.status === 200){
            let temp = [];
            for(let i=0; i<Object.keys(response.data).length; i++){
                temp.push(response.data[i]);
            }
            obj.setState({task_list: temp})
        } else {console.log(response.data.message);}
    }).catch(error => console.log(error))
}

//====================================================================
class Tasks extends Component {
    constructor(props) {
        super(props);
        const employeeId = props.parent.state.empId;
        const empName = props.parent.state.empName;
        this.user_type = sessionStorage.getItem('userType');
        this.user_type = Number(this.user_type);
        const isManager = this.user_type === MANAGER;
        this.content = '';
        this.priority = 1;

        this.state = {
            parent_obj: props.parent,
            employeeId: employeeId,
            employee_name: empName,
            isManager: isManager,
            task_list: []
        };
        this.returnUser = this.returnUser.bind(this);
        this.addTaskToEmployee = this.addTaskToEmployee.bind(this);
        this.checkTask = this.checkTask.bind(this);
        this.markTask = this.markTask.bind(this);
    }

    getTasksEmployee() {
        try {
            get_list_tasks(this, employee_task_route, this.state.employeeId);
        } catch (e) {console.log(e)}
    }

    componentDidMount() {
        this.getTasksEmployee = this.getTasksEmployee.bind(this);
        this.getTasksEmployee();
    }

    returnUser() {
        try {
            this.state.parent_obj.setState({showTasks: false});
        } catch (e) {console.log(e)}
    }

    getListPriority(){
        let pri_list = [];
        for (let i = 1; i < MAX_PRIORITY; ++i){
            pri_list.push(<option key={i} id={i}>{i}</option>)
        }
        return pri_list;
    }

    addTaskToEmployee() {
        const empId = this.state.employeeId;
        const content = this.content;
        const priority = this.priority;
        try {
            put_task_employee(add_task_route, empId, content, priority);
        } catch (e) {console.log(e)}
    }

    checkTask(event) {
        const taskId = event.target.id;
        const flag = event.target.checked;
        try {
            check_task(task_checker_route, taskId, flag);
        } catch (e) {console.log(e)}
    }

    markTask(event) {
        const taskId = event.target.id;
        const flag = event.target.checked;
        try {
            mark_task(task_checker_route, taskId, flag);
        } catch (e) {console.log(e)}
    }

    render() {
        if (this.state.task_list.length > 0) {
            this.tasks = this.state.task_list.map((task) => {
                return <Card key={task.id} style={{ width: '18rem' }} className="CardTasks">
                        <Card.Header>Задача №{task.id}</Card.Header>
                        <Card.Title>Содержимое:</Card.Title>
                        <Card.Text >{task.content}</Card.Text>
                        <Card.Title>Дата получения</Card.Title>
                        <Card.Text >{task.date}</Card.Text>
                        <Card.Title>Приоритет: {task.priority}</Card.Title>
                        <div>
                            <label >Задача выполнена</label>
                            <input id={task.id} type="checkbox" defaultChecked={task.mark_complete}
                                   disabled={this.state.isManager} onChange={this.markTask}></input>
                        </div>
                        <div>
                            <label>Подтвердить выполнение</label>
                            <input id={task.id} type="checkbox" defaultChecked={task.complete}
                                   disabled={!this.state.isManager} onChange={this.checkTask}></input>
                        </div>
                </Card>

            })
        } else {
            this.tasks = <div></div>
        }

        return(
            <div>
                <div><header>Задачи: {this.state.employee_name}</header></div>
                <div>
                    {this.state.isManager ?
                        <div>
                            <textarea onChange={(e) => {this.content = e.target.value}}></textarea>
                            <select defaultValue={1} onChange={(e) => this.priority = e.target.value}>
                                {this.getListPriority()}
                            </select>
                            <button onClick={this.addTaskToEmployee}>Добавить задачу</button>
                        </div> : <div>Задач пока нет...</div>}
                </div>

                <div>
                    {this.tasks}
                </div>
                {this.state.isManager ? <div><button onClick={this.returnUser}>Назад</button></div> : <div/>}
            </div>
        );
    }
}


//=======================================================================
class Manager extends Component {
    constructor(props) {
        super(props);
        this.user_type = sessionStorage.getItem('userType');
        const userId =  sessionStorage.getItem('userId');
        this.user_type = Number(this.user_type);

        this.state = {
            userId: userId,
            empId: 0,
            empName: '',
            employee_list: [],
            task_list: [],
            showTasks: false
        };
    }

    componentDidMount() {
        this.getUserInfo = this.getUserInfo.bind(this);
        this.getUserInfo();
    }

    getUserInfo() {
        const userId = this.state.userId;
        try {
            get_employee_list(this, employees_route, userId);
        } catch (e) {console.log(e);}
    }


    render() {
        if (this.state.employee_list.length > 0){
            this.employee_buttons = this.state.employee_list.map(emp => {
                    return <div key={emp.id}>
                        <button id={emp.id} onClick={(e) =>{
                                this.setState({empId: e.target.id});
                                this.setState({empName: emp.name});
                                this.setState({showTasks: true});
                            }
                        }>

                        №{emp.id} имя:{emp.name}</button>
                    </div>
                })
        } else {
            this.employee_buttons = <div></div>
        }

        return (
            <div>
                <div>
                    {this.state.showTasks ? <Tasks parent={this}/> : this.employee_buttons}
                </div>
            </div>

        );
    }
}

//=======================================================================
class Employee extends Component {
    constructor(props) {
        super(props);
        this.user_type = sessionStorage.getItem('userType');
        const userId =  sessionStorage.getItem('userId');
        this.user_type = Number(this.user_type);

        this.state = {
            empId: userId,
        };
    }

    render() {
        return (
            <div>
                <Tasks parent={this}/>
            </div>
        );
    }
}


//====================================================================
class Tasker extends Component {
    constructor(props) {
        super(props);
        this.user_type = sessionStorage.getItem('userType');
        const userId =  sessionStorage.getItem('userId');
        const name = sessionStorage.getItem('userName');
        if (this.user_type === null){
            alert('Ошибка авторизации');
        }
        this.user_type = Number(this.user_type);
        if (this.user_type < MANAGER || this.user_type > EMPLOYEE ){
            alert('Ошибка авторизации');
        }

        const isManager = this.user_type === MANAGER;
        this.state = {
                        name: name,
                        userId: userId,
                        managerShow: isManager ? true : false
                     };
        this.logOutSystem = this.logOutSystem.bind(this);
    }

    logOutSystem(){
        try {
            sessionStorage.setItem('login', null);
            sessionStorage.setItem('userId', null);
            sessionStorage.setItem('userType', null);
            sessionStorage.setItem('userName', null);
            setTimeout(() => {
                document.location.reload();
            }, 750);
        } catch (e) {console.log(e)}

    }

    render() {
            return(
                <div className='Tasker'>
                    <div>
                        <header className="Tasker-header" />
                        <header>
                            Добрый день: {this.state.name}
                        </header>
                    </div>
                    <div>
                        {this.state.managerShow ? <Manager/> : <Employee />}
                    </div>

                    <div>
                        <button onClick={this.logOutSystem}>Выйти</button>
                    </div>
                </div>


            );
        }
}

export default Tasker;
