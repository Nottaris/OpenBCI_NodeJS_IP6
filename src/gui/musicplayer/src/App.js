import React, {Component} from 'react';
import logo from './logo.png';
import mp3File_summer from './music/bensound-summer.mp3';
import mp3File_anewbeginning from './music/bensound-anewbeginning.mp3';
import mp3File_happyrock from './music/bensound-happyrock.mp3';
import mp3File_violinspider from './music/Marco_Trovatello_-_06_-_Violin_Spider.mp3';
import PlayerBlink from './PlayerBlink';
import PlayerP300 from './PlayerP300';
import './App.css';

class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="App">
                <header className="App-header">
                    <img src={logo} className="App-logo" alt="logo"/>
                    <h5 className="App-title">bci Music Player</h5>
                </header>
                {/*<PlayerBlink tracks={this.props.tracks}/>*/}
                <PlayerP300 tracks={this.props.tracks}/>
            </div>
        );
    }
}

App.defaultProps = {
    tracks: [
        {
            name: "Violin Spider",
            artist: "Marco Trovatello ",
            album: "Not At All",
            year: 2018,
            artwork: "https://freemusicarchive.org/file/images/albums/Marco_Trovatello_-_Not_At_All_-_20180519102404987.jpg",
            duration: 42,
            source: mp3File_violinspider
        },
        {
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
            duration: 217,
            source: mp3File_summer
        },
        {
            name: "A New Beginning",
            artist: "Bensound",
            album: "Summer's Gone",
            year: 2014,
            artwork: "https://www.bensound.com/bensound-img/anewbeginning.jpg",
            duration: 155,
            source: mp3File_anewbeginning
        },
        {
            name: "Happy Rock",
            artist: "Bensound",
            album: "Summer's Gone",
            year: 2015,
            artwork: "https://www.bensound.com/bensound-img/happyrock.jpg",
            duration: 106,
            source: mp3File_happyrock
        }
    ]
};
export default App;
