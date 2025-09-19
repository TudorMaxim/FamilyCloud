import { BrowserRouter, Routes, Route } from 'react-router';
import { Provider } from 'react-redux';
import Header from './common/Header';
import Gallery from './gallery/Gallery';
import Login from './features/auth/Login';
import Register from './features/auth/Register';
import { store } from './store';

function App() {
  return (
    <div className="d-flex flex-column min-vh-100">
      <Provider store={store}>
        <BrowserRouter>
          <Header />
          <main className="container-fluid d-flex flex-grow-1">
            <Routes>
              <Route path="/" element={<Gallery />}></Route>
              <Route path="/login" element={<Login />}></Route>
              <Route path="/register" element={<Register />}></Route>
            </Routes>
          </main>
        </BrowserRouter>
      </Provider>
    </div>
  );
}

export default App;
