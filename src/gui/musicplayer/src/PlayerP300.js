import React from 'react';
import './Player.css';
import {subscribeToCmds, sendP300Cmd} from './api';
import TrackInformation from './components/TrackInformation';
import Scrubber from './components/Scrubber';
import Timestamps from './components/Timestamps';
import AudioVolume from './components/AudioVolume';
import ControlsP300 from './components/ControlsP300';


// Player
export default class P300 extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            playpauseToggle: 'play',
            currentTime: 0,
            audioVolume: 0.5,
            trackNr: 0,
            currentCmd: 'no',
            //colors: ['#e6194b', '#3cb44b', '#ffe119', '#0082c8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#d2f53c', '#e6beff', '#aaffc3', '#ffd8b1'],
            colors: ['#fff'],
            commands: ["next", "voldown", "playpause", "prev", "volup"],
            cmdInterval: 450,
            flashCmdInterval: 140
        };

        this.clickCommand = this.clickCommand.bind(this);
        this.execCommand = this.execCommand.bind(this);
        this.generateCommands = this.generateCommands.bind(this);

        subscribeToCmds(
            this.execCommand,
            this.execCommand,
        );

    };

    componentDidMount() {
        this.generateCommands();
    }


    generateCommands() {
        var commandIdx = 0;

        setInterval(function () {
            this.flashCommandButton(this.state.commands[commandIdx]);
            if (commandIdx < this.state.commands.length - 1) {
                commandIdx++;
            } else {
                commandIdx = 0;
            }
        }.bind(this), this.state.cmdInterval);
    }

    execCommand = (data) => {
        this.clickCommand(data.docommand);
        //  console.log("p300: "+data.docommand);
    };

    //Set the color of the command to white for X seconds
    flashCommandButton(command) {
        if (null !== command) {
            let elem = document.getElementById(command).getElementsByClassName('fa')[0];
            //elem.style.color = "#ffffff";
            elem.style.background = this.state.colors[Math.floor(Math.random() * this.state.colors.length)];

            //Send flashed command and timestamp to server
            let time = Date.now();
            sendP300Cmd(command, time);

            setTimeout(function () {
                elem.style.color = "#1c456e";
                elem.style.background = "#000";
            }, this.state.flashCmdInterval);
        }
    }

    clickCommand = (state) => {
        let audio = document.getElementById('audio');
        switch (state) {
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
            case "playpause":
                if (this.state.playpauseToggle === 'play') {
                    this.play(audio);
                } else if (this.state.playpauseToggle === 'pause'){
                    this.pause(audio);
                };
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

    updateScrubber(percent) {
        // Set scrubber width
        let innerScrubber = document.querySelector('.Scrubber-Progress');
        innerScrubber.style['width'] = percent;
    }

    updateVolumeProgressBar(volume) {
        var elem = document.getElementById("ProgressVolume");
        elem.style.width = 100 * volume + "%";
    }

    play(audio) {
        audio.play();
        audio.volume = this.state.audioVolume;
        let that = this;
        let duration = that.props.tracks[this.state.trackNr].duration;
        setInterval(function () {
            let currentTime = audio.currentTime;
            // Calculate percent of song
            let percent = (currentTime / duration) * 100 + '%';
            that.updateScrubber(percent);
            that.updateTime(currentTime);
        }, 100);
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
            <div className="Player P300">
                <div className="Info">
                    <div className="PlayerCover">
                        <div className="Artwork"
                             style={{'backgroundImage': 'url(' + this.props.tracks[this.state.trackNr].artwork + ')'}}></div>
                    </div>
                    <div className="PlayerInformation">
                        <TrackInformation tracks={this.props.tracks} state={this.state}/>
                        <Scrubber/>
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
                <ControlsP300 playpauseToggle={this.state.playpauseToggle} clickCommand={this.clickCommand}/>
            </div>

        )
    }
};
