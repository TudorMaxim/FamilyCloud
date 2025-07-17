import React from 'react';
import type { User } from './types';

type AuthContextType = {
  user: User | null;
  loading: boolean;
  setUser: (user: User | null) => void;
};

export const AuthContext = React.createContext<AuthContextType | undefined>(undefined);
