import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import useAuth from '../hooks/useAuth';
import UploadMediaPreview from '../features/uploads/UploadMediaPreview';

const Gallery = () => {
  const navigate = useNavigate();
  const { loading, user } = useAuth();

  useEffect(() => {
    if (!user && !loading) {
      navigate('/login');
    }
  }, [user, loading, navigate]);

  return (
    <div>
      <h1>Gallery</h1>
      <UploadMediaPreview />
    </div>
  );
};

export default Gallery;
