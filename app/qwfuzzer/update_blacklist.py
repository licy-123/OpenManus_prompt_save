from app.qwfuzzer.Prompt_Blacklist import prompt_blacklist

from mutator_check import PromptMutator

from app.qwfuzzer.config import qw_api_key, gj_api_key

import re


mutator = PromptMutator(qw_api_key=qw_api_key, gj_api_key=gj_api_key)
def check_prompt(prompt):
    # deepseek的安全检查不通过
    if not mutator.check_safety(prompt):
        prompt_blacklist.add(prompt)
        print(f"提示词{prompt}存在越狱风险")
    elif mutator.check_safety(prompt):
        print(f'提示词{prompt}安全')

# 匹配带有#的行或空行
pattern = re.compile(r"^#|^\s*$")
with open("data.txt", "r", encoding="utf-8") as file:
    for line in file:
        if pattern.match(line):
            continue
        check_prompt(line)
        # 随机变异
        print("变异后")
        mutate_result = mutator.mutate(line)
        check_prompt(mutate_result)

