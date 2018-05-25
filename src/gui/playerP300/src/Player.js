import React from 'react';
import './Player.css';
import mp3File_summer from './music/bensound-summer.mp3';
import mp3File_anewbeginning from './music/bensound-anewbeginning.mp3';
import mp3File_happyrock from './music/bensound-happyrock.mp3';

// Player
class Player extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            playStatus: 'play',
            currentTime: 0,
            trackNr: 0
        };
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
            case "next":
                this.next(audio);
                break;
            case "previous":
                this.previous(audio);
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
        audio.play();
        let that = this;
        let duration = that.props.tracks[this.state.trackNr].duration;
        setInterval(function() {
            let currentTime = audio.currentTime;
            // Calculate percent of song
            let percent = (currentTime / duration) * 100 + '%';
            that.updateScrubber(percent);
            that.updateTime(currentTime);
        }, 100);
        this.setState({ playStatus: 'pause' });
    }

    pause(audio) {
        audio.pause();
        this.setState({ playStatus: 'play' });
    }
    next(audio) {
        this.setState({ trackNr: this.mod((this.state.trackNr + 1), this.props.tracks.length)});
        audio = document.getElementById('audio');
        //load new audio file
        audio.load();
        this.play(audio);
    }
    previous(audio) {
        this.setState({ trackNr: this.mod((this.state.trackNr - 1), this.props.tracks.length)});
        audio = document.getElementById('audio');
        //load new audio file
        audio.load();
        this.play(audio);
    }

    // Help function: Modulo operation with negative numbers
    mod(a, n) {
        return a - (n * Math.floor(a/n));
    }

    render() {
        return (
            <div className="Player">
                <div className="Info">
                    <div className="PlayerCover">
                        <div className="Artwork" style={{'backgroundImage': 'url(' + this.props.tracks[this.state.trackNr].artwork + ')'}}></div>
                    </div>
                    <div className="PlayerInformation">
                        <TrackInformation tracks={this.props.tracks} state={this.state}/>
                        <Scrubber />
                    </div>
                    <div className="PlayerScrubber">
                        <Timestamps duration={this.props.tracks[this.state.trackNr].duration} currentTime={this.state.currentTime} />
                        <audio id="audio">
                            <source src={this.props.tracks[this.state.trackNr].source}  type="audio/mpeg"/>

                        </audio>
                    </div>

                </div>
                <Controls newCommand={this.newCommand}/>
            </div>

        )
    }
};

class TrackInformation extends React.Component {
    render() {
        return (
            <div className="TrackInformation">
                <div className="Name">{this.props.tracks[this.props.state.trackNr].name}</div>
                <div className="Artist">{this.props.tracks[this.props.state.trackNr].artist}</div>
                <div className="Album">{this.props.tracks[this.props.state.trackNr].album} ({this.props.tracks[this.props.state.trackNr].year})</div>
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
               {this.convertTime(this.props.currentTime)} - {this.convertTime(this.props.duration)}
            </div>
        )
    }
};

class Controls extends React.Component {
    constructor(props) {
        super(props);
        this.setCommand = this.setCommand.bind(this);
    }
    setCommand(status){
        this.props.newCommand(status);
    }

    render() {
        return (
            <div className="Controls">
                <div className="row">
                    <div onClick={() => this.setCommand('previous')} className="Button">
                        <i className='fa fa-fw fa-backward'></i>
                    </div>
                    <div onClick={() => this.setCommand('play')} className="Button">
                        <i className='fa fa-fw fa-play'></i>
                    </div>
                    <div onClick={() => this.setCommand('next')} className="Button">
                        <i className='fa fa-fw fa-forward'></i>
                    </div>
                </div>
                <div className="row">
                    <div onClick={() => this.setCommand('down')} className="Button">
                        <i className='fa fa-fw fa-volume-down'></i>
                    </div>
                    <div onClick={() => this.setCommand('pause')} className="Button">
                        <i className='fa fa-fw fa-pause'></i>
                    </div>
                    <div onClick={() => this.setCommand('up')} className="Button">
                        <i className='fa fa-fw fa-volume-up'></i>
                    </div>
                </div>
            </div>
        )
    }
}

Player.defaultProps = {
    tracks:[{
        name: "We Were Young",
        artist: "Odesza",
        album: "Summer's Gone",
        year: 2012,
        artwork: "https://funkadelphia.files.wordpress.com/2012/09/odesza-summers-gone-lp.jpg",
        duration: 192,
        source: "https://s3-us-west-2.amazonaws.com/s.cdpn.io/557257/wwy.mp3"
    },
        {
            name: "Summer",
            artist: "Bensound",
            album: "Summer's Gone",
            year: 2013,
            artwork: "https://www.bensound.com/bensound-img/summer.jpg",
            duration: 192,
            source: mp3File_summer
        },
        {
            name: "A New Beginning",
            artist: "Bensound",
            album: "Summer's Gone",
            year: 2014,
            artwork: "https://www.bensound.com/bensound-img/anewbeginning.jpg",
            duration: 192,
            source: mp3File_anewbeginning
        },
        {
            name: "Happy Rock",
            artist: "Bensound",
            album: "Summer's Gone",
            year: 2015,
            artwork: "https://www.bensound.com/bensound-img/happyrock.jpg",
            duration: 192,
            source: mp3File_happyrock
        }
    ]
};

export default Player;