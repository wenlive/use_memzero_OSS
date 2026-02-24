# Mem0 开源版集成示例

演示如何在项目中集成 **mem0 开源版本**（非平台托管版），实现具有持久记忆能力的 AI 应用。

## 技术栈

| 组件 | 实现 |
|------|------|
| LLM | DeepSeek (deepseek-chat) |
| Embedding | 智谱 AI (embedding-3, 1024 维度) |
| 向量存储 | Qdrant 本地存储 |
| 历史记录 | SQLite |

## 快速开始

### 1. 环境要求

- Python 3.10+

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`：

```env
# Embedding 配置 (智谱 AI)
ZHIPU_API_KEY=your_api_key
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4
ZHIPU_MODEL=embedding-3
ZHIPU_DIMENSION=1024

# LLM 配置 (DeepSeek)
DEEPSEEK_API_KEY=your_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_TEMPERATURE=0.7
```

## 核心配置（关键坑点）

使用 OpenAI 兼容 API 时，mem0 配置有 3 个关键点：

### 1. 使用 `openai_base_url` 而非 `base_url`

```python
# config.py
"llm": {
    "config": {
        "openai_base_url": os.getenv("DEEPSEEK_BASE_URL")  # ✅
        # "base_url": ...  # ❌ 不生效
    }
}
```

### 2. 向量维度必须显式传递

```python
"vector_store": {
    "config": {
        "embedding_model_dims": 1024  # ✅ 必须与 embedder 一致
    }
}
```

### 3. 启用持久化存储

```python
"vector_store": {
    "config": {
        "on_disk": True  # ✅ 否则重启后数据丢失
    }
}
```

完整配置见 `config.py`。

## 项目结构

```
.
├── .env.example     # 环境变量模板
├── config.py        # mem0 配置（核心）
├── chatbot.py       # 聊天机器人实现
├── main.py          # 交互式入口
└── test_demo.py     # 自动演示脚本
```

**数据存储位置**：
- 向量存储: `/tmp/qdrant`
- 历史记录: `~/.mem0/history.db`

## 验证方式

### 方式 1: 自动演示

```bash
rm -rf /tmp/qdrant ~/.mem0  # 清除旧数据
python test_demo.py
```

演示 14 轮对话，覆盖：信息收集 → 记忆检索 → 信息更新 → 持久化验证。

### 方式 2: 交互式验证

```bash
python main.py test_user
```

**测试对话流程**：

| 轮次 | 输入 | 验证目的 |
|------|------|----------|
| 1 | `我叫李明，是产品经理` | 添加记忆 |
| 2 | `我在字节跳动工作` | 添加记忆 |
| 3 | `我喜欢喝美式咖啡` | 添加记忆 |
| 4 | `我叫什么名字？` | 检索记忆 |
| 5 | `我在哪里工作？` | 检索记忆 |
| 6 | `我最近换到阿里巴巴了` | 更新记忆 |
| 7 | `/memories` | 查看所有记忆 |
| 8 | `/quit` | 退出 |

**验证持久化**（重启后）：

```bash
python main.py test_user
# 输入: 你还记得我是谁吗？
# 预期: AI 应回答你的名字和工作
```

**验证用户隔离**：

```bash
python main.py another_user
# 输入: 你知道我是谁吗？
# 预期: AI 应说不认识
```

## 常见问题

### ValueError: shapes (0,1536) and (1024,) not aligned

**原因**: 旧数据使用不同向量维度

**解决**: 清除数据
```bash
rm -rf /tmp/qdrant ~/.mem0
```

### 记忆重启后丢失

**原因**: `on_disk: False`

**解决**: 在 `config.py` 中设置 `on_disk: True`

### TypeError: 'base_url' is an invalid keyword

**原因**: mem0 使用 `openai_base_url`

**解决**: 检查 `config.py` 配置

## 交互命令

- `/memories` - 查看所有记忆
- `/clear` - 清除所有记忆
- `/quit` - 退出
