import sys
from chatbot import Mem0ChatBot
import logging

logger = logging.getLogger(__name__)

def print_banner():
    print("\n" + "="*60)
    print("  Mem0 开源版聊天演示")
    print("  具有持久记忆能力的 AI 助手")
    print("="*60)
    print("\n命令:")
    print("  /memories   - 查看所有记忆")
    print("  /clear      - 清除所有记忆")
    print("  /quit 或 /exit - 退出")
    print("\n开始聊天吧！\n")

def main():
    print_banner()

    # 获取用户 ID（可选）
    user_id = "default_user"
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
        print(f"使用用户 ID: {user_id}\n")

    # 初始化聊天机器人
    bot = Mem0ChatBot(user_id=user_id)

    # 主循环
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # 处理命令
            if user_input.lower() in ['/quit', '/exit']:
                print("\n再见！👋")
                break
            elif user_input.lower() == '/memories':
                bot.show_all_memories()
                continue
            elif user_input.lower() == '/clear':
                confirm = input("确认清除所有记忆？(yes/no): ").strip().lower()
                if confirm == 'yes':
                    bot.clear_memories()
                continue

            # 聊天
            response = bot.chat(user_input)
            print(f"\nAI: {response}\n")

        except KeyboardInterrupt:
            print("\n\n再见！👋")
            break
        except Exception as e:
            logger.error(f"错误: {e}", exc_info=True)
            print(f"\n❌ 发生错误: {e}\n")

if __name__ == "__main__":
    main()
