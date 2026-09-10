export interface Message {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  agent?: string;
}

export type Page = 'dashboard' | 'chat' | 'agents' | 'connections' | 'memory' | 'settings';

export interface MemoryItem {
  id: string;
  key: string;
  value: string;
}

export interface ActivityItem {
  id: string;
  time: string;
  text: string;
  type?: 'success' | 'info' | 'warning' | 'error';
}

export interface AgentActivity {
  id: string;
  name: string;
  status: 'idle' | 'active' | 'thinking' | 'error';
  lastAction: string;
  successRate: number;
}

export interface DashboardData {
  totalConversations: number;
  activeAgents: number;
  apiCallsToday: number;
  successRate: number;
  recentActivity: ActivityItem[];
}

export interface UserSettings {
  name: string;
  persona: 'Casual & Friendly' | 'Professional' | 'Concise & Direct';
}

export interface Connection {
  google: boolean;
  microsoft: boolean;
  slack: boolean;
  weather: boolean;
  news: boolean;
}
