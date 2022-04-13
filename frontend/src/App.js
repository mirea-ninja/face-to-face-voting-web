import React, { useState, useEffect } from 'react';
import { createStore, combineReducers, applyMiddleware, compose } from 'redux'
import { Provider } from 'react-redux'
import thunkMiddleware from 'redux-thunk'
import * as reducers from './reducers'
import './App.css';
import LoginPage from './pages/login/loginPage';
import logo from './assets/logo_sumirea.png';

const reducer = combineReducers(Object.assign({}, reducers, {}))

const enhancer = compose(
  applyMiddleware(thunkMiddleware),
)
const store = createStore(reducer, enhancer)

function App() {
  const [isLoading, setisLoading] = useState(true)

  useEffect(() => {
    let timer = setTimeout(() => setisLoading(false), 2000);
    return () => {
      clearTimeout(timer);
    };
  }, []);

  return (
    <Provider store={store}>
      <div className="container">
        {isLoading ? <img src={logo}></img> : <LoginPage />}
      </div>
    </Provider>

  );
}

export default App;
