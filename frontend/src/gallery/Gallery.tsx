import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import UploadMediaPreview from '../features/uploads/UploadMediaPreview';
import { useSelector } from 'react-redux';
import type { RootState } from '../store';

const Gallery = () => {
  const navigate = useNavigate();
  const { loading, user } = useSelector((state: RootState) => state.auth);

  useEffect(() => {
    if (!loading && user === null) {
      navigate('/login');
    }
  }, [user, loading, navigate]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Gallery</h1>
      <UploadMediaPreview />
    </div>
  );
};

export default Gallery;
