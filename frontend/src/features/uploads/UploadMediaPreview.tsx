import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import styled from 'styled-components';
import type { RootState, AppDispatch } from '../../store';
import uploadFiles from './uploadFiles';
import { removeFile, resetUploads } from './slice';

const MediaBadge = styled.span<{ $mediaType: string }>`
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 8px;
  background-color: ${(props) => (props.$mediaType === 'photo' ? '#e3f2fd' : '#f3e5f5')};
  color: ${(props) => (props.$mediaType === 'photo' ? '#1976d2' : '#7b1fa2')};
`;

const RemoveButton = styled.button`
  position: absolute;
  top: 5px;
  right: 5px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #ddd;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  
  &:hover {
    background: rgba(0, 0, 0, 0.8);
    color: white;
  }
`;

const MediaContainer = styled.div`
  position: relative;
  padding: 8px;
  border-radius: 4px;
  background: #f5f5f5;
`;

interface UploadMediaPreviewProps {
  onUploadComplete?: () => void;
}

const UploadMediaPreview: React.FC<UploadMediaPreviewProps> = ({ onUploadComplete }) => {
  const { tasks, overallProgress } = useSelector((state: RootState) => state.uploads);
  const dispatch = useDispatch<AppDispatch>();

  const handleUpload = React.useCallback(async () => {
    const validTasks = tasks.filter((t) => !t.validationError);
    if (validTasks.length > 0) {
      await uploadFiles(validTasks, dispatch);
      // Clear upload list and call completion callback
      setTimeout(() => {
        dispatch(resetUploads());
        onUploadComplete?.();
      }, 1000);
    }
  }, [tasks, dispatch, onUploadComplete]);

  const handleRemoveFile = (fileName: string) => {
    dispatch(removeFile(fileName));
  };

  return (
    <div className="container py-3">
      <button className="btn btn-primary mb-3" onClick={handleUpload} disabled={tasks.length === 0}>
        Upload All
      </button>

      {tasks.length > 0 && (
        <div className="progress mb-3" style={{ height: '20px' }}>
          <div
            className="progress-bar progress-bar-striped progress-bar-animated"
            role="progressbar"
            style={{ width: `${overallProgress}%` }}
          >
            {overallProgress}%
          </div>
        </div>
      )}

      <div className="row">
        {tasks.map((t, idx) => (
          <div key={idx} className="col-3 mb-3">
            <MediaContainer>
              <RemoveButton onClick={() => handleRemoveFile(t.name)}>×</RemoveButton>
              {t.preview ? (
                <img src={t.preview} className="img-fluid mb-1" alt={t.name} />
              ) : (
                <span>{t.name}</span>
              )}
              <div style={{ marginBottom: '8px' }}>
                <MediaBadge $mediaType={t.mediaType}>{t.mediaType.toUpperCase()}</MediaBadge>
              </div>
              {t.validationError && (
                <div style={{ color: '#d32f2f', fontSize: '0.85rem', marginBottom: '8px' }}>
                  ⚠ {t.validationError.message}
                </div>
              )}
              <div className="progress">
                <div
                  className="progress-bar progress-bar-striped progress-bar-animated"
                  role="progressbar"
                  style={{ width: `${t.progress}%` }}
                >
                  {t.progress}%
                </div>
              </div>
            </MediaContainer>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UploadMediaPreview;
