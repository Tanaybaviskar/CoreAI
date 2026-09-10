'use client';

import { useRef, useEffect } from 'react';
import { SendIcon, Markdown } from '@/components/ui';
import type { Message } from '@/types';

interface ChatPageProps {
  messages: Message[];
  input: string;
  onInputChange: (value: string) => void;
  onSend: () => void;
  isLoading: boolean;
}

export function ChatPage({ messages, input, onInputChange, onSend, isLoading }: ChatPageProps) {
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div className="h-full flex flex-col min-h-0">
      <main className="flex-1 overflow-y-auto p-6 min-h-0">
        <div className="max-w-4xl mx-auto space-y-6">
          {messages.map((msg, idx) => (
            <div
              key={msg.id}
              className={`flex items-start gap-4 ${msg.sender === 'user' ? 'justify-end' : ''} animate-fade-in`}
              style={{ animationDelay: `${idx * 50}ms` }}
            >
              {msg.sender === 'assistant' && (
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-600 via-pink-600 to-cyan-500 flex-shrink-0 flex items-center justify-center text-white font-bold animate-gradient">
                  A
                </div>
              )}
              <div
                className={`max-w-2xl rounded-2xl p-4 shadow-lg ${
                  msg.sender === 'user'
                    ? 'bg-gradient-to-br from-blue-600 to-blue-500 text-white'
                    : 'glass text-white'
                }`}
              >
                {msg.agent && <div className="text-xs text-purple-300 mb-2">{msg.agent}</div>}
                {msg.sender === 'user' ? (
                  <p className="whitespace-pre-wrap leading-relaxed">{msg.text}</p>
                ) : (
                  <Markdown content={msg.text} />
                )}
              </div>
              {msg.sender === 'user' && (
                <div className="w-10 h-10 rounded-xl bg-blue-600 flex-shrink-0 flex items-center justify-center text-white font-bold">
                  U
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex items-start gap-4 animate-fade-in">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-600 to-cyan-500 flex-shrink-0 animate-pulse" />
              <div className="glass rounded-2xl p-4">
                <div className="flex gap-2">
                  <div
                    className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"
                    style={{ animationDelay: '0ms' }}
                  />
                  <div
                    className="w-2 h-2 bg-pink-400 rounded-full animate-bounce"
                    style={{ animationDelay: '150ms' }}
                  />
                  <div
                    className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce"
                    style={{ animationDelay: '300ms' }}
                  />
                </div>
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>
      </main>

      <footer className="p-6 bg-transparent flex-shrink-0">
        <div className="max-w-4xl mx-auto">
          <div className="relative glass rounded-full p-2">
            <input
              type="text"
              value={input}
              onChange={(e) => onInputChange(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask CoreAI anything..."
              disabled={isLoading}
              className="w-full bg-transparent border-none py-3 pl-6 pr-16 text-white placeholder:text-gray-500 focus:outline-none"
            />
            <button
              onClick={onSend}
              disabled={isLoading || !input.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed p-3 rounded-full transition-all transform hover:scale-105 active:scale-95"
            >
              <SendIcon className="w-5 h-5 text-white" />
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}
