import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import { Link } from 'react-router-dom';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import { Collapse } from '@material-ui/core';
import Alert from '@material-ui/lab/Alert';

/**
 * CreateRoomPage component allows users to create or update a room with specific settings.
 */
export default class CreateRoomPage extends Component {
  // Default props for the component
  static defaultProps = {
    votesToSkip: 2,
    guestCanPause: true,
    update: false,
    roomCode: null,
    updateCallback: () => {},
  };

  constructor(props) {
    super(props);
    // Initialize state
    this.state = {
      guestCanPause: this.props.guestCanPause,
      votesToSkip: this.props.votesToSkip,
      errorMsg: '',
      successMsg: '',
    };

    // Bind event handlers
    this.handleRoomButtonPressed = this.handleRoomButtonPressed.bind(this);
    this.handleVotesChange = this.handleVotesChange.bind(this);
    this.handleGuestCanPauseChange = this.handleGuestCanPauseChange.bind(this);
    this.handleUpdateButtonPressed = this.handleUpdateButtonPressed.bind(this);
  }

  /**
   * Handle change in votes to skip input.
   * @param {Event} e - The change event.
   */
  handleVotesChange(e) {
    this.setState({
      votesToSkip: e.target.value,
    });
  }

  /**
   * Handle change in guest can pause radio buttons.
   * @param {Event} e - The change event.
   */
  handleGuestCanPauseChange(e) {
    this.setState({
      guestCanPause: e.target.value === 'true',
    });
  }

  /**
   * Handle the create room button press.
   */
  handleRoomButtonPressed() {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        votes_to_skip: this.state.votesToSkip,
        guest_can_pause: this.state.guestCanPause,
      }),
    };
    fetch('/api/create-room', requestOptions)
      .then((response) => response.json())
      .then((data) => this.props.history.push(`/room/${data.code}`));
  }

  /**
   * Handle the update room button press.
   */
  handleUpdateButtonPressed() {
    const requestOptions = {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        votes_to_skip: this.state.votesToSkip,
        guest_can_pause: this.state.guestCanPause,
        code: this.props.roomCode,
      }),
    };
    fetch('/api/update-room', requestOptions).then((response) => {
      if (response.ok) {
        this.setState({
          successMsg: 'Room updated successfully!',
        });
      } else {
        this.setState({
          errorMsg: 'Error updating room...',
        });
      }
      this.props.updateCallback();
    });
  }

  /**
   * Render buttons for creating a room.
   * @returns {JSX.Element} The create buttons.
   */
  renderCreateButtons() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Button
            color="primary"
            variant="contained"
            onClick={this.handleRoomButtonPressed}
          >
            Create A Room
          </Button>
        </Grid>
        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  }

  /**
   * Render button for updating a room.
   * @returns {JSX.Element} The update button.
   */
  renderUpdateButtons() {
    return (
      <Grid item xs={12} align="center">
        <Button
          color="primary"
          variant="contained"
          onClick={this.handleUpdateButtonPressed}
        >
          Update Room
        </Button>
      </Grid>
    );
  }

  /**
   * Render the component.
   * @returns {JSX.Element} The rendered component.
   */
  render() {
    const { update } = this.props;
    const { errorMsg, successMsg, votesToSkip, guestCanPause } = this.state;
    const title = update ? 'Update Room' : 'Create a Room';

    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Collapse in={errorMsg !== '' || successMsg !== ''}>
            {successMsg !== '' ? (
              <Alert
                severity="success"
                onClose={() => {
                  this.setState({ successMsg: '' });
                }}
              >
                {successMsg}
              </Alert>
            ) : (
              <Alert
                severity="error"
                onClose={() => {
                  this.setState({ errorMsg: '' });
                }}
              >
                {errorMsg}
              </Alert>
            )}
          </Collapse>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            {title}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl component="fieldset">
            <FormHelperText>
              <div align="center">Guest Control of Playback State</div>
            </FormHelperText>
            <RadioGroup
              row
              defaultValue={guestCanPause.toString()}
              onChange={this.handleGuestCanPauseChange}
            >
              <FormControlLabel
                value="true"
                control={<Radio color="primary" />}
                label="Play/Pause"
                labelPlacement="bottom"
              />
              <FormControlLabel
                value="false"
                control={<Radio color="secondary" />}
                label="No Control"
                labelPlacement="bottom"
              />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl>
            <TextField
              required
              type="number"
              onChange={this.handleVotesChange}
              defaultValue={votesToSkip}
              inputProps={{
                min: 1,
                style: { textAlign: 'center' },
              }}
            />
            <FormHelperText>
              <div align="center">Votes Required To Skip Song</div>
            </FormHelperText>
          </FormControl>
        </Grid>
        {update ? this.renderUpdateButtons() : this.renderCreateButtons()}
      </Grid>
    );
  }
}
