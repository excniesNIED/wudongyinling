import { defineStore } from 'pinia';
import { ref } from 'vue';
import { login as apiLogin, getInfo } from '@/api/auth';

export const useUserStore = defineStore('user', () => {
  const user = ref(null);
  const token = ref(localStorage.getItem('user-token') || '');
  const isLoggedIn = ref(!!token.value);

  async function login(userInfo) {
    const response = await apiLogin(userInfo);
    if (response.access_token) {
      token.value = response.access_token;
      localStorage.setItem('user-token', token.value);
      isLoggedIn.value = true;
      // Optionally, fetch user info right after login
      await fetchUserInfo();
      return 'ok';
    } else {
      throw new Error(response.detail || 'Login failed');
    }
  }

  async function fetchUserInfo() {
    try {
      const userInfo = await getInfo();
      user.value = userInfo;
    } catch (error) {
      console.error('Failed to fetch user info:', error);
      logout(); // Log out if user info fetch fails
    }
  }

  function logout() {
    user.value = null;
    token.value = '';
    isLoggedIn.value = false;
    localStorage.removeItem('user-token');
  }

  return {
    user,
    token,
    isLoggedIn,
    login,
    logout,
    fetchUserInfo
  };
});