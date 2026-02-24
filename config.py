from mem0 import Memory
import os
from dotenv import load_dotenv

load_dotenv()

def get_mem0_config():
    """获取 mem0 配置（使用默认 Qdrant 向量存储）"""
    embedding_dims = int(os.getenv("ZHIPU_DIMENSION", "1024"))
    return {
        "llm": {
            "provider": "openai",
            "config": {
                "api_key": os.getenv("DEEPSEEK_API_KEY"),
                "model": os.getenv("DEEPSEEK_MODEL"),
                "temperature": float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7")),
                "openai_base_url": os.getenv("DEEPSEEK_BASE_URL")
            }
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "api_key": os.getenv("ZHIPU_API_KEY"),
                "model": os.getenv("ZHIPU_MODEL"),
                "embedding_dims": embedding_dims,
                "openai_base_url": os.getenv("ZHIPU_BASE_URL")
            }
        },
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "embedding_model_dims": embedding_dims,
                "path": "/tmp/qdrant",
                "on_disk": True
            }
        }
        # history_db 使用默认的 SQLite (~/.mem0/history.db)
    }
