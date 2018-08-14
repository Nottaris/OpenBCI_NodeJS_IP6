import React from "react";

export default class Timestamps extends React.Component {
    convertTime(timestamp) {
        let minutes = Math.floor(timestamp / 60);
        let seconds = timestamp - (minutes * 60);
        if (seconds < 10) {
            seconds = "0" + seconds;
        }
        timestamp = minutes + ":" + seconds;
        return timestamp;
    }

    render() {
        return (
            <div className="Timestamps">
                {this.convertTime(this.props.currentTime)} - {this.convertTime(this.props.duration)}
            </div>
        )
    }
};
