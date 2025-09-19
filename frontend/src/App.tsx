import { BrowserRouter, Routes, Route } from 'react-router';
import Header from './common/Header';
import Gallery from './gallery/Gallery';
import Login from './auth/Login';
import Register from './auth/Register';
import AuthProvider from './context/AuthProvider';
import { Provider } from 'react-redux';
import { store } from './store';

function App() {
  return (
    <div className="d-flex flex-column min-vh-100">
      <Provider store={store}>
        <AuthProvider>
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
        </AuthProvider>
      </Provider>
    </div>
  );
}

export default App;
