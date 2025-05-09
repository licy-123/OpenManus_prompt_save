import asyncio
from app.agent.manus import Manus
from app.logger import logger
from app.qwfuzzer.Prompt_Blacklist import prompt_blacklist
from app.qwfuzzer.config import qw_api_key, gj_api_key
from app.qwfuzzer.mutator_check import PromptMutator


async def main():
    agent = Manus()
    mutator = PromptMutator(qw_api_key=qw_api_key, gj_api_key=gj_api_key)
    try:
        prompt = input("Enter your prompt: ")
        if not prompt.strip():
            logger.warning("Empty prompt provided.")
            return
        """第一重防御,黑名单防御"""
        res = prompt_blacklist.check_similarity(prompt, threshold=0.75)
        if res is True:
            print(f"你输入的提示词具有越狱风险，请重新输入安全的提示词")
            return
        else:
            """第二重防御,大模型防御"""
            ans = mutator.check_safety(prompt)
            if ans is False:
                print(f"你输入的提示词具有越狱风险，请重新输入安全的提示词")
                return
            elif ans is True:
                print(f"提示词检测安全")

        logger.warning("Processing your request...")
        await agent.run(prompt)
        logger.info("Request processing completed.")
    except KeyboardInterrupt:
        logger.warning("Operation interrupted.")
    finally:
        # Ensure agent resources are cleaned up before exiting
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())