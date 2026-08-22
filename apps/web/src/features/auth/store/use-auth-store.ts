import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { LoginResponse } from '../types';

interface AuthState {
  user: LoginResponse | null;
  isAuthModalOpen: boolean;
  setUser: (user: LoginResponse | null) => void;
  openAuthModal: () => void;
  closeAuthModal: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthModalOpen: false,

      setUser: (user) => set({ user }),
      openAuthModal: () => set({ isAuthModalOpen: true }),
      closeAuthModal: () => set({ isAuthModalOpen: false }),
    }),
    {
      name: 'vzticket-user',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ user: state.user }),
    }
  )
);