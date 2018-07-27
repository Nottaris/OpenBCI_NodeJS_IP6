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
            trainingTime: 6000,  //TODO: set final time, (?) 6 sec. recording (pause will be added)
            currentTime: 0,
            audioVolume: 0.5,
            trackNr: 0,
            currentCmd: 'no',
            commands: ['volup', 'playpause', 'next', 'prev', 'voldown'],
            commandinfos: [' volume up - open mouth',
                'play - go forward',
                'next - right hand',
                'prev - left hand',
                'volume down - move feet'
            ],
            commandpreinfos: ['Focus on volume up and think of screaming with your mouth wide open.',
                'Focus on playing and think of leaning and going forward.',
                'Focus on next and think of open and closing your right hand to a fist.',
                'Focus on prev and think of open and closing your left hand to a fist.',
                'Focus on volume down and think of moving your feet.'
            ]
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
        //init text
        infotext.innerText = "Training will start soon. Relax and sit comfy.";
        //info for first command training
        setTimeout(function () {
            infotext.innerText = "Focus on volume up and think of screaming with your mouth wide open.";
        }, 2000);

        //train each command
        let i = 0;
        let interval = setInterval(function () {
            if (i === 5) {
                this.trainingStartML();
                clearInterval(interval);
            } else {
                this.showtrainCommand(this.state.commands[i]);
            }
            i++;
        }.bind(this), this.state.trainingTime + 6000);  //training time plus pause
    }

    //training recording finished, init ml training
    trainingStartML() {
        let infotext = document.getElementById('infotext');
        infotext.innerText = "Please wait. Training data is processed.";
        sendTrainingCmd({command: 'init', slots: 0});
        setTimeout(function () {
            this.trainingFinished();
        }.bind(this), 6000);
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
    trainingPause(info) {
        let cmdIcons = document.getElementsByClassName('cmd');
        for (var i = 0; i < cmdIcons.length; i++) {
            cmdIcons[i].style.color = "#1c456e";
        }
        let infotext = document.getElementById('infotext');
        infotext.innerText = "...relax - stay calm...";
        setTimeout(function () {
            infotext.innerText = info;
        }, 3000);
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
        let cmdindex = this.state.commands.indexOf(command);
        infotext.innerText = this.state.commandinfos[cmdindex];
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
        let trainingSlotSize = this.state.trainingTime / 4;    //on 250 Hz, each 4 ms a sample is recorded
        sendTrainingCmd({command: command, slots: trainingSlotSize});    //after training phase - server saves past data to file
        // get next command
        let cmdindex = this.state.commands.indexOf(command);
        let nextcmd = cmdindex+1;
        let info = '...relax - stay calm...';
        if (nextcmd !== 5){
            info = this.state.commandpreinfos[nextcmd];
        }
        this.trainingPause(info); //gui: show training pause
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
