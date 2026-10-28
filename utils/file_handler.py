import os, hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# 获取文件的 md5的十六进制字符串
def get_file_md5_hex(filepath):

    if not os.path.exists(filepath):
        logger.error(f"[md5计算] The file does not exist{filepath}")
        return

    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径{filepath}不是文件")
        return

    md5_obj = hashlib.md5()
    chunk_size = 4096    # 4KB 分片，避免文件过大爆内存
    try:
        with open(filepath, "rb") as f:     # 必须二进制读取
            while chunk := f.read(chunk_size):
                # 分块读取，每读一块就交给 MD5 更新内部状态
                # 全部读完后，hexdigest() 得到整个文件的最终 MD5，并转成十六进制字符串。
                md5_obj.update(chunk)
        md5_hex = md5_obj.hexdigest()
        return md5_hex
    except Exception as e:
        logger.error(f"计算文件{filepath}md5失败，{str(e)}")
        return None

# 返回文件夹内符合后缀要求的文件路径元组
def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    # 列表容器，暂存符合条件的文件完整路径
    files = []

    if not os.path.isdir(path):
        logger.error(f"【获取允许的文件类型listdir_with_allowed_type{path}不是文件夹")
        return allowed_types

    # os.listdir 返回目录下所有内容，f 只是文件名(1.txt)这种
    for f in os.listdir(path):
        # 仅当它是文件，且文件名以 allowed_types 中某个后缀结尾时收录
        if f.endswith(allowed_types):
            # 返回文件路径
            files.append(os.path.join(path, f))

    # 返回不可变元组，避免调用方误修改结果
    return tuple(files)

# 加载 pdf文档
def pdf_loader(filepath:str, password=None) -> list[Document]:
    return PyPDFLoader(filepath, password).load()

# 加载 txt文档
def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()