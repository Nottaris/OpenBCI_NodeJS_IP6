// Playerhelpers

export const clickCommand = (state) => {
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
        case " = prev":
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

export const updateTime = (timestamp) => {
    timestamp = Math.floor(timestamp);
    this.setState({currentTime: timestamp});
}

export const updateScrubber = (percent) => {
    // Set scrubber width
    let innerScrubber = document.querySelector('.Scrubber-Progress');
    innerScrubber.style['width'] = percent;
}

export const updateVolumeProgressBar = (volume) => {
    var elem = document.getElementById("ProgressVolume");
    elem.style.width = 100 * volume + "%";
}

export const play = (audio) => {
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

export const pause = (audio) => {
    audio.pause();
    this.setState({playpauseToggle: 'play'});
}

export const next = (audio) => {
    this.setState({trackNr: this.mod((this.state.trackNr + 1), this.props.tracks.length)});
    audio = document.getElementById('audio');
    //load new audio file
    audio.load();
    this.play(audio);
}

export const prev = (audio) => {
    this.setState({trackNr: this.mod((this.state.trackNr - 1), this.props.tracks.length)});
    audio = document.getElementById('audio');
    //load new audio file
    audio.load();
    this.play(audio);
}

export const volup = (audio) => {
    if (this.state.audioVolume < 0.8) {
        let newVol = this.state.audioVolume + 0.25;
        this.setState({audioVolume: newVol});
        audio.volume = newVol;
        this.updateVolumeProgressBar(newVol);
    }
}

export const voldown = (audio) => {
    if (this.state.audioVolume > 0.2) {
        let newVol = this.state.audioVolume - 0.25;
        this.setState({audioVolume: newVol});
        audio.volume = newVol;
        this.updateVolumeProgressBar(newVol);
    }
}

// Help function: Modulo operation with negative numbers
export const mod = (a, n) => {
    return a - (n * Math.floor(a / n));
}


