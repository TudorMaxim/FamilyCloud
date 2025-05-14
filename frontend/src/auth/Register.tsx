import React from 'react';
import type { UserRegistrationData } from '../api/types';

const Register = () => {
  const [userData, setUserData] = React.useState<UserRegistrationData>({
    email: '',
    password: '',
    firstName: '',
    lastName: '',
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log('Submit');
    console.log(userData);
  };

  return (
    <div className="d-flex justify-content-center align-items-center flex-grow-1">
      <form
        onSubmit={handleSubmit}
        className="border p-4 rounded shadow bg-light"
        style={{ minWidth: '360px' }}
      >
        <div className="col md-6">
          <label htmlFor="inputFirstName" className="col-form-label">
            First Name
          </label>
          <input
            type="text"
            className="form-control"
            id="inputFirstName"
            onChange={(e) => setUserData((prev) => ({ ...prev, firstName: e.target.value }))}
            required
          />
        </div>
        <div className="col md-6">
          <label htmlFor="inputLastName" className="col-form-label">
            Last Name
          </label>
          <input
            type="text"
            className="form-control"
            id="inputLastName"
            onChange={(e) => setUserData((prev) => ({ ...prev, lastName: e.target.value }))}
            required
          />
        </div>
        <div className="col md-6">
          <label htmlFor="inputEmail" className="col-form-label">
            Email
          </label>
          <input
            type="email"
            className="form-control"
            id="inputEmail"
            onChange={(e) => setUserData((prev) => ({ ...prev, email: e.target.value }))}
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
            onChange={(e) => setUserData((prev) => ({ ...prev, password: e.target.value }))}
            required
          />
        </div>
        <div className="d-flex justify-content-center align-items-center">
          <button type="submit" className="btn btn-primary mt-4">
            Register
          </button>
        </div>
      </form>
    </div>
  );
};

export default Register;
