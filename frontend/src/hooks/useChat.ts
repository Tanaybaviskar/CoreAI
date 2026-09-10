'use client';

import { useState, useCallback, useMemo } from 'react';
import { api } from '@/lib/api';
import type { Message } from '@/types';

const WELCOME_MESSAGE: Message = {
  id: 'init',
  sender: 'assistant',
  text: "Welcome to CoreAI! I'm your enterprise AI assistant powered by specialized agents. How can I help you today?",
};

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([WELCOME_MESSAGE]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const threadId = useMemo(() => `thread_${crypto.randomUUID()}`, []);

  const sendMessage = useCallback(async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      sender: 'user',
      text: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    const assistantMessageId = crypto.randomUUID();
    setMessages((prev) => [...prev, { id: assistantMessageId, sender: 'assistant', text: '' }]);

    try {
      let fullText = '';
      await api.sendMessage(input, threadId, (chunk) => {
        fullText += chunk;
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMessageId ? { ...msg, text: fullText } : msg
          )
        );
      });
    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMessageId
            ? { ...msg, text: 'Connection error. Please check if the backend is running.' }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, threadId]);

  return {
    messages,
    input,
    setInput,
    sendMessage,
    isLoading,
  };
}
