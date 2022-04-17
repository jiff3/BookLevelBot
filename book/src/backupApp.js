import logo from './download.jpg';
import './App.css';
import json from './new_inventory.json';
import { isValidElement, useState } from 'react';


function App() {
  const [searchTerm, setSearchTerm] = useState("");
  const [count, setCount] = useState(0);

  return (
    <div className="App">
        <input
            type = "text"
            placeholder='Enter Title Name'
            onChange={(event) => {
            setSearchTerm(event.target.value);
            }}
        />
            
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
                <img src={logo} />
                <div className='info'>
                    <b><p>{truncate(val.title, 70)}</p></b>
                    <p>By {truncate(val.author, 100)}</p>
                    <p>Grade Level: {val.grade}</p>
                    <p>ISBN: {val.isbn}</p>
                </div>
                <div className='button-wrapper'>
                  <button onClick={()=>setCount(count-1)}>–</button>
                  <p id='available'>{val.copies}</p>
                  <button onClick={()=>setCount(count+1)}>+</button>
                </div>
            </div>
            );
        })}
        </div>
    </div>
  );
}

function truncate(str, n) {
  
  return str?.length > (window.innerWidth / n) ? str.substr(0, window.innerWidth / n) + "..." : str;
}


export default App;