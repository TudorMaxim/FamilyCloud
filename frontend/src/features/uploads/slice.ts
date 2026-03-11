import { createSlice, type PayloadAction } from '@reduxjs/toolkit';
import type { MediaType, ValidationError } from './validation';

export type FileMeta = {
  name: string;
  size: number;
  type: string;
  lastModified: number;
};

export type FileUploadTask = FileMeta & {
  preview: string;
  progress: number;
  taskId: string | null;
  totalChunks?: number;
  uploadedChunks?: number;
  mediaType: MediaType;
  validationError?: ValidationError;
};

type UploadState = {
  tasks: FileUploadTask[];
  overallProgress: number;
};

const initialState: UploadState = {
  tasks: [],
  overallProgress: 0,
};

const uploadSlice = createSlice({
  name: 'uploads',
  initialState,
  reducers: {
    addFiles: (state, action: PayloadAction<FileUploadTask[]>) => {
      state.tasks.push(...action.payload);
    },
    setTaskId: (state, action: PayloadAction<{ fileName: string; taskId: string }>) => {
      const task = state.tasks.find((t) => t.name === action.payload.fileName);
      if (task) task.taskId = action.payload.taskId;
    },
    updateProgress: (state, action: PayloadAction<{ taskId: string; uploadedChunks: number }>) => {
      const task = state.tasks.find((t) => t.taskId === action.payload.taskId);
      if (task) {
        task.uploadedChunks = action.payload.uploadedChunks;
        task.progress = Math.round((task.uploadedChunks / (task.totalChunks ?? 1)) * 100);

        const totalTasks = state.tasks.length;
        const sumProgress = state.tasks.reduce((sum, t) => sum + t.progress, 0);
        state.overallProgress = Math.round(sumProgress / totalTasks);
      }
    },
    resetUploads: (state) => {
      state.tasks = [];
      state.overallProgress = 0;
    },
    removeFile: (state, action: PayloadAction<string>) => {
      state.tasks = state.tasks.filter((t) => t.name !== action.payload);
      const totalTasks = state.tasks.length;
      if (totalTasks === 0) {
        state.overallProgress = 0;
      } else {
        const sumProgress = state.tasks.reduce((sum, t) => sum + t.progress, 0);
        state.overallProgress = Math.round(sumProgress / totalTasks);
      }
    },
  },
});

export const { addFiles, setTaskId, updateProgress, resetUploads, removeFile } = uploadSlice.actions;
export default uploadSlice.reducer;
