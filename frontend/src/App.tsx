import { BrowserRouter, Routes, Route } from 'react-router';
import Header from './common/Header';
import Gallery from './gallery/Gallery';
import AuthLayout from './auth/AuthLayout';
import Login from './auth/Login';
import Register from './auth/Register';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <>
      <AuthProvider>
        <BrowserRouter>
          <Header />
          <main className="container-fluid">
            <Routes>
              <Route path="/" element={<Gallery />}></Route>
              <Route element={<AuthLayout />}>
                <Route path="/login" element={<Login />}></Route>
                <Route path="/register" element={<Register />}></Route>
              </Route>
            </Routes>
          </main>
        </BrowserRouter>
      </AuthProvider>
    </>
  );
}

export default App;
