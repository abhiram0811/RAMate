// Chat input component for sending messages
'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
  disabled?: boolean;
  placeholder?: string;
}

export default function ChatInput({
  onSendMessage,
  isLoading = false,
  disabled = false,
  placeholder = "Ask RAMate about RA policies, procedures, or training materials...",
}: ChatInputProps) {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const trimmedMessage = message.trim();
    if (!trimmedMessage || isLoading || disabled) return;
    
    onSendMessage(trimmedMessage);
    setMessage('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const exampleQuestions = [
    "What are the emergency evacuation procedures?",
    "What items are prohibited in residence halls?",
    "How do I handle a noise complaint?",
    "What should I do during duty rounds?",
    "What are the assembly areas for emergencies?"
  ];

  return (
    <div className="space-y-4">
      {/* Example Questions */}
      {message === '' && (
        <div className="flex flex-wrap gap-2 px-4">
          <div className="text-xs text-gray-500 w-full mb-2">Try asking:</div>
          {exampleQuestions.map((question, index) => (
            <button
              key={index}
              onClick={() => setMessage(question)}
              className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-full transition-colors border border-gray-200 hover:border-gray-300"
              disabled={isLoading || disabled}
            >
              {question}
            </button>
          ))}
        </div>
      )}

      {/* Chat Input Form */}
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative flex items-end space-x-3 p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
          <div className="flex-1">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              disabled={isLoading || disabled}
              className={cn(
                "w-full p-3 text-sm border border-gray-300 rounded-lg resize-none",
                "focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder-gray-400 bg-gray-50",
                "min-h-[44px] max-h-[120px]",
                (isLoading || disabled) && "opacity-50 cursor-not-allowed"
              )}
              rows={1}
            />
          </div>
          
          <button
            type="submit"
            disabled={!message.trim() || isLoading || disabled}
            className={cn(
              "p-3 rounded-lg transition-all duration-200",
              "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
              message.trim() && !isLoading && !disabled
                ? "bg-blue-600 hover:bg-blue-700 text-white shadow-sm hover:shadow-md"
                : "bg-gray-200 text-gray-400 cursor-not-allowed"
            )}
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
        
        <div className="flex justify-between items-center px-4 pt-2">
          <div className="text-xs text-gray-400">
            Press Enter to send, Shift+Enter for new line
          </div>
          <div className="text-xs text-gray-400">
            {message.length}/1000
          </div>
        </div>
      </form>
    </div>
  );
}
