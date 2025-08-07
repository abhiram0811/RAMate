// Status indicator component
'use client';

import { useEffect, useState } from 'react';
import { CheckCircle, XCircle, AlertCircle, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { apiService, SystemStatus } from '@/lib/api';

export default function StatusIndicator() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkStatus();
    // Check status every 30 seconds
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkStatus = async () => {
    try {
      setIsLoading(true);
      const statusData = await apiService.getSystemStatus();
      setStatus(statusData);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to check status');
      setStatus(null);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading && !status) {
    return (
      <div className="flex items-center space-x-2 text-sm text-gray-500">
        <Loader2 className="w-4 h-4 animate-spin" />
        <span>Checking system status...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center space-x-2 text-sm text-red-600">
        <XCircle className="w-4 h-4" />
        <span>API Offline</span>
      </div>
    );
  }

  if (!status?.data) {
    return (
      <div className="flex items-center space-x-2 text-sm text-yellow-600">
        <AlertCircle className="w-4 h-4" />
        <span>Status Unknown</span>
      </div>
    );
  }

  const { data } = status;
  const isHealthy = data.vector_store_status === 'healthy' && data.total_documents > 0;

  return (
    <div className="space-y-2">
      <div className={cn(
        "flex items-center space-x-2 text-sm",
        isHealthy ? "text-green-600" : "text-yellow-600"
      )}>
        {isHealthy ? (
          <CheckCircle className="w-4 h-4" />
        ) : (
          <AlertCircle className="w-4 h-4" />
        )}
        <span>
          {isHealthy ? 'System Online' : 'Limited Functionality'}
        </span>
      </div>
      
      <div className="text-xs text-gray-500 space-y-1">
        <div>📚 {data.total_documents} documents loaded</div>
        <div>🔧 {data.embedding_method} embeddings</div>
        <div>🤖 AI: {data.openrouter_configured ? 'Configured' : 'Local fallback'}</div>
      </div>
    </div>
  );
}
