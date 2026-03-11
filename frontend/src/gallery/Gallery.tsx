import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import styled from 'styled-components';
import UploadMediaPreview from '../features/uploads/UploadMediaPreview';
import MediaDisplay from '../features/uploads/MediaDisplay';
import { useSelector } from 'react-redux';
import type { RootState } from '../store';

const GalleryWrapper = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
`;

const GalleryGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
  margin-top: 20px;
`;

const MediaCard = styled.div`
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  }
`;

const MediaInfo = styled.div`
  padding: 12px;
  background: white;
  font-size: 0.9rem;
  color: #333;
  
  .filename {
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 4px;
  }
  
  .meta {
    font-size: 0.8rem;
    color: #666;
  }
`;

interface FileMetadata {
  id: number;
  filename: string;
  media_type: 'photo' | 'video';
  thumbnail_path?: string | null;
  duration?: number | null;
  uploaded_at?: string;
}

const Gallery = () => {
  const navigate = useNavigate();
  const { loading, user } = useSelector((state: RootState) => state.auth);
  const [files, setFiles] = useState<FileMetadata[]>([]);
  const [filesLoading, setFilesLoading] = useState(false);

  const fetchFiles = async () => {
    try {
      setFilesLoading(true);
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/files`, {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setFiles(data);
      }
    } catch (error) {
      console.error('Error fetching files:', error);
    } finally {
      setFilesLoading(false);
    }
  };

  useEffect(() => {
    if (!loading && user === null) {
      navigate('/login');
    }
  }, [user, loading, navigate]);

  useEffect(() => {
    if (user) {
      fetchFiles();
    }
  }, [user]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <GalleryWrapper>
      <h1>Gallery</h1>
      <UploadMediaPreview onUploadComplete={fetchFiles} />
      
      {filesLoading && <p>Loading files...</p>}
      
      {files.length > 0 ? (
        <>
          <h2 style={{ marginTop: '40px' }}>Your Files ({files.length})</h2>
          <GalleryGrid>
            {files.map((file) => (
              <MediaCard key={file.id}>
                <MediaDisplay
                  mediaType={file.media_type}
                  thumbnailPath={file.thumbnail_path}
                  filename={file.filename}
                  duration={file.duration}
                />
                <MediaInfo>
                  <div className="filename" title={file.filename}>
                    {file.filename}
                  </div>
                  <div className="meta">
                    {file.media_type === 'video' && file.duration && (
                      <>{Math.floor(file.duration / 60)}:{(file.duration % 60).toString().padStart(2, '0')}</>
                    )}
                    {file.media_type === 'photo' && 'Photo'}
                  </div>
                </MediaInfo>
              </MediaCard>
            ))}
          </GalleryGrid>
        </>
      ) : (
        <p style={{ marginTop: '20px', color: '#666' }}>No files yet. Upload some photos or videos to get started!</p>
      )}
    </GalleryWrapper>
  );
};

export default Gallery;
