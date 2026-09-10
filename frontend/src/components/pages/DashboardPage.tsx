'use client';

import { useState, useEffect } from 'react';
import { PageWrapper } from '@/components/layout';
import { Card, StatCard, ChatIcon, AgentsIcon, ActivityIcon, CheckIcon } from '@/components/ui';
import type { DashboardData, UserSettings, ActivityItem } from '@/types';

interface DashboardPageProps {
  data: DashboardData | null;
  settings: UserSettings | null;
}

export function DashboardPage({ data, settings }: DashboardPageProps) {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const greeting = () => {
    const hour = time.getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 18) return 'Good Afternoon';
    return 'Good Evening';
  };

  const getActivityDotColor = (type?: ActivityItem['type']) => {
    switch (type) {
      case 'success':
        return 'bg-green-400';
      case 'warning':
        return 'bg-yellow-400';
      case 'error':
        return 'bg-red-400';
      default:
        return 'bg-blue-400';
    }
  };

  return (
    <PageWrapper title={`${greeting()}, ${settings?.name || 'User'}`} scrollable>
      <div className="space-y-6">
        <Card className="p-8 text-center">
          <div className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400 animate-gradient">
            {time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
          </div>
          <div className="text-gray-400 mt-2">
            {time.toLocaleDateString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </div>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            title="Conversations"
            value={data?.totalConversations || 0}
            subtitle="Total interactions"
            icon={<ChatIcon className="w-6 h-6" />}
            color="purple"
          />
          <StatCard
            title="Active Agents"
            value={data?.activeAgents || 0}
            subtitle="Running now"
            icon={<AgentsIcon className="w-6 h-6" />}
            color="cyan"
          />
          <StatCard
            title="API Calls"
            value={data?.apiCallsToday || 0}
            subtitle="Today"
            icon={<ActivityIcon className="w-6 h-6" />}
            color="pink"
          />
          <StatCard
            title="Success Rate"
            value={`${data?.successRate || 0}%`}
            subtitle="System reliability"
            icon={<CheckIcon className="w-6 h-6" />}
            color="green"
          />
        </div>

        <Card className="p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <ActivityIcon className="w-5 h-5 text-purple-400" />
            Recent Activity
          </h3>
          <div className="space-y-3">
            {(data?.recentActivity || []).map((activity, idx) => (
              <div
                key={activity.id || idx}
                className="flex items-start gap-3 p-3 rounded-lg bg-gray-800/30 hover:bg-gray-800/50 transition-colors"
              >
                <div className={`w-2 h-2 rounded-full mt-2 ${getActivityDotColor(activity.type)}`} />
                <div className="flex-1">
                  <p className="text-gray-300">{activity.text}</p>
                  <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
                </div>
              </div>
            ))}
            {(!data?.recentActivity || data.recentActivity.length === 0) && (
              <p className="text-gray-400 text-center py-4">No recent activity</p>
            )}
          </div>
        </Card>
      </div>
    </PageWrapper>
  );
}
