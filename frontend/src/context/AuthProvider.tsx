import React from 'react';
import familyCloudAPI from '../api';
import { AuthContext } from './AuthContext';
import type { User } from './types';

function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = React.useState<User | null>(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    familyCloudAPI
      .getCurrentUser()
      .then((user) => {
        setUser(user);
      })
      .finally(() => setLoading(false));
  }, []);

  return <AuthContext.Provider value={{ user, loading, setUser }}>{children}</AuthContext.Provider>;
}

export default AuthProvider;
