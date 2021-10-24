import React, {Component} from "react";
import axios from "axios";

const auth_route = '/authorization';
const register_route = '/register';

const MANAGER = 1;
const EMPLOYEE = 2;

function auth(req_str, login, password) {
    axios.get(req_str, {
        params: {
            login: login,
            password: password
        }
        })
        .then(response => {
            const resp_data = response.data;
            if (resp_data.stat === 'FAIL'){
                alert('Ошибка авторизации ' + resp_data.message);
            } else {
                sessionStorage.setItem('login', resp_data.login);
                sessionStorage.setItem('userId', resp_data.id);
                sessionStorage.setItem('userType', resp_data.user_type);
                sessionStorage.setItem('userName', resp_data.name);
            }
        })
        .catch(error =>  alert('Ошибка авторизации: ' + error))
}

function register(req_str, login, password, name, user_type, manager_id) {
    const data = {
        login: login,
        password: password,
        user_type : user_type,
        name: name,
        managerId: manager_id
    }
    axios.put(req_str, data)
        .then(function (response) {
            if (response.status === 204){
                alert('Ошибка регистрации пользователя!');
            } else {
                alert(`Пользователь ${login} успешно зарегистрирован!`)
            }
        })
        .catch(error => alert('Ошибка регистрации: ' + error))
}

function get_list_of_managers(obj, req_str) {
    axios.get(req_str)
        .then(response => {
            if (response.status === 200){
                const resp_data = response.data;
                let temp = [];
                for(let i=0; i<Object.keys(resp_data).length; i++){
                    temp.push(response.data[i]);
                }
                obj.manager_list = temp;
            } else {
                alert(response.data.message);
            }
        })
        .catch(error => console.log(error))
}

class Authorization extends Component{
    constructor(props) {
        super(props);
        try{
            this.state = {
                user_type: MANAGER,
                isAuth : true
            };
            this.Login = '';
            this.Password = '';
            this.Name = '';
            this.manager_list = [];
            this.managerId = 0;
            this.handleInputLogin = this.handleInputLogin.bind(this);
            this.handleInputPassword = this.handleInputPassword.bind(this);
            this.handleAuthUser = this.handleAuthUser.bind(this);
            this.handleInputName = this.handleInputName.bind(this);
            this.handleRegisterUser = this.handleRegisterUser.bind(this);
        } catch (e) {

        }
        try{
            get_list_of_managers(this, register_route)
        } catch (e) {
            console.log(e);
        }
    }

    handleAuthUser(event){
        try {
            auth(auth_route, this.Login, this.Password);
            setTimeout(() => {
                document.location.reload();
            }, 750);

        } catch (e) {console.log(e);}
    }

    handleRegisterUser(event){
        try {
            register(register_route, this.Login, this.Password,
                this.Name, this.state.user_type, this.managerId);
        } catch (e) {console.log(e);}
    }

    handleInputPassword(event){
        try { this.Password = event.target.value;
        } catch (e) { console.log(e);}
    }

    handleInputLogin(event){
        try { this.Login = event.target.value;
        } catch (e) {console.log(e);}
    }

    handleInputName(event){
        try {this.Name = event.target.value;}
        catch (e) {console.log(e);}
    }


    render(){
        if (this.manager_list.length > 0 && this.state.user_type === EMPLOYEE){
            this.managerId = this.manager_list[0].id;
            this.man_selector = <select defaultValue={this.manager_list[0].id}
                                        onChange={(e) => this.managerId = Number(e.target.value)}>
                {this.manager_list.map(obj => {return <option key={obj.id} value={obj.id}>{obj.name}</option>} ) }
            </select>
        } else {
            this.man_selector = <div></div>
        }


        if (this.state.isAuth){
            return (
                <div>
                    <header>
                        Авторизация:
                    </header>
                    <label>
                        Логин:
                        <input type="text" name="login" defaultValue={this.Login}
                               onChange={this.handleInputLogin}
                        />
                    </label>
                    <label>
                        Пароль:
                        <input type="password" name="password" defaultValue=""
                                onChange={this.handleInputPassword}
                        />
                    </label>
                    <div>
                        <button onClick={this.handleAuthUser}>Войти</button>
                    </div>
                    <div>
                        <button onClick={() => this.setState({isAuth : false})}>Регистрация</button>
                    </div>

                </div>
            );
        } else {
            return (
                <div>
                    <header>
                        Регистрация:
                    </header>
                    <div>
                        <label>
                            Логин:
                            <input type="text" name="login" defaultValue=""
                                   onChange={this.handleInputLogin} />
                        </label>
                        <label>
                            Пароль:
                            <input type="password" name="password" defaultValue=""
                                    onChange={this.handleInputPassword}/>
                        </label>
                        <label>
                            Имя:
                            <input type="text" name="name" defaultValue=""
                                    onChange={this.handleInputName}/>
                        </label>
                        <select defaultValue={MANAGER} onChange={event => this.setState({user_type : Number(event.target.value)})}>
                            <option key={MANAGER} value={MANAGER}>Менеджер</option>
                            <option key={EMPLOYEE} value={EMPLOYEE}>Работник</option>
                        </select>
                        <div>
                            {this.man_selector}
                        </div>
                        <div>
                            <button onClick={this.handleRegisterUser}>Зарегистрироваться</button>
                        </div>
                        <div>
                            <button onClick={() => this.setState({isAuth : true})}>Авторизация</button>
                        </div>
                    </div>
                </div>
            );
        }
    }
}
export default Authorization;
