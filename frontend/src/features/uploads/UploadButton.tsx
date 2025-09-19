import React from 'react';
import styled from 'styled-components';
import { useDispatch } from 'react-redux';
import type { AppDispatch } from '../../store';
import { addFiles } from './slice';
import { storeFiles } from './fileMap';

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

  const handleMediaPickerChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = event.target.files ? Array.from(event.target.files) : [];
    storeFiles(selectedFiles);
    if (selectedFiles.length > 0) {
      dispatch(
        addFiles(
          selectedFiles.map((file) => ({
            name: file.name,
            size: file.size,
            type: file.type,
            lastModified: file.lastModified,
            preview: URL.createObjectURL(file),
            progress: 0,
            taskId: null,
            totalChunks: Math.ceil(file.size / CHUNK_SIZE),
            uploadedChunks: 0,
          }))
        )
      );
    }
  };

  return (
    <div className="d-flex align-items-center">
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
