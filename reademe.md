# AI-XiaoZhi 项目架构升级与开发规划

本文档旨在记录并指导 AI-XiaoZhi 项目下一阶段的重大架构升级。核心目标是建立一个稳定、可扩展、高内聚、低耦合的前后端通信体系，为未来的功能迭代和技术迁移奠定坚实基础。

## 1. 现状分析与挑战

### 1.1. 后端 (xiaozhi-esp32-server)
- **结构**: 基于 Python (Flask/FastAPI)，包含 `core` 业务逻辑、`plugins_func` 插件功能等模块，结构清晰。
- **挑战**: 目前主要通过 HTTP API 与外部通信，缺少实时推送能力，导致客户端需要通过轮询获取最新状态，效率低下且不及时。

### 1.2. 小程序端 (miniprogram-v1)
- **结构**: 标准的微信小程序结构，`pages` 存放页面，`utils` 存放公共方法，`app.js` 处理全局逻辑。
- **挑战**:
    - **数据获取分散**: 各个页面独立调用 API 获取数据，导致数据状态不一致、管理混乱。
    - **高度耦合**: 页面逻辑与具体的 API 请求 (`wx.request`) 强耦合，如果后端接口变更或技术栈更换，需要修改大量页面代码。
    - **缺乏实时性**: 无法实时感知设备上下线、状态变化等事件。

## 2. 顶层设计：面向未来的模块化架构

为了解决上述挑战，并为未来可能的"后端更换为Java"或"UI大改"做好准备，我们设计了以下分层解耦架构。

### 2.1. 核心思想：建立"通信服务层" (The Bridge)

我们将在小程序内部建立一个独立的 **通信服务层 (`services`)**。该层是小程序UI与后端之间唯一的沟通桥梁。

```mermaid
graph TD
    subgraph 微信小程序
        direction LR
        subgraph UI层 (Pages)
            P1(页面A)
            P2(页面B)
            P3(页面C)
        end
        subgraph 通信服务层 (Services)
            DS(deviceService.js <br> 状态管理器)
            WS(websocketService.js <br> 实时通信)
            AS(apiService.js <br> HTTP请求)
        end
        UI层 -->|只与Service交互| 通信服务层
    end

    subgraph 后端服务器
        B_API(HTTP API)
        B_WS(WebSocket)
    end

    通信服务层 -->|发起请求/建连接| 后端服务器

    B_WS --o|主动推送| WS
```

### 2.2. 各层职责

*   **UI层 (Pages)**:
    *   **职责**: 只负责界面的展示和用户交互。
    *   **规则**: **绝不**直接调用 `wx.request` 或处理任何 WebSocket 细节。所有的数据请求和状态订阅都必须通过 `deviceService.js`。
    *   **例子**: `deviceService.getDeviceList().then(...)`, `deviceService.onDeviceStatusChange(callback)`。

*   **通信服务层 (Services)**:
    *   `apiService.js`: 封装所有 `wx.request` 请求。提供清晰的、业务化的方法，如 `fetchDeviceList()`、`updateDeviceName(id, name)`。处理公共的 loading、错误处理、header 设置等。
    *   `websocketService.js`: 封装 WebSocket 的所有细节，包括连接、断线重连、心跳维持、接收并解析服务端推送的消息。它像一个电话总机，只负责接收和分发原始消息。
    *   `deviceService.js`: **核心状态管理器**。
        1.  对UI层提供统一接口，屏蔽了底层是 HTTP 还是 WebSocket。
        2.  通过 `apiService.js` 拉取初始数据。
        3.  监听来自 `websocketService.js` 的实时消息（如"设备A上线"），更新自身维护的全局设备列表。
        4.  当数据变化时，通过回调机制通知所有正在监听的UI页面进行刷新。

## 3. 详细开发规划

我们将分阶段进行开发，确保每一步都稳妥可靠。

### Phase 1: 后端 WebSocket 能力建设

**目标**: 让 Python 后端具备 WebSocket 实时推送能力。

1.  **技术选型**: 为 `app.py` 集成 `Flask-SocketIO` 或 `FastAPI-WebSocket` 库。
2.  **实现连接点**: 创建 `/ws` 或 `/socket.io` 端点，用于处理来自小程序的 WebSocket 连接请求。
3.  **集成业务逻辑**:
    *   修改设备上线/离线逻辑（很可能与MQTT消息处理相关）：当服务器检测到设备状态变化时，不再仅仅是更新数据库，而是要立刻通过 WebSocket 向所有连接的小程序客户端广播一条消息。
    *   **消息格式**: 定义标准化的JSON消息格式，例如：`{ "event": "device_online", "data": { "deviceId": "xxx", "deviceName": "客厅的小智" } }` 或 `{ "event": "device_offline", "data": { "deviceId": "xxx" } }`。

### Phase 2: 小程序"通信服务层"搭建

**目标**: 在小程序中构建出解耦的 `services` 层。

1.  **创建目录**: 在小程序根目录下创建 `services` 文件夹。
2.  **编写 `apiService.js`**:
    *   将 `utils/api.js` 中现有的 API 请求逻辑迁移和封装到 `services/apiService.js` 中。
    *   导出业务化函数，如 `export const getDevices = () => request('/devices', 'GET');`。
3.  **编写 `websocketService.js`**:
    *   实现连接、断开、重连、心跳等功能。
    *   提供 `onMessage(callback)` 方法，让其他模块可以监听收到的所有原始消息。
4.  **编写 `deviceService.js`**:
    *   在内部引入 `apiService` 和 `websocketService`。
    *   维护一个全局的设备列表变量 `globalDeviceList`。
    *   提供 `getDeviceList()` 方法：如果 `globalDeviceList` 为空，则调用 `apiService` 获取，否则直接返回。
    *   调用 `websocketService.onMessage()` 监听消息，根据消息的 `event` 类型来更新 `globalDeviceList`。
    *   实现一个简单的发布-订阅模式，提供 `subscribe(callback)` 和 `unsubscribe(callback)` 方法，当列表更新时，调用所有订阅的回调函数。
5.  **全局实例化**: 在 `app.js` 的 `onLaunch` 中，初始化并挂载 `deviceService`到`getApp().globalData`上，使其成为全局单例。

### Phase 3: UI 页面重构

**目标**: 将所有页面对数据的依赖切换到新建的 `deviceService`。

1.  **修改 `pages/index/index.js`**, **`pages/devices/devices.js`** 等所有相关页面。
2.  **移除**所有 `wx.request` 代码。
3.  在 `onLoad` 或 `onShow` 中：
    *   通过 `getApp().globalData.deviceService.getDeviceList()` 获取初始列表并渲染。
    *   通过 `getApp().globalData.deviceService.subscribe(this.onDeviceUpdate)` 注册一个回调函数 `this.onDeviceUpdate`。
4.  在页面的 `onUnload` 中，调用 `unsubscribe` 方法取消订阅，避免内存泄漏。
5.  编写 `onDeviceUpdate(newList)` 回调函数，在其中 `this.setData({ deviceList: newList })` 来刷新界面。

## 4. 关键收益

*   **高度解耦**: UI层与数据层完全分离。未来更换后端或UI，工作量都将大大减少。
*   **状态统一**: 所有数据由 `deviceService` 统一管理，彻底解决数据不一致问题。
*   **代码清晰**: 职责划分明确，新功能开发和后期维护都变得更加简单。
*   **实时体验**: 用户可以实时看到设备状态变化，体验大幅提升。

---

我们已经有了清晰的蓝图。接下来，我建议我们严格按照这个规划，从 **Phase 1: 后端 WebSocket 能力建设** 开始着手。您同意吗？
