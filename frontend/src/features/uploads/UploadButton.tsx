import React from 'react';
import styled from 'styled-components';
import { useDispatch } from 'react-redux';
import type { AppDispatch } from '../../store';
import { addFiles } from './slice';
import { storeFiles } from './fileMap';
import { validateFiles } from './validation';
import Alert from '../../common/Alert';

const CHUNK_SIZE = 5 * 1024 * 1024; // 5MB

const UploadIcon = styled.span`
  color: var(--bs-nav-link-color);
  font-size: 1.25rem;
  margin: 0.5rem;

  &:focus,
  &:hover {
    color: var(--bs-nav-link-hover-color);
    cursor: pointer;
  }
`;

const MediaPicker = styled.input`
  display: none;
`;

const UploadButton = () => {
  const mediaPickerRef = React.useRef<HTMLInputElement | null>(null);
  const dispatch = useDispatch<AppDispatch>();
  const [validationErrors, setValidationErrors] = React.useState<string[]>([]);

  const handleMediaPickerChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = event.target.files ? Array.from(event.target.files) : [];
    
    // Validate files before processing
    const { valid, invalid } = validateFiles(selectedFiles);
    
    // Show validation errors if any
    if (invalid.length > 0) {
      setValidationErrors(invalid.map((i) => i.error.message));
    } else {
      setValidationErrors([]);
    }

    // Store and add only valid files
    if (valid.length > 0) {
      storeFiles(valid.map((v) => v.file));
      dispatch(
        addFiles(
          valid.map((v) => ({
            name: v.file.name,
            size: v.file.size,
            type: v.file.type,
            lastModified: v.file.lastModified,
            preview: URL.createObjectURL(v.file),
            progress: 0,
            taskId: null,
            totalChunks: Math.ceil(v.file.size / CHUNK_SIZE),
            uploadedChunks: 0,
            mediaType: v.mediaType,
          }))
        )
      );
    }
  };

  return (
    <div className="d-flex align-items-center">
      {validationErrors.length > 0 && (
        <div style={{ position: 'absolute', top: '60px', right: '10px', zIndex: 1000, maxWidth: '400px' }}>
          {validationErrors.map((error, idx) => (
            <Alert key={idx} type="danger" message={error} />
          ))}
        </div>
      )}
      <UploadIcon className="bi bi-plus-circle" onClick={() => mediaPickerRef.current?.click()} />
      <MediaPicker
        type="file"
        multiple
        accept="image/*,video/*"
        ref={mediaPickerRef}
        onChange={handleMediaPickerChange}
      />
    </div>
  );
};

export default UploadButton;
