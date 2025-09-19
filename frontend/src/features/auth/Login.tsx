import React from 'react';
import { useNavigate } from 'react-router';
import { useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from '../../store';
import type { UserCredentials } from '../../api/types';
import familyCloudAPI from '../../api';
import Alert from '../../common/Alert';
import useAlert from '../../hooks/useAlert';
import { setUser, setLoading } from './slice';

const Login = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();
  const { loading, authenticated } = useSelector((state: RootState) => state.auth);
  const { alert, setAlert } = useAlert();
  const [credentials, setCredentials] = React.useState<UserCredentials>({
    email: '',
    password: '',
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    dispatch(setLoading(true));
    familyCloudAPI
      .login(credentials)
      .then((user) => {
        dispatch(setUser(user));
        navigate('/');
      })
      .catch((err) => setAlert(err.message))
      .finally(() => dispatch(setLoading(false)));
  };

  React.useEffect(() => {
    if (authenticated) {
      navigate('/');
    }
  }, [authenticated, navigate]);

  return (
    <>
      <Alert type="danger" message={alert} />
      <div className="d-flex justify-content-center align-items-center flex-grow-1">
        <form
          onSubmit={handleSubmit}
          className="border p-4 rounded shadow bg-light"
          style={{ minWidth: '360px' }}
        >
          <div className="col md-6">
            <label htmlFor="inputEmail" className="col-form-label">
              Email
            </label>
            <input
              type="email"
              className="form-control"
              id="inputEmail"
              onChange={(e) => setCredentials((prev) => ({ ...prev, email: e.target.value }))}
              required
            />
          </div>
          <div className="col md-6">
            <label htmlFor="inputPassword" className="col-form-label">
              Password
            </label>
            <input
              type="password"
              className="form-control"
              id="inputPassword"
              onChange={(e) => setCredentials((prev) => ({ ...prev, password: e.target.value }))}
              required
            />
          </div>
          <div className="d-flex justify-content-center align-items-center">
            <button type="submit" className="btn btn-primary mt-4" disabled={loading}>
              Login
            </button>
          </div>
        </form>
      </div>
    </>
  );
};

export default Login;
