import { configureStore } from '@reduxjs/toolkit';
import uploadReducer from '../features/uploads/slice';

export const store = configureStore({
  reducer: {
    uploads: uploadReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
