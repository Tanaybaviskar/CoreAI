import { ReactNode, CSSProperties } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  style?: CSSProperties;
}

export function Card({ children, className = '', hover = false, style }: CardProps) {
  return (
    <div
      className={`
        glass rounded-2xl
        ${hover ? 'glass-hover' : ''}
        ${className}
      `}
      style={style}
    >
      {children}
    </div>
  );
}

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle: string;
  icon?: ReactNode;
  color?: 'purple' | 'cyan' | 'pink' | 'green' | 'blue';
}

const colorClasses = {
  purple: { text: 'text-purple-400', bg: 'bg-purple-500/20' },
  cyan: { text: 'text-cyan-400', bg: 'bg-cyan-500/20' },
  pink: { text: 'text-pink-400', bg: 'bg-pink-500/20' },
  green: { text: 'text-green-400', bg: 'bg-green-500/20' },
  blue: { text: 'text-blue-400', bg: 'bg-blue-500/20' },
};

export function StatCard({ title, value, subtitle, icon, color = 'purple' }: StatCardProps) {
  const colors = colorClasses[color];

  return (
    <Card hover className="p-6 animate-slide-in">
      <div className="flex items-start justify-between mb-4">
        <div>
          <p className="text-gray-400 text-sm font-medium mb-1">{title}</p>
          <h3 className={`text-3xl font-bold ${colors.text}`}>{value}</h3>
        </div>
        {icon && (
          <div className={`p-3 ${colors.bg} rounded-lg ${colors.text}`}>{icon}</div>
        )}
      </div>
      <p className="text-gray-500 text-sm">{subtitle}</p>
    </Card>
  );
}
