import { createSlice, type PayloadAction } from '@reduxjs/toolkit';
export type User = {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
};

export type AuthState = {
  user?: User | null;
  loading: boolean;
  authenticated?: boolean;
};

const initialState: AuthState = {
  loading: false,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User | null>) => {
      state.user = action.payload;
      state.authenticated = !!action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
  },
});

export const { setUser, setLoading } = authSlice.actions;
export default authSlice.reducer;
