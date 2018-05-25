import React from 'react';
import './Player.css';

// Player
class Player extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            playStatus: 'play',
            currentTime: 0
        };
        this.play = this.play.bind(this);
        this.pause = this.pause.bind(this);
        this.newCommand = this.newCommand.bind(this);
    };


    newCommand = (state) => {
        let audio = document.getElementById('audio');
        switch(state) {
            case "play":
                this.play(audio);
                break;
            case "pause":
                this.pause(audio);
                break;
        }

    }

    updateTime(timestamp) {
        timestamp = Math.floor(timestamp);
        this.setState({ currentTime: timestamp });
    }
    updateScrubber(percent) {
        // Set scrubber width
        let innerScrubber = document.querySelector('.Scrubber-Progress');
        innerScrubber.style['width'] = percent;
    }

    play(audio){
        console.log("play");
        audio.play();
        let that = this;
        setInterval(function() {
            let currentTime = audio.currentTime;
            let duration = that.props.track.duration;

            // Calculate percent of song
            let percent = (currentTime / duration) * 100 + '%';
            that.updateScrubber(percent);
            that.updateTime(currentTime);
        }, 100);
        this.setState({ playStatus: 'pause' });
    }

    pause(audio) {
        console.log("pause");
        audio.pause();
        this.setState({ playStatus: 'play' });
    }
    next(audio) {
        console.log("next");
        audio.next();
    }
    previous(audio) {
        console.log("next previous");
        audio.next();
    }


    render() {
        return (
            <div className="Player">
                <div>
                    <div className="PlayerCover">
                        <div className="Artwork" style={{'backgroundImage': 'url(' + this.props.track.artwork + ')'}}></div>
                    </div>
                    <div className="PlayerInformation">
                        <TrackInformation track={this.props.track} />
                        <Scrubber />
                    </div>
                    <div className="PlayerScrubber">
                        <Timestamps duration={this.props.track.duration} currentTime={this.state.currentTime} />
                        <audio id="audio">
                            <source src={this.props.track.source} />
                            <source src={this.props.track.source} />
                            <source src={this.props.track.source} />
                        </audio>
                    </div>
                </div>
                <Controls newCommand={this.newCommand}/>
            </div>

        )
    }
};

Player.defaultProps = {
    track: {
        name: "We Were Young",
        artist: "Odesza",
        album: "Summer's Gone",
        year: 2012,
        artwork: "https://funkadelphia.files.wordpress.com/2012/09/odesza-summers-gone-lp.jpg",
        duration: 192,
        source: "https://s3-us-west-2.amazonaws.com/s.cdpn.io/557257/wwy.mp3"
    }
};


class TrackInformation extends React.Component {
    render() {
        return (
            <div className="TrackInformation">
                <div className="Name">{this.props.track.name}</div>
                <div className="Artist">{this.props.track.artist}</div>
                <div className="Album">{this.props.track.album} ({this.props.track.year})</div>
            </div>
        )
    }
};

class Scrubber extends React.Component {
    render() {
        return (
            <div className="Scrubber">
                <div className="Scrubber-Progress"></div>
            </div>
        )
    }
};


class Timestamps extends React.Component {
    convertTime(timestamp) {
        let minutes = Math.floor(timestamp / 60);
        let seconds = timestamp - (minutes * 60);
        if(seconds < 10) {
            seconds = '0' + seconds;
        }
        timestamp = minutes + ':' + seconds;
        return timestamp;
    }

    render() {
        return (
            <div className="Timestamps">
               {this.convertTime(this.props.currentTime)} -{this.convertTime(this.props.duration)}
            </div>
        )
    }
};

class Controls extends React.Component {
    constructor(props) {
        super(props);
        this.play = this.play.bind(this);
        this.pause = this.pause.bind(this);
        console.log(props);
    }
    play(){
        this.props.newCommand('play');
    }

    pause(){
        this.props.newCommand('pause');
     }

    next(){
        this.props.newCommand('next');
    }
    previous(){
        this.props.newCommand('previous');
    }
    down(){
        this.props.newCommand('previous');
    }
    up(){
        this.props.newCommand('previous');
    }
    render() {

        let classNames;

        return (
            <div className="Controls">
                <table>
                    <tr>
                        <td>
                            <div onClick={this.play} className="Button">
                                <i className='fa fa-fw fa-play'></i>
                            </div>
                        </td>
                        <td>
                            <div onClick={this.previous} className="Button">
                                <i className='fa fa-fw fa-backward'></i>
                            </div>
                        </td>
                        <td>
                            <div onClick={this.next} className="Button">
                                <i className='fa fa-fw fa-forward'></i>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div onClick={this.pause} className="Button">
                                <i className='fa fa-fw fa-pause'></i>
                            </div>
                        </td>
                        <td>
                            <div onClick={this.up} className="Button">
                                <i className='fa fa-fw fa-volume-up'></i>
                            </div>
                        </td>
                        <td>
                            <div onClick={this.down} className="Button">
                                <i className='fa fa-fw fa-volume-down'></i>
                            </div>
                        </td>
                    </tr>
                </table>

            </div>
        )
    }
}
export default Player;