from mutator_check import PromptMutator

from config import qw_api_key, gj_api_key

from Prompt_Blacklist import prompt_blacklist

mutator = PromptMutator(qw_api_key=qw_api_key, gj_api_key=gj_api_key)
up1, up2, down = 0, 0, 0
with open("HarmBench_data.txt", "r", encoding="utf-8") as file:
    for line in file:
        res = prompt_blacklist.check_similarity(line, threshold=0.75)
        down += 1
        # 第一重防御成功检测
        if res is True:
            up2 += 1
        else:
            ans = mutator.check_safety(line)
            # 第二重防御成功检测
            if ans is False:
                up2 += 1

print(f"第二重防御拦截率为:{up2 / down}")