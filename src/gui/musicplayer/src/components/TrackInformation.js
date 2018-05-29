import React from 'react';

class TrackInformation extends React.Component {
    render() {
        return (
            <div className="TrackInformation">
                <div className="Name">{this.props.tracks[this.props.state.trackNr].name}</div>
                <div className="Artist">{this.props.tracks[this.props.state.trackNr].artist}</div>
                <div
                    className="Album">{this.props.tracks[this.props.state.trackNr].album} ({this.props.tracks[this.props.state.trackNr].year})
                </div>
            </div>
        )
    }
};

export default TrackInformation;