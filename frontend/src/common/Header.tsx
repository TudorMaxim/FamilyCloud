import styled from 'styled-components';
import { Link, NavLink, useNavigate } from 'react-router';
import FamilyCloudIcon from '../assets/familyCloudIcon.svg';
import useAuth from '../hooks/useAuth';
import familyCloudAPI from '../api';

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
  return (
    <>
      <li className="navbar-item">
        <a
          href="#"
          className="nav-link"
          onClick={() => familyCloudAPI.logout().then(() => navigate('/'))}
        >
          Logout
        </a>
      </li>
    </>
  );
};

const Header = () => {
  const { loading, user } = useAuth();
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
