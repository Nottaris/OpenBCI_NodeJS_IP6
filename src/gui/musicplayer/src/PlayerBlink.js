import React from 'react';
import './Player.css';
import {subscribeToBlinkCmds} from './api';
import TrackInformation from './components/TrackInformation';
import Timestamps from './components/Timestamps';
import AudioVolume from './components/AudioVolume';
import Controls from './components/Controls';

// Player
export default class PlayerBlink extends React.Component {
    constructor(props) {
        super(props);
        console.log(props);
        this.state = {
            playStatus: 'play',
            currentTime: 0,
            audioVolume: 0.5,
            trackNr: 0,
            currentCmd: 'no'
        };

        this.clickCommand = this.clickCommand.bind(this);
        this.flashCommand = this.flashCommand.bind(this);
        this.execCommand = this.execCommand.bind(this);


        subscribeToBlinkCmds(
            this.flashCommand,
            this.execCommand
        );

    };

    componentWillUnmount() {
        if (this.state.playpauseToggle === 'play') {
            let audio = document.getElementById('audio');
            this.pause(audio);
        }
    }


    flashCommand = (data) => {
        this.setState({currentCmd: data.command});
        this.blinkCommandButton(data.command);
    }

    execCommand = () => {
        console.log("exec: " + this.state.currentCmd);
        this.clickCommand(this.state.currentCmd);
        let elem = document.getElementById(this.state.currentCmd).getElementsByClassName('fa')[0];
        elem.style.color = "green";
    }

    //Set the color of the command to white for X seconds
    blinkCommandButton(command) {
        if (null !== command) {
            let elem = document.getElementById(command).getElementsByClassName('fa')[0];
            elem.style.color = "#ffffff";
            setTimeout(function () {
                elem.style.color = "#1c456e";
            }, 1000);
        }
    }

    clickCommand = (state) => {
        let audio = document.getElementById('audio');
        switch (state) {
            case "play":
                this.play(audio);
                break;
            case "pause":
                this.pause(audio);
                break;
            case "next":
                this.next(audio);
                break;
            case "prev":
                this.prev(audio);
                break;
            case "volup":
                this.volup(audio);
                break;
            case "voldown":
                this.voldown(audio);
                break;
            default:
                //this should never happen
                console.log("Error: clickCommand had unknown state")
                break;
        }

    }

    updateTime(timestamp) {
        timestamp = Math.floor(timestamp);
        this.setState({currentTime: timestamp});
    }

    updateVolumeProgressBar(volume) {
        var elem = document.getElementById("ProgressVolume");
        elem.style.width = 100 * volume + "%";
    }

    play(audio) {
        audio.play();
        audio.volume = this.state.audioVolume;
        let that = this;
        setInterval(function () {
            let currentTime = audio.currentTime;
            // Calculate percent of song
            that.updateTime(currentTime);
        }, 200);
        this.setState({playpauseToggle: 'pause'});
    }

    pause(audio) {
        audio.pause();
        this.setState({playpauseToggle: 'play'});
    }

    next(audio) {
        this.setState({trackNr: this.mod((this.state.trackNr + 1), this.props.tracks.length)});
        audio = document.getElementById('audio');
        //load new audio file
        audio.load();
        this.play(audio);
    }

    prev(audio) {
        this.setState({trackNr: this.mod((this.state.trackNr - 1), this.props.tracks.length)});
        audio = document.getElementById('audio');
        //load new audio file
        audio.load();
        this.play(audio);
    }

    volup(audio) {
        if (this.state.audioVolume < 0.8) {
            let newVol = this.state.audioVolume + 0.25;
            this.setState({audioVolume: newVol});
            audio.volume = newVol;
            this.updateVolumeProgressBar(newVol);
        }
    }

    voldown(audio) {
        if (this.state.audioVolume > 0.2) {
            let newVol = this.state.audioVolume - 0.25;
            this.setState({audioVolume: newVol});
            audio.volume = newVol;
            this.updateVolumeProgressBar(newVol);
        }
    }

    // Help function: Modulo operation with negative numbers
    mod(a, n) {
        return a - (n * Math.floor(a / n));
    }

    render() {
        return (
            <div className="Player Blink">
                <div className="Info">
                    <div className="PlayerCover">
                        <div className="Artwork"
                             style={{'backgroundImage': 'url(' + this.props.tracks[this.state.trackNr].artwork + ')'}}></div>
                    </div>
                    <div className="PlayerInformation">
                        <TrackInformation tracks={this.props.tracks} state={this.state}/>
                    </div>
                    <div className="PlayerScrubber">
                        <Timestamps duration={this.props.tracks[this.state.trackNr].duration}
                                    currentTime={this.state.currentTime}/>
                        <AudioVolume volume={this.state.audioVolume}/>
                        <audio id="audio">
                            <source src={this.props.tracks[this.state.trackNr].source} type="audio/mpeg"/>
                        </audio>
                    </div>

                </div>
                <Controls clickCommand={this.clickCommand}/>
            </div>

        )
    }
};
