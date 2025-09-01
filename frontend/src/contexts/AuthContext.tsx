'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User, LoginRequest, Igreja, Campus } from '@/types';
import apiClient from '@/lib/api';

interface AuthContextType {
  user: User | null;
  igreja: Igreja | null;
  campus: Campus | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => Promise<void>;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [igreja, setIgreja] = useState<Igreja | null>(null);
  const [campus, setCampus] = useState<Campus | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user && apiClient.isAuthenticated();

  const login = async (credentials: LoginRequest) => {
    try {
      setIsLoading(true);
      const response = await apiClient.login(credentials);
      setUser(response.user);
      await loadTenantData();
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      await apiClient.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setIgreja(null);
      setCampus(null);
    }
  };

  const refreshProfile = async () => {
    try {
      const profile = await apiClient.getProfile();
      setUser(profile);
      await loadTenantData();
    } catch (error) {
      console.error('Profile refresh error:', error);
      await logout();
    }
  };

  const loadTenantData = async () => {
    try {
      const igrejas = await apiClient.get<{ results: Igreja[] }>('/api/core/igrejas/');
      if (igrejas.results.length > 0) {
        setIgreja(igrejas.results[0]);
      }

      const campusData = await apiClient.get<{ results: Campus[] }>('/api/core/campus/');
      if (campusData.results.length > 0) {
        setCampus(campusData.results[0]);
      }
    } catch (error) {
      console.error('Error loading tenant data:', error);
    }
  };

  useEffect(() => {
    const initializeAuth = async () => {
      if (apiClient.isAuthenticated()) {
        try {
          await refreshProfile();
        } catch (error) {
          console.error('Auth initialization error:', error);
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  const value: AuthContextType = {
    user,
    igreja,
    campus,
    isLoading,
    isAuthenticated,
    login,
    logout,
    refreshProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
