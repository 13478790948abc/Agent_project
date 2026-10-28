from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.logger_handler import logger
from utils.config_handler import chroma_config
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.path_tool import get_abs_path

class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_config["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_config["persist_directory"],
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separators"],
            length_function=len
        )

    def get_retriever(self):
        # 把用户的自然语言问题，变成一批从知识库里召回的参考文档（Document 列表）
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_config["k"]})

    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算文件的 MD5做去重
        :return: None
        """
        def check_md5_hex(md5_for_check: str):
            MD5_path = get_abs_path(chroma_config["md5_hex_store"])

            if not os.path.exists(MD5_path):
                open(MD5_path, "w", encoding="utf-8").close()
                return False        # md5 没处理过
            else:
                for line in open(MD5_path, "r", encoding="utf-8").readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True

            return False

        def save_md5(md5_for_check: str):
            MD5_path = get_abs_path(chroma_config["md5_hex_store"])
            with open(MD5_path, "a", encoding="utf-8") as f:
               f.write(md5_for_check +"\n")

        def get_file_documents(read_path: str):
            #获取文件里面的内容

            if read_path.endswith(".txt"):
                return txt_loader(read_path)

            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []

        filepath = get_abs_path(chroma_config["data_path"])
        # 获取文件夹内所有文件的路径，pdf和 txt的 完整路径
        allow_files_path: list[str] = listdir_with_allowed_type(
            filepath,
            tuple(chroma_config["allow_knowledge_file_type"])
        )

        for path in allow_files_path:
            # 获取文件的 MD5
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"【加载知识库】{path}[该文件的MD5值已经存在了，跳过]")
                continue

            try:
                # 得到文件内容
                documents: list[Document] = get_file_documents(path)
                if not documents:
                    logger.warning(f"【加载知识库】{path}内没有内容，是空文件")

                # 得到文本分块内容
                split_document: list[Document] = self.spliter.split_documents(documents)
                if not split_document:
                    logger.warning(f"【加载知识库】{path}分片后没有有效文本内容，跳过")
                    continue

                # 将内容存入向量库
                self.vector_store.add_documents(split_document)

                # 记录这个已经处理好的文件的MD5值，避免重复下载
                save_md5(md5_hex)

                logger.info(f"【加载知识库】{path}内容加载成功！！")

            except Exception as e:
                # exc_info 为 True 会记录详细的报错堆栈, False仅记录报错信息本身
                logger.error(f"【加载知识库】{path}加载失败：{str(e)}", exc_info=True)
                continue