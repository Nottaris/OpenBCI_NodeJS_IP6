import React from 'react';
import './Player.css';
import {subscribeToMindCmds, sendTrainingCmd} from './api';
import TrackInformation from './components/TrackInformation';
import Scrubber from './components/Scrubber';
import Timestamps from './components/Timestamps';
import AudioVolume from './components/AudioVolume';
import ControlsMind from './components/ControlsMind';
import Training from './components/Training';

// Player
export default class PlayerBlink extends React.Component {
    constructor(props) {
        super(props);
        console.log(props);
        this.state = {
            playpauseToggle: 'play',
            trainingToggle: false,
            currentTime: 0,
            audioVolume: 0.5,
            trackNr: 0,
            currentCmd: 'no',
            commands: [
                'playpause',
                'next',
                'prev',
                'volup',
                'voldown'
            ]
        };

        this.clickCommand = this.clickCommand.bind(this);
        this.execCommand = this.execCommand.bind(this);
        this.trainingInit = this.trainingInit.bind(this);
        this.trainingFinished = this.trainingFinished.bind(this);
        this.trainCommand = this.trainCommand.bind(this);

        subscribeToMindCmds(
            this.execCommand,
        );

    };

    //init training session
    trainingInit = () => {
        if (!this.state.trainingToggle) {
            this.setState({trainingToggle: true});
            //pause audio
            let audio = document.getElementById('audio');
            this.pause(audio);
            let trainIcon = document.getElementById('training').getElementsByClassName('fa')[0];
            trainIcon.style.color = "lightblue";

            //train each command
            let i = 0;
            let interval = setInterval(function () {
                if(i===5){
                    this.trainingFinished();
                    clearInterval(interval);
                    return;
                }else{
                    this.trainCommand(this.state.commands[i]);
                }
                i++;
            }.bind(this), 7000);  //7 sec. for dev, 65 sec. aka 65000 for production (a bit longer than record session)


        } else {
            alert("Training already running. Wait until finished and restart if desired.");
        }
    }

    //show training finished
    trainingFinished() {
        this.setState({trainingToggle: false});
        let cmdIcons = document.getElementsByClassName('fa');
        for (var i = 0; i < cmdIcons.length; i++) {
            cmdIcons[i].style.color = "#1c456e";
        }
        let infotext = document.getElementById('infotext');
        infotext.innerText = "Training finished. Have fun.";
    }

    //training of command x
    trainCommand(command) {
        //show info and start highligthing command to train
        let infotext = document.getElementById('infotext');
        //TODO: alter text based on command to train
        infotext.innerText = "Concentrate on playing and think of leaning or going forward.";
        let cmdIcon = document.getElementById(command).getElementsByClassName('fa')[0];
        cmdIcon.style.color = "#ffffff";
        sendTrainingCmd(command);
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
                } else if (this.state.playpauseToggle === 'pause') {
                    this.pause(audio);
                }
                break;
            default:
                //this should never happen
                console.log("Error: clickCommand had unknown state " + typeof state);
                break;
        }

    };

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
            <div className="Player Blink">
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
                <ControlsMind playpauseToggle={this.state.playpauseToggle} clickCommand={this.clickCommand}/>
                <Training trainingInit={this.trainingInit}/>
            </div>

        )
    }
};
