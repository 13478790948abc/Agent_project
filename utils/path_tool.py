"""
为整个工程提供统一的绝对路径
"""
import os

def get_project_root() -> str:
    """
    获取工程所在的根目录
    :return: 字符串根目录
    """
    # 当前文件的绝对路径 也就是:
    current_file = os.path.abspath(__file__)
    # print(f"current_file:{current_file}")   D:\Agent_p\Agent_project\utils\path_tool.py

    # 获取工程的根目录,先获取文件所在的文件夹绝对路径
    current_dir = os.path.dirname(current_file)
    # print(f"current_dir:{current_dir}")    D:\Agent_p\Agent_project\utils

    # 获取根目录本身
    project_root = os.path.dirname(current_dir)
    # print(f"project_root:{project_root}")  D:\Agent_p\Agent_project

    return project_root

def get_abs_path(relative_path:str) -> str:
    """
    传入相对路径，得到绝对路径
    :param relative_path: 相对路径
    :return: 绝对路径
    """
    project_root = get_project_root()
    return os.path.join(project_root, relative_path)

if __name__ == '__main__':
    print(get_abs_path("config/config.txt"))