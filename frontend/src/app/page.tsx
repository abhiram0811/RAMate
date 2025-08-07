'use client';

import { useState, useEffect, useRef } from 'react';
import { BookOpen, MessageSquare, AlertCircle } from 'lucide-react';
import ChatInput from '@/components/ChatInput';
import Message from '@/components/Message';
import StatusIndicator from '@/components/StatusIndicator';
import { apiService, ChatResponse } from '@/lib/api';
import { generateSessionId } from '@/lib/utils';

interface ChatMessage {
  id: string;
  query: string;
  answer: string;
  sources: string[];
  links: string[];
  confidence: number;
  timestamp: string;
  isLoading?: boolean;
}

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => generateSessionId());
  const [apiAvailable, setApiAvailable] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Check API availability on mount
  useEffect(() => {
    checkApiAvailability();
  }, []);

  const checkApiAvailability = async () => {
    const available = await apiService.isApiAvailable();
    setApiAvailable(available);
  };

  const handleSendMessage = async (query: string) => {
    if (!query.trim() || isLoading) return;

    // Add loading message
    const loadingMessageId = Date.now().toString();
    const loadingMessage: ChatMessage = {
      id: loadingMessageId,
      query,
      answer: '',
      sources: [],
      links: [],
      confidence: 0,
      timestamp: new Date().toISOString(),
      isLoading: true,
    };

    setMessages((prev) => [...prev, loadingMessage]);
    setIsLoading(true);

    try {
      const response: ChatResponse = await apiService.sendChatMessage({
        query,
        session_id: sessionId,
      });

      // Remove loading message and add real response
      setMessages((prev) => {
        const filtered = prev.filter((msg) => msg.id !== loadingMessageId);
        
        if (response.status === 'success' && response.data) {
          const newMessage: ChatMessage = {
            id: Date.now().toString(),
            query: response.data.query,
            answer: response.data.answer,
            sources: response.data.sources,
            links: response.data.links,
            confidence: response.data.confidence,
            timestamp: response.data.timestamp,
          };
          return [...filtered, newMessage];
        } else {
          // Error response
          const errorMessage: ChatMessage = {
            id: Date.now().toString(),
            query,
            answer: response.message || 'Sorry, I encountered an error processing your request. Please try again.',
            sources: [],
            links: [],
            confidence: 0,
            timestamp: new Date().toISOString(),
          };
          return [...filtered, errorMessage];
        }
      });
    } catch (error) {
      // Remove loading message and add error message
      setMessages((prev) => {
        const filtered = prev.filter((msg) => msg.id !== loadingMessageId);
        const errorMessage: ChatMessage = {
          id: Date.now().toString(),
          query,
          answer: 'Sorry, I couldn\'t connect to the RAMate API. Please check if the backend server is running and try again.',
          sources: [],
          links: [],
          confidence: 0,
          timestamp: new Date().toISOString(),
        };
        return [...filtered, errorMessage];
      });
      
      setApiAvailable(false);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">RAMate</h1>
                <p className="text-sm text-gray-600">Your RA Assistant at Colorado State University</p>
              </div>
            </div>
            <StatusIndicator />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-6">
        {!apiAvailable && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-red-600" />
              <div>
                <div className="font-medium text-red-900">API Connection Error</div>
                <div className="text-sm text-red-700">
                  Cannot connect to RAMate backend. Please ensure the API server is running on localhost:5000.
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Welcome Message */}
        {messages.length === 0 && (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-teal-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <MessageSquare className="w-8 h-8 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Welcome to RAMate! 👋
            </h2>
            <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
              I\'m your AI assistant here to help you find information from your RA training documents. 
              Ask me about policies, procedures, emergency protocols, or anything from your training materials!
            </p>
            <div className="text-sm text-gray-500">
              💡 Try asking about emergency procedures, prohibited items, or duty protocols
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="space-y-6 mb-6">
          {messages.map((message) => (
            <Message
              key={message.id}
              query={message.query}
              answer={message.answer}
              sources={message.sources}
              links={message.links}
              confidence={message.confidence}
              timestamp={message.timestamp}
              isLoading={message.isLoading}
            />
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Chat Input */}
        <div className="sticky bottom-0 bg-gradient-to-t from-white via-white to-transparent pt-6">
          <ChatInput
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            disabled={!apiAvailable}
            placeholder={
              apiAvailable
                ? "Ask RAMate about RA policies, procedures, or training materials..."
                : "API connection required to send messages..."
            }
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white mt-12">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="text-center text-sm text-gray-500">
            <p className="mb-2">
              RAMate v1.0.0 - AI-powered RA assistance for Colorado State University
            </p>
            <p>
              Built with ❤️ for Resident Assistants • Powered by OpenRouter & ChromaDB
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
