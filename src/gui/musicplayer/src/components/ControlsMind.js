import React from "react";

export default class Controls extends React.Component {
    constructor(props) {
        super(props);
        this.setCommand = this.setCommand.bind(this);
    }

    setCommand(status) {
        this.props.clickCommand(status);
    }

    render() {
        return (
            <div className="Controls">
                <div className="row">
                    <div onClick={() => this.setCommand('voldown')} id="voldown" className="Button">
                        <i className='cmd fa fa-fw fa-volume-down'></i>
                    </div>
                    <div onClick={() => this.setCommand('prev')} id="prev" className="Button">
                        <i className='cmd fa fa-fw fa-backward'></i>
                    </div>
                    <div onClick={() => this.setCommand('playpause')} id="playpause" className="Button">
                        <i className={"cmd fa fa-fw fa-" + this.props.playpauseToggle}></i>
                    </div>
                    <div onClick={() => this.setCommand('next')} id="next" className="Button">
                        <i className='cmd fa fa-fw fa-forward'></i>
                    </div>
                    <div onClick={() => this.setCommand('volup')} id="volup" className="Button">
                        <i className='cmd fa fa-fw fa-volume-up'></i>
                    </div>
                </div>
            </div>
        )
    }
}
