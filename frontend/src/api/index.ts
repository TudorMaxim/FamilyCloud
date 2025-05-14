import type { UserCredentials, UserRegistrationData } from './types';

class FamilyCloudAPI {
  async login(credentials: UserCredentials) {
    const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/login`, {
      method: 'POST',
      credentials: 'include',
      body: JSON.stringify(credentials),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error();
    }
    return data;
  }

  async logout() {
    const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/logout`, {
      method: 'POST',
      credentials: 'include',
    });
    return await res.json();
  }

  async register(data: UserRegistrationData) {
    const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/login`, {
      method: 'POST',
      credentials: 'include',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return await res.json();
  }

  async getCurrentUser() {
    const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/me`, {
      credentials: 'include',
    });

    if (!res.ok) return null;
    return await res.json();
  }
}

const familyCloudAPI = new FamilyCloudAPI();

export default familyCloudAPI;
