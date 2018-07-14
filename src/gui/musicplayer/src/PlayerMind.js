import React from 'react';
import './Player.css';
import {subscribeToMindCmds, sendTrainingCmd} from './api';
import TrackInformation from './components/TrackInformation';
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
            trainingTime: 7000,  //7 sec. for dev, 65 sec. aka 65000 for production (a bit longer than record session)
            currentTime: 0,
            audioVolume: 0.5,
            trackNr: 0,
            currentCmd: 'no',
            commands: {
                'volup': 'Focus on volume up and think of screaming with your mouth wide open.',
                'playpause': 'Focus on playing and think of leaning or going forward.',
                'next': 'Focus on next and think of stretching your right arm.',
                'prev': 'Focus on prev and think of stretching your left arm.',
                'voldown': 'Focus on volume down and think of lowering you head.'
            }
        };

        this.clickCommand = this.clickCommand.bind(this);
        this.execCommand = this.execCommand.bind(this);
        this.trainingInit = this.trainingInit.bind(this);
        this.trainingFinished = this.trainingFinished.bind(this);
        this.trainCommand = this.trainCommand.bind(this);
        this.showtrainCommand = this.showtrainCommand.bind(this);
        this.move = this.move.bind(this);
        this.toggleButtonsOnTraining = this.toggleButtonsOnTraining.bind(this);
        this.trainingPause = this.trainingPause.bind(this);

        subscribeToMindCmds(
            this.execCommand,
        );

    };

    componentWillUnmount() {
        if (this.state.playpauseToggle === 'play') {
            let audio = document.getElementById('audio');
            this.pause(audio);
        }
    }

    //init training session
    trainingInit = () => {
        this.toggleButtonsOnTraining(true);
        //pause audio
        let audio = document.getElementById('audio');
        this.pause(audio);
        let trainIcon = document.getElementById('training').getElementsByClassName('fa')[0];
        trainIcon.style.color = "lightblue";
        let infotext = document.getElementById('infotext');
        infotext.innerText = "Training will start soon. Relax and focus on the highlighted command.";

        //train each command
        let i = 3;  //TODO: set i = 0 to loop all commands
        const commands = Object.keys(this.state.commands);
        let interval = setInterval(function () {
            if (i === 5) {
                this.trainingFinished();
                clearInterval(interval);
            } else {
                this.showtrainCommand(commands[i]);
            }
            i++;
        }.bind(this), this.state.trainingTime + 2000); //waits 2000ms longer than actual training time
    }


    //show training finished
    trainingFinished() {
        let cmdIcons = document.getElementsByClassName('cmd');
        for (var i = 0; i < cmdIcons.length; i++) {
            cmdIcons[i].style.color = "#1c456e";
        }
        let infotext = document.getElementById('infotext');
        infotext.innerText = "Training finished. Have fun.";
        this.toggleButtonsOnTraining(false);
    }

    //show training pause
    trainingPause() {
        let cmdIcons = document.getElementsByClassName('cmd');
        for (var i = 0; i < cmdIcons.length; i++) {
            cmdIcons[i].style.color = "#1c456e";
        }
        let infotext = document.getElementById('infotext');
        infotext.innerText = "...hold on - the next command is coming!";
    }

    toggleButtonsOnTraining(disable) {
        let buttons = document.getElementsByClassName('Button');
        if (disable) {
            for (let i = 0; i < buttons.length; i++) {
                buttons[i].setAttribute('style', 'pointer-events: none;');
            }
        } else {
            for (let i = 0; i < buttons.length; i++) {
                buttons[i].setAttribute('style', 'pointer-events: all;');
            }
        }
    }

    //show training of command x in gui
    showtrainCommand(command) {
        //show info and start highligthing command to train
        let infotext = document.getElementById('infotext');
        infotext.innerText = this.state.commands[command];
        //reset all icons to default color
        let cmdIcons = document.getElementsByClassName('cmd');
        for (var i = 0; i < cmdIcons.length; i++) {
            cmdIcons[i].style.color = "#1c456e";
        }
        //highlight current training cmd icon
        let cmdIcon = document.getElementById(command).getElementsByClassName('fa')[0];
        cmdIcon.style.color = "#ffffff";
        //start progressBar for cmd
        this.move(command);
    }

    //progress bar training time and call trainCommand if time is passed
    move(command) {
        var elem = document.getElementById("progressBar");
        var width = 0;
        var id = setInterval(frame.bind(this), this.state.trainingTime / 100); // 1% of training time

        function frame() {
            if (width >= 100) {
                elem.style.width = 0 + '%';
                clearInterval(id);
                this.trainCommand(command);
            } else {
                width++;
                elem.style.width = width + '%';
            }
        }
    }

    //training of command x (init on server)
    trainCommand(command) {
        sendTrainingCmd(command);    //after training phase - server saves past data to file
        this.trainingPause(); //gui: show training pause
    }


    execCommand = () => {
        console.log("exec: " + this.state.currentCmd);
        this.clickCommand(this.state.currentCmd);
        let elem = document.getElementById(this.state.currentCmd).getElementsByClassName('fa')[0];
        elem.style.color = "green";
        setTimeout(function () {
            elem.style.color = "#1c456e";
        }, 250);
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
