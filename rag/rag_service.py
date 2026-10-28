"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from rag.vector_store import VectorStoreService
from model.factory import chat_model
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate


def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        # 从数据库里检索与用户提问相关的内容，取 k个值
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str) -> list[Document]:
        # 执行 从数据库里检索与用户提问相关的内容，取 k个值
        return self.retriever.invoke(query)

    def rag_summarize(self, querry: str) -> str:
        context_docs = self.retriever_docs(querry)

        context=""
        count = 0
        for doc in context_docs:
            count += 1
            context += f"[参考资料:{count}]: 参考资料：{doc.page_content} | 参考元数据：{doc.metadata}"

        return self.chain.invoke(
            {
                "input": querry,
                "context": context
            }
        )

if __name__ == '__main__':
    rag_service = RagSummarizeService()
    print(rag_service.rag_summarize("小户型适合那种扫地机器人"))