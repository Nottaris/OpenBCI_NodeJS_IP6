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
                    <h1 className="App-title">bci Music Player</h1>
                </header>
                <p className="App-intro">
                    To get started, setup your bci and do <code>npm run stream</code> and reload.
                </p>
                <Player/>
            </div>
        );
    }
}

export default App;
