import React from 'react';
import './playToggle.css';

class playToggle extends React.Component {
    constructor(props) {
        super(props);
        this.state = {isToggleOn: true};

        // This binding is necessary to make `this` work in the callback
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick() {
        this.setState(prevState => ({
            isToggleOn: !prevState.isToggleOn
        }));
    }

    render() {
        return (
                <button onClick={this.handleClick}>
                    {this.state.isToggleOn ? 'Play' : 'Pause'}
                </button>
        );
    }
}

export default playToggle;