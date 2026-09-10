'use client';

import { PageWrapper } from '@/components/layout';
import { Card, Button } from '@/components/ui';
import type { MemoryItem } from '@/types';

interface MemoryPageProps {
  memoryItems: MemoryItem[] | null;
}

export function MemoryPage({ memoryItems }: MemoryPageProps) {
  return (
    <PageWrapper title="Assistant Memory" scrollable>
      <div className="max-w-3xl space-y-3">
        {(memoryItems || []).map((item, idx) => (
          <Card
            key={item.id}
            hover
            className="p-5 flex justify-between items-center animate-slide-in"
            style={{ animationDelay: `${idx * 50}ms` }}
          >
            <div>
              <p className="text-sm text-purple-400 font-semibold mb-1">{item.key}</p>
              <p className="text-white">{item.value}</p>
            </div>
            <Button variant="ghost" size="sm">
              Edit
            </Button>
          </Card>
        ))}
        {(!memoryItems || memoryItems.length === 0) && (
          <div className="text-center py-12 text-gray-400">
            <p>No memory items stored yet.</p>
          </div>
        )}
      </div>
    </PageWrapper>
  );
}
