'use client';

import { useState, useEffect } from 'react';
import { PageWrapper } from '@/components/layout';
import { Card, Button, Input, Select } from '@/components/ui';
import type { UserSettings } from '@/types';

interface SettingsPageProps {
  settings: UserSettings | null;
  onSave: (settings: UserSettings) => void;
}

export function SettingsPage({ settings, onSave }: SettingsPageProps) {
  const [localSettings, setLocalSettings] = useState<UserSettings | null>(settings);

  useEffect(() => {
    setLocalSettings(settings);
  }, [settings]);

  const handleSave = () => {
    if (localSettings) {
      onSave(localSettings);
    }
  };

  if (!localSettings) {
    return (
      <PageWrapper title="Settings">
        <div className="flex items-center justify-center h-full">
          <p className="text-gray-400">Loading settings...</p>
        </div>
      </PageWrapper>
    );
  }

  return (
    <PageWrapper title="Settings" scrollable>
      <div className="max-w-3xl space-y-6">
        <Card className="p-6 space-y-4">
          <h3 className="text-xl font-semibold text-purple-400">User Profile</h3>
          <div>
            <label className="text-sm text-gray-400 block mb-2">Name</label>
            <Input
              type="text"
              value={localSettings.name}
              onChange={(e) =>
                setLocalSettings((s) => (s ? { ...s, name: e.target.value } : null))
              }
              placeholder="Your Name"
            />
          </div>
        </Card>

        <Card className="p-6 space-y-4">
          <h3 className="text-xl font-semibold text-purple-400">AI Persona</h3>
          <div>
            <label className="text-sm text-gray-400 block mb-2">Response Style</label>
            <Select
              value={localSettings.persona}
              onChange={(e) =>
                setLocalSettings((s) =>
                  s ? { ...s, persona: e.target.value as UserSettings['persona'] } : null
                )
              }
            >
              <option value="Casual & Friendly">Casual & Friendly</option>
              <option value="Professional">Professional</option>
              <option value="Concise & Direct">Concise & Direct</option>
            </Select>
          </div>
        </Card>

        <Card className="p-6 space-y-4">
          <h3 className="text-xl font-semibold text-red-400">Data Management</h3>
          <Button variant="danger">Delete All Data</Button>
        </Card>

        <Button onClick={handleSave} className="w-full py-4">
          Save Changes
        </Button>
      </div>
    </PageWrapper>
  );
}
