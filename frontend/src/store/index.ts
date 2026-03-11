import { configureStore } from '@reduxjs/toolkit';
import uploadReducer from '../features/uploads/slice';
import authReducer from '../features/auth/slice';

export const store = configureStore({
  reducer: {
    uploads: uploadReducer,
    auth: authReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
