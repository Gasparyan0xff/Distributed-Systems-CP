import React, { Component } from 'react';
import Authorization from './Authorization';
import Tasker from './Tasker';

class App extends Component{
	constructor(props) {
		super(props);
		this.state = {
						TaskerShow: false
					 };
		try {
			const userId = sessionStorage.getItem('userId');
			if (userId !== null && userId > 0) {
				this.state.TaskerShow = true;
			} else {
				this.state.TaskerShow = false;
			}
		} catch (e) {
			console.log(e)
		}

	}


	render(){
		return (
			<div className='App'>
				<div>
					<header className="App-header">
					</header>
				</div>
				<div>
					{
						this.state.TaskerShow ? <Tasker/> : <Authorization />
					}

				</div>
			</div>
		);
	}

}

export default App;
