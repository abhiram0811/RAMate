// Utility functions for the RAMate frontend
import { clsx, type ClassValue } from 'clsx';

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

export function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

export function formatTimestamp(timestamp: string): string {
  try {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true,
    });
  } catch {
    return '';
  }
}

export function formatConfidence(confidence: number): string {
  const percentage = Math.round(confidence * 100);
  if (percentage >= 80) return 'High';
  if (percentage >= 60) return 'Medium';
  if (percentage >= 40) return 'Low';
  return 'Very Low';
}

export function getConfidenceColor(confidence: number): string {
  const percentage = Math.round(confidence * 100);
  if (percentage >= 80) return 'text-green-600';
  if (percentage >= 60) return 'text-yellow-600';
  if (percentage >= 40) return 'text-orange-600';
  return 'text-red-600';
}

export function extractDocumentName(link: string): string {
  try {
    const parts = link.split('/');
    const filename = parts[parts.length - 1];
    return filename.replace('.pdf', '').replace(/[_-]/g, ' ');
  } catch {
    return 'Document';
  }
}

export function isValidUrl(string: string): boolean {
  try {
    new URL(string);
    return true;
  } catch {
    return false;
  }
}
