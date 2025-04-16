# Prompt_Blacklist.py
from scipy.spatial.distance import cosine
from pathlib import Path
import json
import requests
from app.qwfuzzer.config import qw_api_key, gj_api_key

class PromptBlacklist:
    """
    用于黑名单的一系列操作包括取出，加入，持久维护，词嵌入，以及计算余弦相似度等等
    """
    def __init__(self, gj_api_key):
        self.file_path = Path(__file__).with_name("prompt_blacklist.json")
        self.prompts = self._load()
        self._precompute_embeddings()
        self.gj_api_key = gj_api_key


    def call_embedding_model(self, input, model='BAAI/bge-large-zh-v1.5'):
        """
        用于将输入的input词嵌入成词向量
        """
        url = "https://api.siliconflow.cn/v1/chat/completions"

        payload = {
            "model": "BAAI/bge-large-zh-v1.5",
            "input": input,
            "encoding_format": "float"
        }
        headers = {
            "Authorization": f"Bearer {self.gj_api_key}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        return response.text

    def _precompute_embeddings(self):
        """
        预计算所有黑名单词的嵌入向量
        """
        self.embeddings = {
            prompt: self.call_embedding_model(input=prompt)
            for prompt in self.prompts
        }

    def check_similarity(self, user_prompt, threshold=0.75):
        """
        检查用户输入与黑名单的语义相似度
        返回: True 代表大于阈值，有风险 False 代表小于阈值正常
        """
        user_vec = self.call_embedding_model(user_prompt)

        max_sim = 0
        best_match = None

        for prompt, prompt_vec in self.embeddings.items():
            sim = 1 - cosine(user_vec, prompt_vec)  # 余弦相似度
            if sim > max_sim:
                max_sim = sim
                best_match = prompt
                if sim >= threshold:  # 提前终止
                    return True

        return False

    def _load(self):
        """
        从文件加载历史数据，从而和新数据结合一块重新写入到prompt_blacklist.json文件中
        """
        if self.file_path.exists():
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        return set()  # 默认空集合

    def add(self, prompt):
        """
        添加并自动保存
        """
        self.prompts.add(prompt)
        self._save()

    def _save(self):
        """
        保存到文件
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(list(self.prompts), f, indent=2)


# 单例对象
prompt_blacklist = PromptBlacklist(gj_api_key=gj_api_key)