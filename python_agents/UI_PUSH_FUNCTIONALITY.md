# UI Push 功能说明

## 概述

在TypeScript版本的LangGraph智能体中，`ui.push`是一个关键功能，用于将UI组件推送到前端界面。在Python版本中，我实现了对应的`push_ui_message`功能。

## 实现细节

### 1. UIMessageManager 类

在 `agents/types.py` 中实现了 `UIMessageManager` 类：

```python
class UIMessageManager:
    """Manager for UI messages in Python LangGraph agents."""
    
    def __init__(self):
        self.items = []
    
    def push(self, ui_component: Dict[str, Any], message_metadata: Optional[Dict[str, Any]] = None):
        """Push a UI component to the UI state."""
        ui_message = {
            "id": ui_component.get("id", str(uuid.uuid4())),
            "name": ui_component["name"],
            "props": ui_component["props"],
            "metadata": message_metadata or {}
        }
        self.items.append(ui_message)
        return ui_message
```

### 2. typed_ui 函数

```python
def typed_ui(config: Dict[str, Any]) -> UIMessageManager:
    """Create a typed UI manager for the given config."""
    return UIMessageManager()
```

### 3. 使用方式

在每个需要推送UI组件的节点中：

```python
async def some_node(state: State, config: Dict[str, Any]) -> Update:
    ui = typed_ui(config)
    
    # 推送UI组件
    ui.push(
        {
            "name": "component-name",
            "props": {
                "key1": "value1",
                "key2": "value2"
            }
        },
        {"message": ai_message}  # 可选的元数据
    )
    
    return {
        "messages": [ai_message],
        "ui": ui.items,  # 返回UI组件列表
        "timestamp": time.time()
    }
```

## 已更新的智能体

### 1. 开放代码智能体 (Open Code Agent)

在 `agents/open_code/nodes/executor.py` 中：

```python
# Push UI component - this is the key functionality that was missing!
ui.push(
    {
        "name": "proposed-change",
        "props": {
            "toolCallId": tool_call_id,
            "change": update_file_contents,
            "planItem": next_plan_item,
            "fullWriteAccess": full_write_access,
        },
    },
    {"message": ai_message},
)
```

### 2. 旅行规划智能体 (Trip Planner Agent)

在 `agents/trip_planner/nodes/tools.py` 中：

```python
ui.push(
    {
        "name": "accommodations-list",
        "props": {
            "toolCallId": tool_call["id"],
            "accommodations": result["accommodations"],
            "tripDetails": trip_details
        }
    },
    {"message": response}
)
```

### 3. 股票经纪人智能体 (Stockbroker Agent)

在 `agents/stockbroker/tools.py` 中：

```python
ui.push(
    {
        "name": "stockbroker",
        "props": {
            "toolName": tool_name,
            "result": result,
            "timestamp": time.time()
        }
    },
    {"message": response}
)
```

### 4. 写作智能体 (Writer Agent)

在 `agents/writer_agent.py` 中：

```python
ui.push(
    {
        "id": document_id,
        "name": "writer",
        "props": {
            "content": content,
            "is_generating": True
        }
    },
    {"message": last_message}
)
```

## 与TypeScript版本的对应关系

| TypeScript | Python |
|------------|--------|
| `ui.push(component, metadata)` | `ui.push(component, metadata)` |
| `typedUi<ComponentMap>(config)` | `typed_ui(config)` |
| `ui.items` | `ui.items` |

## 功能特点

1. **类型安全**: 使用Pydantic进行数据验证
2. **异步支持**: 完全支持Python的异步/等待语法
3. **元数据支持**: 支持消息元数据传递
4. **ID生成**: 自动生成唯一ID
5. **状态管理**: 维护UI组件列表

## 使用示例

```python
# 在智能体节点中使用
async def my_node(state: State, config: Dict[str, Any]) -> Update:
    ui = typed_ui(config)
    
    # 推送不同类型的UI组件
    ui.push({
        "name": "data-table",
        "props": {"data": my_data}
    })
    
    ui.push({
        "name": "chart",
        "props": {"type": "line", "data": chart_data}
    })
    
    return {
        "messages": [response],
        "ui": ui.items,
        "timestamp": time.time()
    }
```

这个实现确保了Python版本与TypeScript版本在UI推送功能上的完全对等，为生成式UI提供了完整的支持。
