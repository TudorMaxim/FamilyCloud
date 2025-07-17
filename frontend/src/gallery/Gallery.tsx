import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import useAuth from '../hooks/useAuth';

const Gallery = () => {
  const navigate = useNavigate();
  const { loading, user } = useAuth();

  useEffect(() => {
    if (!user && !loading) {
      navigate('/login');
    }
  }, [user, loading, navigate]);

  return <h1>Gallery</h1>;
};

export default Gallery;
