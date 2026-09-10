'use client';

import { BellIcon, CloseIcon } from '@/components/ui';
import type { ActivityItem } from '@/types';

interface HeaderProps {
  title: string;
  activityCount?: number;
  onToggleActivity: () => void;
}

export function Header({ title, activityCount = 0, onToggleActivity }: HeaderProps) {
  return (
    <header className="flex-shrink-0 p-6 flex items-center justify-between z-10 glass border-b border-purple-500/20">
      <div className="flex items-center gap-4">
        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 animate-gradient">
          {title}
        </h1>
      </div>
      <button
        onClick={onToggleActivity}
        className="p-3 rounded-xl hover:bg-white/10 transition-all relative transform hover:scale-105"
      >
        <BellIcon className="w-6 h-6 text-gray-300" />
        {activityCount > 0 && (
          <span className="absolute top-2 right-2 block h-3 w-3 rounded-full bg-cyan-400 ring-2 ring-[#020010] animate-pulse" />
        )}
      </button>
    </header>
  );
}

interface ActivityPanelProps {
  activities: ActivityItem[];
  onClose: () => void;
}

export function ActivityPanel({ activities, onClose }: ActivityPanelProps) {
  return (
    <div className="absolute top-24 right-4 w-96 glass rounded-2xl shadow-2xl z-50 animate-fade-in p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-white text-lg">Activity Feed</h3>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-white transition-colors p-1"
        >
          <CloseIcon className="w-5 h-5" />
        </button>
      </div>
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {activities.map((item, idx) => (
          <div
            key={item.id}
            className="p-3 rounded-lg bg-gray-800/30 hover:bg-gray-800/50 transition-colors animate-slide-in"
            style={{ animationDelay: `${idx * 50}ms` }}
          >
            <p className="text-xs text-gray-400">{item.time}</p>
            <p className="text-sm text-gray-200 mt-1">{item.text}</p>
          </div>
        ))}
        {activities.length === 0 && (
          <p className="text-gray-400 text-center py-4">No recent activity</p>
        )}
      </div>
    </div>
  );
}
