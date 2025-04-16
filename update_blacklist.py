from Prompt_Blacklist import prompt_blacklist
from mutator_check import PromptMutator
from .config import qw_api_key, gj_api_key


mutator = PromptMutator(qw_api_key=qw_api_key, gj_api_key=gj_api_key)
def check_prompt(prompt):
    # deepseek的安全检查不通过
    if not mutator.check_safety(prompt):
        prompt_blacklist.add(prompt)
        print(f"提示词{prompt}存在越狱风险")
    elif mutator.check_safety(prompt):
        print(f'提示词{prompt}安全')
