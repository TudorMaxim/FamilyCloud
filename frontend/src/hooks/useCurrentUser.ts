import React from 'react';
import { useDispatch } from 'react-redux';
import type { AppDispatch } from '../store';
import familyCloudAPI from '../api';
import { setUser, setLoading } from '../features/auth/slice';

const useCurrentUser = () => {
  const dispatch = useDispatch<AppDispatch>();
  React.useEffect(() => {
    dispatch(setLoading(true));
    familyCloudAPI
      .getCurrentUser()
      .then((user) => {
        dispatch(setUser(user));
      })
      .finally(() => dispatch(setLoading(false)));
  }, [dispatch]);
};

export default useCurrentUser;
