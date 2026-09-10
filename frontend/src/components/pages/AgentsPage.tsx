'use client';

import { PageWrapper } from '@/components/layout';
import { Card } from '@/components/ui';
import type { AgentActivity } from '@/types';

interface AgentsPageProps {
  agents: AgentActivity[];
}

const statusStyles = {
  active: 'bg-green-500/20 text-green-400 animate-pulse',
  thinking: 'bg-yellow-500/20 text-yellow-400',
  error: 'bg-red-500/20 text-red-400',
  idle: 'bg-gray-500/20 text-gray-400',
};

export function AgentsPage({ agents }: AgentsPageProps) {
  return (
    <PageWrapper title="Agent Dashboard" scrollable>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent, idx) => (
          <Card
            key={agent.id}
            hover
            className="p-6 animate-slide-in"
            style={{ animationDelay: `${idx * 100}ms` }}
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white">{agent.name}</h3>
              <div
                className={`px-3 py-1 rounded-full text-xs font-semibold ${statusStyles[agent.status]}`}
              >
                {agent.status}
              </div>
            </div>
            <p className="text-gray-400 text-sm mb-4">{agent.lastAction}</p>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-500">Success Rate</span>
              <span className="text-purple-400 font-semibold">{agent.successRate}%</span>
            </div>
            <div className="mt-3 h-2 bg-gray-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-purple-500 to-cyan-500 transition-all duration-500"
                style={{ width: `${agent.successRate}%` }}
              />
            </div>
          </Card>
        ))}
      </div>
    </PageWrapper>
  );
}
