import './App.css';
import React, { useState, useEffect } from 'react';
import { TwitterTweetEmbed } from 'react-twitter-embed';

function App() {
  const [fileLines, setFileLines] = useState([]);

  useEffect(() => {
    const readFile = async () => {
      try {
        const response = await fetch('tweets.txt'); // Replace with your file's URL or path
        const text = await response.text();
        const lines = text.split('\n');
        setFileLines(lines);
      } catch (error) {
        console.error('Error reading the file:', error);
      }
    };

    readFile();
  }, []); 

  return (
    <div className="App">
      <div className="App2">
        {fileLines.map((line, index) => (
          <TwitterTweetEmbed
            key={index}
            tweetId={line.toString()}
            options={{width: 1200}}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
