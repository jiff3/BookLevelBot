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
            {json.filter((book) => {
              if (searchTerm == "") {
                return book;
              } else if (book.title.toString().toLowerCase().includes(searchTerm.toLowerCase()) || book.author.toString().toLowerCase().includes(searchTerm.toLowerCase())) {
                return book;
              }
            }).map((book, key) => {
            return (
            <div className='tile' key={key}>
                <img src={logo} />
                <b><p id='titl'>{truncate(book.title, 60)}</p></b>
                <p>By {truncate(book.author, 80)}</p>
                <p>Grade Level: {book.grade}</p>
                <p>ISBN: {book.isbn}</p>
                <div className='button-wrapper'>
                  <button onClick={() => setCount(book.copies > 0 ? book.copies -= 1 : 0)}>–</button>
                    <p id='available'>{book.copies}</p>
                  <button onClick={()=>setCount(book.copies +=1)}>+</button>
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