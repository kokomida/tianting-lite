import React from 'react';
import { cn } from '@/utils/cn';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helper?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'error';
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({
    label,
    error,
    helper,
    leftIcon,
    rightIcon,
    variant = 'default',
    className,
    id,
    ...props
  }, ref) => {
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
    
    const variantClasses = {
      default: '',
      success: 'input-success',
      warning: 'input-warning', 
      error: 'input-error'
    };
    
    const actualVariant = error ? 'error' : variant;
    
    return (
      <div className="form-group">
        {label && (
          <label htmlFor={inputId} className="form-label">
            {label}
          </label>
        )}
        <div className="relative">
          {leftIcon && (
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <span className="text-secondary-400 w-4 h-4">
                {leftIcon}
              </span>
            </div>
          )}
          <input
            ref={ref}
            id={inputId}
            className={cn(
              'input-base',
              variantClasses[actualVariant],
              leftIcon && 'pl-10',
              rightIcon && 'pr-10',
              'input-responsive',
              className
            )}
            {...props}
          />
          {rightIcon && (
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <span className="text-secondary-400 w-4 h-4">
                {rightIcon}
              </span>
            </div>
          )}
        </div>
        {(error || helper) && (
          <div className="flex justify-between items-start text-sm mt-1">
            <span className={error ? 'form-error' : 'form-helper'}>
              {error || helper}
            </span>
          </div>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';