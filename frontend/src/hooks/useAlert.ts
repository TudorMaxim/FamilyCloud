import { useState, useEffect } from 'react';

const useAlert = () => {
  const [alert, setAlert] = useState<string | null>(null);
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      setAlert(null);
    }, 5000);

    return () => {
      clearTimeout(timeoutId);
    };
  });
  return { alert, setAlert };
};

export default useAlert;
