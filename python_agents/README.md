# Python LangGraph Agents

这是TypeScript版本的LangGraph智能体项目的Python实现。该项目包含了一系列使用LangGraph构建的智能体，可以与Agent Chat UI配合使用。

![Generative UI Example](../static/gen_ui.gif)

## 功能特性

- **监督者智能体**: 路由对话到专门的智能体
- **股票经纪人智能体**: 处理股票交易和投资组合管理
- **旅行规划智能体**: 帮助规划旅行和预订
- **开放代码智能体**: 生成React TODO应用代码
- **披萨订购智能体**: 演示工具调用和结果渲染
- **写作智能体**: 生成文本文档
- **邮件智能体**: 带有人机交互功能的邮件助手
- **聊天智能体**: 简单的对话智能体

## 安装

### 使用Docker Compose（推荐）

1. 克隆仓库并进入Python智能体目录：
```bash
cd python_agents
```

2. 复制环境配置文件：
```bash
cp env.example .env
```

3. 编辑`.env`文件，设置必要的API密钥：
```bash
# 必需的API密钥
OPENAI_API_KEY="your_openai_api_key_here"
GOOGLE_API_KEY="your_google_api_key_here"

# 可选的API密钥
ANTHROPIC_API_KEY="your_anthropic_api_key_here"
FINANCIAL_DATASETS_API_KEY="your_financial_datasets_api_key_here"
```

4. 启动服务：
```bash
docker compose up
```

### 本地安装

1. 确保Python 3.11+已安装

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 设置环境变量（同上）

4. 运行应用：
```bash
python main.py
```

## 使用方法

### 可用的智能体

- **agent**: 主监督者智能体（默认）
- **chat**: 简单聊天智能体
- **email_agent**: 邮件助手智能体
- **stockbroker**: 股票经纪人智能体
- **trip_planner**: 旅行规划智能体
- **open_code**: 代码生成智能体
- **pizza_orderer**: 披萨订购智能体
- **writer_agent**: 写作智能体

### 示例提示

#### 主智能体（agent）
- `What can you do?` - 列出所有可用工具/操作
- `Show me places to stay in <地点>` - 触发旅行智能体显示住宿选择
- `Recommend some restaurants for me in <地点>` - 触发旅行智能体显示餐厅推荐
- `What's the current price of <股票代码>` - 触发股票经纪人智能体显示股价
- `I want to buy <数量> shares of <股票代码>` - 触发股票经纪人智能体购买股票
- `Show me my portfolio` - 触发股票经纪人智能体显示投资组合
- `Write a React TODO app for me` - 触发开放代码智能体
- `Order me a pizza <配料说明> in <地点>` - 触发披萨订购智能体
- `Write me a short story about <主题>` - 触发写作智能体

#### 聊天智能体（chat）
- 任何一般性对话问题

#### 邮件智能体（email_agent）
- `Write me an email to <邮箱> about <邮件描述>` - 生成邮件并等待人工确认

## 项目结构

```
python_agents/
├── agents/                    # 智能体模块
│   ├── __init__.py
│   ├── types.py              # 通用类型定义
│   ├── chat_agent.py         # 聊天智能体
│   ├── stockbroker/          # 股票经纪人智能体
│   │   ├── __init__.py
│   │   ├── types.py
│   │   └── tools.py
│   ├── trip_planner/         # 旅行规划智能体
│   │   ├── __init__.py
│   │   ├── types.py
│   │   └── nodes/
│   │       ├── classify.py
│   │       ├── extraction.py
│   │       └── tools.py
│   ├── supervisor/           # 监督者智能体
│   │   ├── __init__.py
│   │   ├── types.py
│   │   └── nodes/
│   │       ├── router.py
│   │       └── general_input.py
│   ├── email_agent/          # 邮件智能体
│   │   ├── __init__.py
│   │   ├── types.py
│   │   └── nodes/
│   │       ├── write_email.py
│   │       ├── interrupt.py
│   │       ├── send_email.py
│   │       └── rewrite_email.py
│   ├── open_code/            # 开放代码智能体
│   │   ├── __init__.py
│   │   ├── types.py
│   │   └── nodes/
│   │       ├── planner.py
│   │       └── executor.py
│   ├── pizza_orderer.py      # 披萨订购智能体
│   └── writer_agent.py       # 写作智能体
├── main.py                   # 主入口文件
├── requirements.txt          # Python依赖
├── Dockerfile               # Docker配置
├── docker-compose.yml       # Docker Compose配置
├── env.example              # 环境变量示例
└── README.md                # 本文档
```

## 开发

### 添加新的智能体

1. 在`agents/`目录下创建新的智能体模块
2. 实现必要的节点和工具
3. 在`main.py`中注册新智能体
4. 更新文档

### 测试

```bash
python -m pytest tests/
```

### 代码格式化

```bash
black .
isort .
```

## 与TypeScript版本的差异

- 使用Python的异步/等待语法
- 使用Pydantic进行数据验证
- 使用LangChain的Python SDK
- 简化了UI组件渲染（专注于核心功能）
- 保持了相同的智能体逻辑和流程

## 故障排除

### 常见问题

1. **API密钥错误**: 确保所有必需的API密钥都已正确设置
2. **依赖安装失败**: 确保Python版本为3.11+
3. **Docker构建失败**: 检查Dockerfile和网络连接

### 日志

查看详细日志：
```bash
docker compose logs -f python-agents
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

与原始TypeScript项目相同的许可证。
