import { clsx, type ClassValue } from 'clsx';

/**
 * 条件类名合并工具函数
 * 基于clsx实现，用于组合Tailwind CSS类名
 * 
 * @param inputs - 类名参数，可以是字符串、对象、数组等
 * @returns 合并后的类名字符串
 * 
 * @example
 * cn('bg-blue-500', 'text-white') // 'bg-blue-500 text-white'
 * cn('bg-blue-500', { 'text-white': true, 'font-bold': false }) // 'bg-blue-500 text-white'
 * cn(['bg-blue-500', 'text-white']) // 'bg-blue-500 text-white'
 */
export function cn(...inputs: ClassValue[]): string {
  return clsx(inputs);
}