// API service for communicating with the RAMate backend
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export interface ChatMessage {
  query: string;
  session_id?: string;
}

export interface ChatResponse {
  status: 'success' | 'error';
  data?: {
    answer: string;
    sources: string[];
    links: string[];
    confidence: number;
    query: string;
    timestamp: string;
  };
  message?: string;
  timestamp: string;
}

export interface SystemStatus {
  status: 'success' | 'error';
  data?: {
    vector_store_status: string;
    total_documents: number;
    source_files: string[];
    openrouter_configured: boolean;
    embedding_method: string;
  };
  timestamp: string;
}

export interface FeedbackData {
  query: string;
  answer: string;
  rating: 'thumbs_up' | 'thumbs_down';
  comment?: string;
}

class ApiService {
  private axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000, // 30 seconds
    headers: {
      'Content-Type': 'application/json',
    },
  });

  constructor() {
    // Request interceptor
    this.axiosInstance.interceptors.request.use(
      (config) => {
        console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('❌ API Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.axiosInstance.interceptors.response.use(
      (response) => {
        console.log(`✅ API Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error) => {
        console.error('❌ API Response Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // Health check
  async healthCheck(): Promise<{ status: string; service: string; version: string }> {
    try {
      const response = await this.axiosInstance.get('/');
      return response.data;
    } catch (error) {
      throw new Error('Failed to connect to RAMate API');
    }
  }

  // Get system status
  async getSystemStatus(): Promise<SystemStatus> {
    try {
      const response = await this.axiosInstance.get('/api/status');
      return response.data;
    } catch (error) {
      throw new Error('Failed to get system status');
    }
  }

  // Send chat message
  async sendChatMessage(message: ChatMessage): Promise<ChatResponse> {
    try {
      const response = await this.axiosInstance.post('/api/chat', message);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.data) {
          return error.response.data;
        }
      }
      throw new Error('Failed to send chat message');
    }
  }

  // Send user feedback
  async sendFeedback(feedback: FeedbackData): Promise<{ status: string; message: string }> {
    try {
      const response = await this.axiosInstance.post('/api/feedback', feedback);
      return response.data;
    } catch (error) {
      throw new Error('Failed to send feedback');
    }
  }

  // Check if API is available
  async isApiAvailable(): Promise<boolean> {
    try {
      await this.healthCheck();
      return true;
    } catch {
      return false;
    }
  }
}

export const apiService = new ApiService();
