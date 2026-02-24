import logging
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory
from config import get_mem0_config
import os

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Mem0ChatBot:
    def __init__(self, user_id: str = "default_user"):
        """初始化聊天机器人"""
        self.user_id = user_id
        self.memory = Memory.from_config(get_mem0_config())
        self.llm_client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL")
        )
        logger.info(f"聊天机器人初始化完成 (user_id: {user_id})")

    def search_memories(self, query: str, limit: int = 5) -> List[Dict]:
        """搜索相关记忆"""
        logger.info(f"🔍 搜索记忆: query='{query}'")
        results = self.memory.search(query=query, user_id=self.user_id, limit=limit)
        memories = results.get("results", [])
        logger.info(f"✓ 找到 {len(memories)} 条相关记忆")
        for i, mem in enumerate(memories, 1):
            logger.info(f"  记忆 {i}: {mem['memory'][:80]}...")
        return memories

    def build_context(self, memories: List[Dict]) -> str:
        """构建记忆上下文"""
        if not memories:
            return "（暂无相关记忆）"
        context_lines = [f"- {m['memory']}" for m in memories]
        return "\n".join(context_lines)

    def chat(self, user_input: str) -> str:
        """主聊天函数"""
        logger.info(f"\n{'='*60}")
        logger.info(f"👤 用户输入: {user_input}")

        # 1. 检索相关记忆
        memories = self.search_memories(user_input)
        memory_context = self.build_context(memories)

        # 2. 构建提示词
        system_prompt = f"""你是一个有帮助的 AI 助手，具有记忆能力。

用户的相关记忆：
{memory_context}

请根据这些记忆和用户的输入，给出个性化的回复。如果用户提供了新信息，
请自然地记住它们。"""

        # 3. 调用 LLM
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        logger.info("🤖 调用 LLM 生成回复...")
        response = self.llm_client.chat.completions.create(
            model=os.getenv("DEEPSEEK_MODEL"),
            messages=messages,
            temperature=float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7"))
        )
        assistant_reply = response.choices[0].message.content
        logger.info(f"✓ AI 回复: {assistant_reply}")

        # 4. 保存对话到记忆
        messages.append({"role": "assistant", "content": assistant_reply})
        logger.info("💾 保存对话到记忆系统...")
        memory_result = self.memory.add(messages, user_id=self.user_id)
        logger.info(f"✓ 记忆已保存 (可能提取了 {len(memory_result)} 条新记忆)")

        return assistant_reply

    def show_all_memories(self):
        """显示所有记忆"""
        logger.info(f"\n{'='*60}")
        logger.info(f"📚 用户 {self.user_id} 的所有记忆：")
        all_memories = self.memory.get_all(user_id=self.user_id)
        memories = all_memories.get("results", [])
        if not memories:
            logger.info("  （暂无记忆）")
        else:
            for i, mem in enumerate(memories, 1):
                logger.info(f"  {i}. {mem['memory']}")
        return memories

    def clear_memories(self):
        """清除所有记忆"""
        logger.info(f"🗑️  清除用户 {self.user_id} 的所有记忆...")
        all_memories = self.memory.get_all(user_id=self.user_id)
        for mem in all_memories.get("results", []):
            self.memory.delete(memory_id=mem['id'], user_id=self.user_id)
        logger.info("✓ 记忆已清空")
