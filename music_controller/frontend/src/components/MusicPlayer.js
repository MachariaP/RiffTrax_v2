import React, { Component } from 'react';
import {
  Grid,
  Typography,
  Card,
  IconButton,
  LinearProgress,
} from '@material-ui/core';
import PlayArrowIcon from '@material-ui/icons/PlayArrow';
import PauseIcon from '@material-ui/icons/Pause';
import SkipNextIcon from '@material-ui/icons/SkipNext';

/**
 * MusicPlayer component displays a music player interface with controls to play, pause, and skip songs.
 */
export default class MusicPlayer extends Component {
  /**
   * Sends a request to skip the current song.
   */
  skipSong() {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    };
    fetch('/spotify/skip', requestOptions);
  }

  /**
   * Sends a request to pause the current song.
   */
  pauseSong() {
    const requestOptions = {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
    };
    fetch('/spotify/pause', requestOptions);
  }

  /**
   * Sends a request to play the current song.
   */
  playSong() {
    const requestOptions = {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
    };
    fetch('/spotify/play', requestOptions);
  }

  /**
   * Renders the component.
   * @returns {JSX.Element} The rendered component.
   */
  render() {
    const { time, duration, image_url, title, artist, is_playing, votes, votes_required } = this.props;
    const songProgress = (time / duration) * 100;

    return (
      <Card>
        <Grid container alignItems="center">
          <Grid item align="center" xs={4}>
            <img src={image_url} alt="Album cover" height="100%" width="100%" />
          </Grid>
          <Grid item align="center" xs={8}>
            <Typography component="h5" variant="h5">
              {title}
            </Typography>
            <Typography color="textSecondary" variant="subtitle1">
              {artist}
            </Typography>
            <div>
              <IconButton
                onClick={() => {
                  is_playing ? this.pauseSong() : this.playSong();
                }}
              >
                {is_playing ? <PauseIcon /> : <PlayArrowIcon />}
              </IconButton>
              <IconButton onClick={() => this.skipSong()}>
                {votes} / {votes_required}
                <SkipNextIcon />
              </IconButton>
            </div>
          </Grid>
        </Grid>
        <LinearProgress variant="determinate" value={songProgress} />
      </Card>
    );
  }
}
