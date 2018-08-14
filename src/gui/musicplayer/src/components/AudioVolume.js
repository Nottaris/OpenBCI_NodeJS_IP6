import React from "react";

export default class AudioVolume extends React.Component {
    render() {
        return (
            <div className="AudioProgress">
                <div className="Icon">
                    <i className="fa fa-fw fa-volume-up"></i>
                </div>
                <div className="AudioProgressBar">
                    <div className="ProgressBackground">
                        <div id="ProgressVolume"></div>
                    </div>
                </div>
            </div>
        )
    }
}