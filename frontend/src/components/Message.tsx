// Message component for displaying chat messages
'use client';

import { useState } from 'react';
import { ThumbsUp, ThumbsDown, Copy, ExternalLink, Clock, Target } from 'lucide-react';
import { cn, formatTimestamp, formatConfidence, getConfidenceColor, extractDocumentName } from '@/lib/utils';
import { FeedbackData, apiService } from '@/lib/api';

interface MessageProps {
  query: string;
  answer: string;
  sources: string[];
  links: string[];
  confidence: number;
  timestamp: string;
  isLoading?: boolean;
}

export default function Message({
  query,
  answer,
  sources,
  links,
  confidence,
  timestamp,
  isLoading = false,
}: MessageProps) {
  const [feedback, setFeedback] = useState<'thumbs_up' | 'thumbs_down' | null>(null);
  const [feedbackSent, setFeedbackSent] = useState(false);
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [feedbackComment, setFeedbackComment] = useState('');
  const [copied, setCopied] = useState(false);

  const handleFeedback = async (rating: 'thumbs_up' | 'thumbs_down') => {
    if (feedbackSent) return;

    setFeedback(rating);
    
    if (rating === 'thumbs_down') {
      setShowFeedbackForm(true);
    } else {
      await sendFeedback(rating);
    }
  };

  const sendFeedback = async (rating: 'thumbs_up' | 'thumbs_down', comment?: string) => {
    try {
      const feedbackData: FeedbackData = {
        query,
        answer,
        rating,
        comment: comment || '',
      };

      await apiService.sendFeedback(feedbackData);
      setFeedbackSent(true);
      setShowFeedbackForm(false);
      
      // Show success message briefly
      setTimeout(() => setFeedbackSent(false), 3000);
    } catch (error) {
      console.error('Error sending feedback:', error);
    }
  };

  const copyToClipboard = async () => {
    try {
      const textToCopy = `Q: ${query}\n\nA: ${answer}\n\nSources: ${sources.join(', ')}`;
      await navigator.clipboard.writeText(textToCopy);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-4 p-6 bg-white rounded-lg shadow-sm border border-gray-100">
        <div className="flex items-start space-x-3">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
            RA
          </div>
          <div className="flex-1">
            <div className="text-sm font-medium text-gray-900 mb-2">You asked:</div>
            <div className="text-gray-700 bg-gray-50 p-3 rounded-lg border-l-4 border-blue-500">
              {query}
            </div>
          </div>
        </div>
        
        <div className="flex items-start space-x-3">
          <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-teal-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
            🤖
          </div>
          <div className="flex-1">
            <div className="text-sm font-medium text-gray-900 mb-2">RAMate is thinking...</div>
            <div className="space-y-2">
              <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
              <div className="h-4 bg-gray-200 rounded animate-pulse w-3/4"></div>
              <div className="h-4 bg-gray-200 rounded animate-pulse w-1/2"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4 p-6 bg-white rounded-lg shadow-sm border border-gray-100">
      {/* User Query */}
      <div className="flex items-start space-x-3">
        <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
          RA
        </div>
        <div className="flex-1">
          <div className="text-sm font-medium text-gray-900 mb-2">You asked:</div>
          <div className="text-gray-700 bg-gray-50 p-3 rounded-lg border-l-4 border-blue-500">
            {query}
          </div>
        </div>
      </div>

      {/* RAMate Response */}
      <div className="flex items-start space-x-3">
        <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-teal-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
          🤖
        </div>
        <div className="flex-1">
          <div className="flex items-center justify-between mb-2">
            <div className="text-sm font-medium text-gray-900">RAMate:</div>
            <div className="flex items-center space-x-4 text-xs text-gray-500">
              <div className="flex items-center space-x-1">
                <Target className="w-3 h-3" />
                <span className={cn('font-medium', getConfidenceColor(confidence))}>
                  {formatConfidence(confidence)}
                </span>
              </div>
              <div className="flex items-center space-x-1">
                <Clock className="w-3 h-3" />
                <span>{formatTimestamp(timestamp)}</span>
              </div>
            </div>
          </div>
          
          <div className="prose prose-sm max-w-none text-gray-700 mb-4">
            {answer.split('\n').map((paragraph, index) => (
              <p key={index} className="mb-2 last:mb-0">
                {paragraph}
              </p>
            ))}
          </div>

          {/* Sources */}
          {sources.length > 0 && (
            <div className="mb-4">
              <div className="text-xs font-medium text-gray-600 mb-2">Sources:</div>
              <div className="space-y-1">
                {sources.map((source, index) => (
                  <div key={index} className="text-xs text-gray-600 bg-gray-50 px-2 py-1 rounded">
                    📄 {source}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Document Links */}
          {links.length > 0 && (
            <div className="mb-4">
              <div className="text-xs font-medium text-gray-600 mb-2">Documents:</div>
              <div className="space-y-1">
                {links.map((link, index) => (
                  <button
                    key={index}
                    onClick={() => window.open(link, '_blank')}
                    className="flex items-center space-x-2 text-xs text-blue-600 hover:text-blue-800 bg-blue-50 hover:bg-blue-100 px-2 py-1 rounded transition-colors"
                  >
                    <ExternalLink className="w-3 h-3" />
                    <span>{extractDocumentName(link)}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex items-center justify-between pt-3 border-t border-gray-100">
            <div className="flex items-center space-x-2">
              <button
                onClick={() => handleFeedback('thumbs_up')}
                className={cn(
                  'p-2 rounded-full transition-colors',
                  feedback === 'thumbs_up'
                    ? 'bg-green-100 text-green-600'
                    : 'hover:bg-gray-100 text-gray-400 hover:text-gray-600'
                )}
                disabled={feedbackSent}
              >
                <ThumbsUp className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleFeedback('thumbs_down')}
                className={cn(
                  'p-2 rounded-full transition-colors',
                  feedback === 'thumbs_down'
                    ? 'bg-red-100 text-red-600'
                    : 'hover:bg-gray-100 text-gray-400 hover:text-gray-600'
                )}
                disabled={feedbackSent}
              >
                <ThumbsDown className="w-4 h-4" />
              </button>
              {feedbackSent && (
                <span className="text-xs text-green-600 font-medium">Thank you for your feedback!</span>
              )}
            </div>
            
            <button
              onClick={copyToClipboard}
              className="flex items-center space-x-1 text-xs text-gray-500 hover:text-gray-700 transition-colors"
            >
              <Copy className="w-3 h-3" />
              <span>{copied ? 'Copied!' : 'Copy'}</span>
            </button>
          </div>

          {/* Feedback Form */}
          {showFeedbackForm && (
            <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <div className="text-sm font-medium text-gray-900 mb-2">
                Help us improve! What could have been better?
              </div>
              <textarea
                value={feedbackComment}
                onChange={(e) => setFeedbackComment(e.target.value)}
                placeholder="Your feedback..."
                className="w-full p-2 text-sm border border-gray-300 rounded-md resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
              />
              <div className="flex justify-end space-x-2 mt-2">
                <button
                  onClick={() => setShowFeedbackForm(false)}
                  className="px-3 py-1 text-xs text-gray-600 hover:text-gray-800"
                >
                  Cancel
                </button>
                <button
                  onClick={() => sendFeedback('thumbs_down', feedbackComment)}
                  className="px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Send Feedback
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
