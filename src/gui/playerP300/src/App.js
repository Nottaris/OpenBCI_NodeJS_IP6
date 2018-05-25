import React, {Component} from 'react';
import logo from './logo.png';
import Player from './Player';
import './App.css';

class App extends Component {
    render() {
        return (
            <div className="App">
                <header className="App-header">
                    <img src={logo} className="App-logo" alt="logo"/>
                    <h5 className="App-title">bci Music Player</h5>
                </header>
                <Player/>
            </div>
        );
    }
}

export default App;
