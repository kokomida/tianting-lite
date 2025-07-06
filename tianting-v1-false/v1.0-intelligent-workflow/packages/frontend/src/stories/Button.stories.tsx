import type { Meta, StoryObj } from '@storybook/react';
// import { action } from '@storybook/addon-actions';
import { Play, Plus, Download } from 'lucide-react';
import { Button } from '@/components/ui/Button';

const meta = {
  title: 'UI/Button',
  component: Button,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: '天庭系统的按钮组件，支持多种变体、尺寸和状态。',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost', 'success', 'warning', 'error'],
      description: '按钮的视觉变体',
    },
    size: {
      control: 'select', 
      options: ['sm', 'md', 'lg'],
      description: '按钮的尺寸',
    },
    loading: {
      control: 'boolean',
      description: '是否显示加载状态',
    },
    disabled: {
      control: 'boolean',
      description: '是否禁用按钮',
    },
  },
  args: { 
    onClick: () => console.log('clicked'),
    children: '按钮',
  },
} satisfies Meta<typeof Button>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: '主要按钮',
  },
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: '次要按钮',
  },
};

export const Outline: Story = {
  args: {
    variant: 'outline',
    children: '边框按钮',
  },
};

export const Ghost: Story = {
  args: {
    variant: 'ghost',
    children: '幽灵按钮',
  },
};

export const Success: Story = {
  args: {
    variant: 'success',
    children: '成功按钮',
  },
};

export const Warning: Story = {
  args: {
    variant: 'warning',
    children: '警告按钮',
  },
};

export const Error: Story = {
  args: {
    variant: 'error',
    children: '错误按钮',
  },
};

export const Small: Story = {
  args: {
    size: 'sm',
    children: '小按钮',
  },
};

export const Medium: Story = {
  args: {
    size: 'md',
    children: '中等按钮',
  },
};

export const Large: Story = {
  args: {
    size: 'lg',
    children: '大按钮',
  },
};

export const Loading: Story = {
  args: {
    loading: true,
    children: '加载中...',
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
    children: '禁用按钮',
  },
};

export const WithLeftIcon: Story = {
  args: {
    leftIcon: <Plus />,
    children: '添加项目',
  },
};

export const WithRightIcon: Story = {
  args: {
    rightIcon: <Download />,
    children: '下载文件',
  },
};

export const IconOnly: Story = {
  args: {
    leftIcon: <Play />,
    'aria-label': '播放',
  },
};

export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-wrap gap-4">
      <Button variant="primary">主要</Button>
      <Button variant="secondary">次要</Button>
      <Button variant="outline">边框</Button>
      <Button variant="ghost">幽灵</Button>
      <Button variant="success">成功</Button>
      <Button variant="warning">警告</Button>
      <Button variant="error">错误</Button>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: '展示所有按钮变体的组合。',
      },
    },
  },
};

export const AllSizes: Story = {
  render: () => (
    <div className="flex items-center gap-4">
      <Button size="sm">小</Button>
      <Button size="md">中</Button>
      <Button size="lg">大</Button>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: '展示所有按钮尺寸的组合。',
      },
    },
  },
};