import React, { Component } from 'react';
import { render } from 'react-dom';
import HomePage from './HomePage';

/**
 * App component serves as the main entry point for the application.
 */
export default class App extends Component {
  /**
   * Renders the component.
   * @returns {JSX.Element} The rendered component.
   */
  render() {
    return (
      <div className="center">
        <HomePage />
      </div>
    );
  }
}

// Get the DOM element to mount the React application
const appDiv = document.getElementById('app');

// Render the App component into the DOM element
render(<App />, appDiv);