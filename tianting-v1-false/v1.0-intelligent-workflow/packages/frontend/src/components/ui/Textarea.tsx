import React, { useState } from 'react';
import { cn } from '@/utils/cn';

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helper?: string;
  maxLength?: number;
  showCount?: boolean;
  variant?: 'default' | 'success' | 'warning' | 'error';
  resize?: 'none' | 'vertical' | 'horizontal' | 'both';
}

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({
    label,
    error,
    helper,
    maxLength,
    showCount = false,
    variant = 'default',
    resize = 'vertical',
    className,
    id,
    value,
    defaultValue,
    onChange,
    ...props
  }, ref) => {
    const [charCount, setCharCount] = useState(() => {
      const initialValue = value || defaultValue || '';
      return initialValue.toString().length;
    });
    
    const textareaId = id || `textarea-${Math.random().toString(36).substr(2, 9)}`;
    
    const variantClasses = {
      default: '',
      success: 'input-success',
      warning: 'input-warning',
      error: 'input-error'
    };
    
    const resizeClasses = {
      none: 'textarea-resize-none',
      vertical: 'textarea-resize-vertical',
      horizontal: 'textarea-resize-horizontal',
      both: 'textarea-resize-both'
    };
    
    const actualVariant = error ? 'error' : variant;
    
    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
      const newValue = event.target.value;
      setCharCount(newValue.length);
      onChange?.(event);
    };
    
    const isOverLimit = maxLength && charCount > maxLength;
    
    return (
      <div className="form-group">
        {label && (
          <label htmlFor={textareaId} className="form-label">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          id={textareaId}
          className={cn(
            'input-base',
            variantClasses[actualVariant],
            resizeClasses[resize],
            'min-h-[80px]',
            'input-responsive',
            className
          )}
          maxLength={maxLength}
          value={value}
          defaultValue={defaultValue}
          onChange={handleChange}
          {...props}
        />
        {(showCount || error || helper) && (
          <div className="flex justify-between items-start text-sm mt-1">
            <span className={error ? 'form-error' : 'form-helper'}>
              {error || helper}
            </span>
            {showCount && maxLength && (
              <span className={cn(
                'text-sm font-medium',
                isOverLimit ? 'text-error-600' : 'text-secondary-500'
              )}>
                {charCount}/{maxLength}
              </span>
            )}
          </div>
        )}
      </div>
    );
  }
);

Textarea.displayName = 'Textarea';