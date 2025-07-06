import React from 'react';
import { Loader2 } from 'lucide-react';
import { cn } from '@/utils/cn';

export interface LoadingProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  variant?: 'spinner' | 'dots' | 'pulse';
  text?: string;
  overlay?: boolean;
  className?: string;
}

export const Loading: React.FC<LoadingProps> = ({
  size = 'md',
  variant = 'spinner',
  text,
  overlay = false,
  className
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6', 
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  };
  
  const renderSpinner = () => (
    <Loader2 className={cn('loading-spinner', sizeClasses[size])} />
  );
  
  const renderDots = () => (
    <div className="loading-dots">
      <div className="loading-dot" />
      <div className="loading-dot" />
      <div className="loading-dot" />
    </div>
  );
  
  const renderPulse = () => (
    <div className={cn(
      'bg-secondary-300 rounded animate-pulse-soft',
      size === 'sm' ? 'w-8 h-8' : 
      size === 'md' ? 'w-12 h-12' :
      size === 'lg' ? 'w-16 h-16' : 'w-20 h-20'
    )} />
  );
  
  const renderContent = () => {
    let loadingElement;
    
    switch (variant) {
      case 'dots':
        loadingElement = renderDots();
        break;
      case 'pulse':
        loadingElement = renderPulse();
        break;
      default:
        loadingElement = renderSpinner();
    }
    
    return (
      <div className={cn(
        'flex flex-col items-center justify-center space-y-2',
        !overlay && 'p-4',
        className
      )}>
        {loadingElement}
        {text && (
          <span className="text-sm text-secondary-600 animate-pulse">
            {text}
          </span>
        )}
      </div>
    );
  };
  
  if (overlay) {
    return (
      <div className="loading-overlay">
        {renderContent()}
      </div>
    );
  }
  
  return renderContent();
};

Loading.displayName = 'Loading';