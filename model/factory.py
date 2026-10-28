from abc import ABC, abstractmethod
from typing import Optional
from utils.config_handler import rag_config
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
import os
from langchain_community.embeddings import DashScopeEmbeddings

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

class BaseModelFactory(ABC):

    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=rag_config["chat_model_name"],
            api_key=DASHSCOPE_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_config["embedding_model_name"])

chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()

