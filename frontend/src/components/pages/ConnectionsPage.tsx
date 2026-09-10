'use client';

import { useState } from 'react';
import { PageWrapper } from '@/components/layout';
import { Card, Button, GoogleIcon, MicrosoftIcon, SlackIcon, ActivityIcon, DashboardIcon } from '@/components/ui';
import type { Connection } from '@/types';
import { ReactNode } from 'react';

interface ConnectionItemProps {
  icon: ReactNode;
  name: string;
  description: string;
  connected: boolean;
  onToggle: () => void;
}

function ConnectionItem({ icon, name, description, connected, onToggle }: ConnectionItemProps) {
  return (
    <Card hover className="p-6 flex items-center justify-between animate-slide-in">
      <div className="flex items-center gap-4">
        <div className="w-12 h-12 rounded-xl bg-gray-800/50 flex items-center justify-center">
          {icon}
        </div>
        <div>
          <div className="font-semibold text-white flex items-center gap-2">
            {name}
            {connected && <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />}
          </div>
          <div className="text-sm text-gray-400">{description}</div>
        </div>
      </div>
      <Button
        variant={connected ? 'danger' : 'primary'}
        size="sm"
        onClick={onToggle}
        className="rounded-full px-6"
      >
        {connected ? 'Disconnect' : 'Connect'}
      </Button>
    </Card>
  );
}

export function ConnectionsPage() {
  const [connections, setConnections] = useState<Connection>({
    google: true,
    microsoft: false,
    slack: false,
    weather: true,
    news: true,
  });

  const toggleConnection = (service: keyof Connection) => {
    setConnections((prev) => ({ ...prev, [service]: !prev[service] }));
  };

  return (
    <PageWrapper title="Manage Connections" scrollable>
      <div className="max-w-3xl space-y-4">
        <ConnectionItem
          icon={<GoogleIcon className="w-6 h-6 text-white" />}
          name="Google Workspace"
          description="Calendar, Gmail, Meet"
          connected={connections.google}
          onToggle={() => toggleConnection('google')}
        />
        <ConnectionItem
          icon={<MicrosoftIcon className="w-6 h-6 text-white" />}
          name="Microsoft 365"
          description="Outlook, Teams, OneDrive"
          connected={connections.microsoft}
          onToggle={() => toggleConnection('microsoft')}
        />
        <ConnectionItem
          icon={<SlackIcon className="w-6 h-6 text-white" />}
          name="Slack"
          description="Team communication"
          connected={connections.slack}
          onToggle={() => toggleConnection('slack')}
        />
        <ConnectionItem
          icon={<ActivityIcon className="w-6 h-6 text-white" />}
          name="Weather API"
          description="Real-time weather data"
          connected={connections.weather}
          onToggle={() => toggleConnection('weather')}
        />
        <ConnectionItem
          icon={<DashboardIcon className="w-6 h-6 text-white" />}
          name="News API"
          description="Latest news updates"
          connected={connections.news}
          onToggle={() => toggleConnection('news')}
        />
      </div>
    </PageWrapper>
  );
}
