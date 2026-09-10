'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import type { DashboardData, MemoryItem, ActivityItem, UserSettings, AgentActivity } from '@/types';

const DEFAULT_AGENTS: AgentActivity[] = [
  { id: '1', name: 'Calendar Agent', status: 'idle', lastAction: 'Ready to schedule', successRate: 98 },
  { id: '2', name: 'Email Agent', status: 'idle', lastAction: 'Ready to manage emails', successRate: 95 },
  { id: '3', name: 'Meeting Agent', status: 'idle', lastAction: 'Ready to coordinate', successRate: 97 },
  { id: '4', name: 'Weather Agent', status: 'active', lastAction: 'Fetching forecast', successRate: 99 },
  { id: '5', name: 'News Agent', status: 'active', lastAction: 'Aggregating headlines', successRate: 96 },
  { id: '6', name: 'Task Agent', status: 'idle', lastAction: 'Ready to organize tasks', successRate: 94 },
];

const DEFAULT_SETTINGS: UserSettings = {
  name: 'User',
  persona: 'Casual & Friendly',
};

interface AppData {
  dashboard: DashboardData | null;
  memory: MemoryItem[] | null;
  activity: ActivityItem[] | null;
  settings: UserSettings;
  agents: AgentActivity[];
  isLoading: boolean;
  error: string | null;
}

export function useAppData() {
  const [data, setData] = useState<AppData>({
    dashboard: null,
    memory: null,
    activity: null,
    settings: DEFAULT_SETTINGS,
    agents: DEFAULT_AGENTS,
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    async function fetchData() {
      try {
        const [dashboard, memory, activity] = await Promise.all([
          api.getDashboard(),
          api.getMemory(),
          api.getActivity(),
        ]);

        setData((prev) => ({
          ...prev,
          dashboard,
          memory,
          activity,
          isLoading: false,
        }));
      } catch (error) {
        console.error('Failed to fetch data:', error);
        setData((prev) => ({
          ...prev,
          isLoading: false,
          error: 'Failed to connect to backend',
        }));
      }
    }

    fetchData();
  }, []);

  const updateSettings = (settings: UserSettings) => {
    setData((prev) => ({ ...prev, settings }));
  };

  return {
    ...data,
    updateSettings,
  };
}
