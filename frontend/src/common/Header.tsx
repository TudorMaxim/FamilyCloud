import styled from 'styled-components';
import { useDispatch } from 'react-redux';
import type { RootState, AppDispatch } from '../store';
import { setUser } from '../features/auth/slice';
import { Link, NavLink, useNavigate } from 'react-router';
import FamilyCloudIcon from '../assets/familyCloudIcon.svg';
import familyCloudAPI from '../api';
import UploadButton from '../features/uploads/UploadButton';
import { useSelector } from 'react-redux';
import useCurrentUser from '../hooks/useCurrentUser';

const Title = styled.span`
  margin: 0 8px;
`;

const UnauthenticatedLinks = () => (
  <>
    <li className="nav-item">
      <NavLink to="/login" className="nav-link">
        Login
      </NavLink>
    </li>
    <li className="navbar-item">
      <NavLink to="/register" className="nav-link">
        Register
      </NavLink>
    </li>
  </>
);

const AuthenticatedLinks = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();
  const logout = async () => {
    try {
      const response = await familyCloudAPI.logout();
      if (response.ok) {
        dispatch(setUser(null));
        navigate('/');
      }
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <>
      <li className="navbar-item">
        <UploadButton />
      </li>
      <li className="navbar-item d-flex align-items-center">
        <a href="#" className="nav-link" onClick={logout}>
          Logout
        </a>
      </li>
    </>
  );
};

const Header = () => {
  const { loading, user } = useSelector((state: RootState) => state.auth);
  useCurrentUser();

  return (
    <nav className="navbar navbar-expand-lg sticky-top navbar-dark bg-dark">
      <div className="container-fluid">
        <Link to="/" className="navbar-brand">
          <img src={FamilyCloudIcon} width={30} height={30} alt="Logo" />
          <Title>Family Cloud</Title>
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#headerLinks"
          aria-controls="headerLinks"
          aria-expanded="false"
          aria-label="Toggle header links"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="headerLinks">
          <ul className="navbar-nav ms-auto">
            {!loading && !user && <UnauthenticatedLinks />}
            {!loading && user && <AuthenticatedLinks />}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Header;
