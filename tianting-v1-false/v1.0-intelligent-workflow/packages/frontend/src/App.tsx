import React from 'react';
import { Sparkles, Play, Download, Users } from 'lucide-react';
import { 
  Button, 
  Input, 
  Textarea, 
  Card, 
  CardHeader, 
  CardContent, 
  CardFooter,
  Badge,
  Loading 
} from './components/ui';

function App() {
  const [loading, setLoading] = React.useState(false);
  const [inputValue, setInputValue] = React.useState('');
  const [textareaValue, setTextareaValue] = React.useState('');

  const handleSubmit = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 2000);
  };

  return (
    <div className="min-h-screen bg-secondary-50 container-padding section-spacing">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* 标题区域 */}
        <div className="text-center space-y-4">
          <h1 className="text-heading-1 flex items-center justify-center gap-2">
            <Sparkles className="w-8 h-8 text-primary-600" />
            天庭系统 UI 组件库
          </h1>
          <p className="text-body-large">
            为"言出法随"体验而设计的现代化组件库
          </p>
          <div className="flex justify-center gap-2">
            <Badge variant="primary">React 18</Badge>
            <Badge variant="success">TypeScript</Badge>
            <Badge variant="secondary">Tailwind CSS</Badge>
          </div>
        </div>

        {/* 按钮展示区域 */}
        <Card variant="elevated">
          <CardHeader>
            <h2 className="text-heading-2">按钮组件</h2>
            <p className="text-body">支持多种变体、尺寸和状态的按钮组件</p>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <h3 className="text-heading-3">变体展示</h3>
                <div className="flex flex-wrap gap-3">
                  <Button variant="primary">主要按钮</Button>
                  <Button variant="secondary">次要按钮</Button>
                  <Button variant="outline">边框按钮</Button>
                  <Button variant="ghost">幽灵按钮</Button>
                  <Button variant="success">成功按钮</Button>
                  <Button variant="warning">警告按钮</Button>
                  <Button variant="error">错误按钮</Button>
                </div>
              </div>
              
              <div className="space-y-2">
                <h3 className="text-heading-3">尺寸展示</h3>
                <div className="flex items-center gap-3">
                  <Button size="sm">小按钮</Button>
                  <Button size="md">中等按钮</Button>
                  <Button size="lg">大按钮</Button>
                </div>
              </div>
              
              <div className="space-y-2">
                <h3 className="text-heading-3">图标按钮</h3>
                <div className="flex gap-3">
                  <Button leftIcon={<Play />}>播放</Button>
                  <Button rightIcon={<Download />}>下载</Button>
                  <Button leftIcon={<Users />} variant="outline">团队</Button>
                </div>
              </div>
              
              <div className="space-y-2">
                <h3 className="text-heading-3">状态展示</h3>
                <div className="flex gap-3">
                  <Button loading={loading} onClick={handleSubmit}>
                    {loading ? '处理中...' : '提交请求'}
                  </Button>
                  <Button disabled>禁用按钮</Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* 表单组件区域 */}
        <Card variant="elevated">
          <CardHeader>
            <h2 className="text-heading-2">表单组件</h2>
            <p className="text-body">输入框和文本域组件，支持标签、错误状态和帮助文本</p>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <Input
                label="项目名称"
                placeholder="请输入项目名称"
                helper="项目名称将显示在仪表板中"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
              />
              
              <Input
                label="邮箱地址"
                type="email"
                placeholder="your@email.com"
                leftIcon={<Users />}
                variant="success"
                helper="我们将使用此邮箱发送项目更新"
              />
              
              <Input
                label="错误示例"
                placeholder="输入内容"
                error="此字段为必填项"
              />
              
              <Textarea
                label="项目描述"
                placeholder="请详细描述您的项目需求..."
                helper="详细的描述有助于AI更好地理解您的需求"
                maxLength={500}
                showCount
                value={textareaValue}
                onChange={(e) => setTextareaValue(e.target.value)}
                rows={4}
              />
            </div>
          </CardContent>
        </Card>

        {/* 其他组件区域 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card variant="interactive">
            <CardHeader>
              <h3 className="text-heading-3">加载组件</h3>
            </CardHeader>
            <CardContent className="space-y-4">
              <Loading variant="spinner" text="正在生成项目规划..." />
              <Loading variant="dots" size="lg" />
              <Loading variant="pulse" size="md" />
            </CardContent>
          </Card>
          
          <Card variant="interactive">
            <CardHeader>
              <h3 className="text-heading-3">标签组件</h3>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                <Badge variant="primary">React</Badge>
                <Badge variant="secondary">TypeScript</Badge>
                <Badge variant="success">已完成</Badge>
                <Badge variant="warning">进行中</Badge>
                <Badge variant="error">已取消</Badge>
                <Badge variant="outline">自定义</Badge>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* 功能演示区域 */}
        <Card variant="elevated">
          <CardHeader>
            <h2 className="text-heading-2">组件集成演示</h2>
            <p className="text-body">展示组件如何协同工作以创建完整的用户界面</p>
          </CardHeader>
          <CardContent>
            <div className="bg-secondary-50 p-6 rounded-lg">
              <h4 className="text-heading-3 mb-4">AI项目需求输入表单</h4>
              <div className="space-y-4">
                <Input
                  label="项目类型"
                  placeholder="例如：智能音乐推荐APP"
                  leftIcon={<Sparkles />}
                />
                <Textarea
                  label="详细需求描述"
                  placeholder="请描述您想要开发的项目功能、目标用户、技术要求等..."
                  maxLength={1000}
                  showCount
                  rows={6}
                />
                <div className="flex justify-between items-center">
                  <div className="flex gap-2">
                    <Badge variant="outline">Web应用</Badge>
                    <Badge variant="outline">移动端</Badge>
                    <Badge variant="outline">API服务</Badge>
                  </div>
                  <Button variant="primary" size="lg" leftIcon={<Sparkles />}>
                    生成项目规划
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <p className="text-body-small text-secondary-500">
              这个表单展示了如何将多个UI组件组合成一个完整的功能模块
            </p>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}

export default App;