import './App.css';
import json from './data.json';
import { isValidElement, useState } from 'react';


function App() {
  const [searchTerm, setSearchTerm] = useState("");

  return (
    <div className="App">
        <div className='searchBox'>
            <input
                type = "text"
                placeholder='Enter Title Name'
                onChange={(event) => {
                setSearchTerm(event.target.value);
                }}
            />
            
        </div>
        <div className='tiles'>
            {json.filter((val) => {
              if (searchTerm == "") {
                return val;
              } else if (val.title.toString().toLowerCase().includes(searchTerm.toLowerCase())) {
                return val;
              }
            }).map((val, key) => {
            return (
            <div className='tile' key={key}>
                {/* <img src="download.png" /> */}
                <b><p>{truncate(val.title)}</p></b>
                <p>By {truncate(val.author)}</p>
            </div>
            );
        })}
        </div>
    </div>
  );
}

function truncate(str) {
  let n = 30;
  return str?.length > (window.innerWidth / n) ? str.substr(0, window.innerWidth / n) + "..." : str;
}

export default App;