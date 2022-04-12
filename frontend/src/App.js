import React, { useState, useEffect } from 'react';
import './App.css';
import LoginPage from './pages/login/loginPage';
import logo from './assets/logo_sumirea.png';

function App() {
  const [isLoading, setisLoading] = useState(true)

  useEffect(() => {
    let timer = setTimeout(() => setisLoading(false), 2000);
    return () => {
      clearTimeout(timer);
    };
  }, []);

  return (
    <div className="container">
      {isLoading ? <img src={logo}></img> : <LoginPage />}
    </div>
  );
}

export default App;
