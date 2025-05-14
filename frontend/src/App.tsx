import { BrowserRouter, Routes, Route } from 'react-router';
import Header from './common/Header';
import Login from './auth/Login';
import Register from './auth/Register';
import Gallery from './gallery/Gallery';

function App() {
  return (
    <>
      <BrowserRouter>
        <Header />
        <main className="container-fluid">
          <Routes>
            <Route path="/" element={<Gallery />}></Route>
            <Route path="/login" element={<Login />}></Route>
            <Route path="/register" element={<Register />}></Route>
          </Routes>
        </main>
      </BrowserRouter>
    </>
  );
}

export default App;
