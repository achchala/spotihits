import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [artistName, setArtistName] = useState('');
  const [topSongs, setTopSongs] = useState([]);

  const getTopSongs = async () => {
    try {
      const searchResponse = await axios.get('https://api.spotify.com/v1/search', {
        params: {
          q: artistName,
          type: 'artist',
          limit: 1
        },
        headers: {
          'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
        }
      });

      const artistId = searchResponse.data.artists.items[0].id;

      const topTracksResponse = await axios.get(`https://api.spotify.com/v1/artists/${artistId}/top-tracks`, {
        params: {
          country: 'US'
        },
        headers: {
          'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
        }
      });

      const topSongs = topTracksResponse.data.tracks.slice(0, 5).map(track => track.name);

      setTopSongs(topSongs);
    } catch (error) {
      console.error('Error:', error.message);
    }
  };

  return (
    <div className="App">
      <h1>Top 5 Streamed Songs on Spotify</h1>
      <div>
        <input
          type="text"
          value={artistName}
          onChange={(e) => setArtistName(e.target.value)}
          placeholder="Enter artist name"
        />
        <button onClick={getTopSongs}>Get Top Songs</button>
      </div>
      {topSongs.length > 0 ? (
        <ul>
          {topSongs.map((song, index) => (
            <li key={index}>{song}</li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}

export default App;
