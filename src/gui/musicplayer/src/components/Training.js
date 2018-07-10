import React from "react";

export default class Training extends React.Component {
    constructor(props) {
        super(props);
        this.trainingInit = this.trainingInit.bind(this);
    }

    trainingInit() {
        this.props.trainingInit();
    }

    render() {
        return (
            <div className="Controls">
                <div className="row">
                    <div onClick={() => this.trainingInit()} id="training" className="Button">
                        <i className='fa fa-fw fa-graduation-cap'></i>
                        <div id="progress">
                            <div id="progressBar"></div>
                        </div>
                        <p id="infotext" className="infotext">Start training phase</p>
                    </div>
                </div>
            </div>
        )
    }
}
