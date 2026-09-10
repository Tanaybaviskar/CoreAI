import { ReactNode } from 'react';

interface PageWrapperProps {
  title: string;
  children: ReactNode;
  scrollable?: boolean;
}

export function PageWrapper({ title, children, scrollable = false }: PageWrapperProps) {
  return (
    <div className="animate-fade-in h-full flex flex-col p-8 min-h-0">
      <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 mb-6 flex-shrink-0 animate-gradient">
        {title}
      </h1>
      <div className={`flex-1 min-h-0 ${scrollable ? 'overflow-y-auto' : 'overflow-hidden'}`}>
        {children}
      </div>
    </div>
  );
}
