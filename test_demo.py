"""
自动化演示脚本，展示 mem0 的记忆能力
"""
from chatbot import Mem0ChatBot
import time

def run_demo():
    print("\n" + "="*60)
    print("Mem0 记忆能力演示")
    print("="*60 + "\n")

    bot = Mem0ChatBot(user_id="demo_user")

    # 演示对话
    demo_conversations = [
        "我叫张三，是一名软件工程师",
        "我喜欢吃意大利菜和日本料理",
        "我正在学习 Rust 编程语言",
        "我住在北京",
        "我的爱好是 hiking 和摄影",
        # 测试记忆
        "我叫什么名字？",
        "我喜欢吃什么食物？",
        "我正在学习什么编程语言？",
        "我住在哪里？",
        "我的爱好是什么？",
        # 新信息
        "实际上，我最近搬到了上海",
        "我又多了一个爱好：弹吉他",
        # 再次测试记忆更新
        "我现在住在哪里？",
        "我有哪些爱好？"
    ]

    print("开始演示对话...\n")

    for i, user_input in enumerate(demo_conversations, 1):
        print(f"\n--- 对话 {i} ---")
        print(f"用户: {user_input}")

        response = bot.chat(user_input)
        print(f"AI: {response}")

        time.sleep(1)

    # 显示所有记忆
    print("\n" + "="*60)
    print("演示结束！以下是 AI 记住的所有信息：")
    print("="*60)
    bot.show_all_memories()

if __name__ == "__main__":
    run_demo()
