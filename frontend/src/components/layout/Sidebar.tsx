'use client';

import type { Page } from '@/types';
import {
  DashboardIcon,
  ChatIcon,
  AgentsIcon,
  ConnectionsIcon,
  MemoryIcon,
  SettingsIcon,
} from '@/components/ui';

interface NavItem {
  id: Page;
  name: string;
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
}

const navItems: NavItem[] = [
  { id: 'dashboard', name: 'Dashboard', icon: DashboardIcon },
  { id: 'chat', name: 'Chat', icon: ChatIcon },
  { id: 'agents', name: 'Agents', icon: AgentsIcon },
  { id: 'connections', name: 'Connections', icon: ConnectionsIcon },
  { id: 'memory', name: 'Memory', icon: MemoryIcon },
  { id: 'settings', name: 'Settings', icon: SettingsIcon },
];

interface SidebarProps {
  active: Page;
  onNavigate: (page: Page) => void;
}

export function Sidebar({ active, onNavigate }: SidebarProps) {
  return (
    <nav className="h-full w-20 bg-gray-900/50 backdrop-blur-xl border-r border-purple-500/20 p-4 flex flex-col items-center justify-between">
      <div className="w-full flex flex-col items-center">
        <div className="w-12 h-12 bg-gradient-to-br from-purple-600 via-pink-600 to-cyan-500 rounded-xl mb-12 flex items-center justify-center text-white font-bold text-xl animate-gradient">
          C
        </div>

        <ul className="space-y-4 w-full">
          {navItems.map((item, idx) => {
            const Icon = item.icon;
            const isActive = active === item.id;

            return (
              <li
                key={item.id}
                style={{ animationDelay: `${idx * 50}ms` }}
                className="animate-slide-in"
              >
                <button
                  onClick={() => onNavigate(item.id)}
                  className={`
                    w-full p-3 rounded-xl transition-all duration-300
                    ${
                      isActive
                        ? 'bg-purple-600/50 text-white shadow-lg shadow-purple-500/50 scale-110'
                        : 'text-gray-400 hover:bg-white/10 hover:text-white hover:scale-105'
                    }
                  `}
                  title={item.name}
                >
                  <Icon className="w-6 h-6 mx-auto" />
                </button>
              </li>
            );
          })}
        </ul>
      </div>

      <div className="w-10 h-10 bg-green-500/20 rounded-full border-2 border-green-500/30 flex items-center justify-center">
        <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
      </div>
    </nav>
  );
}
