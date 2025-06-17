import time
import json
import os
from typing import List, Dict, Any, Coroutine
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tools.data_tools import DataTools

# Create MCP server
mcp = FastMCP("Nexent_MCP", port=5011)

# Load environment variables
load_dotenv()

# Initialize DataTools
data_tools = DataTools()

# @mcp.tool(name="dispatch_files", description="判断路径类型，并返回所有待处理的文件路径列表")
# async def dispatch_files(path: str) -> List[str]:
#     """
#     如果是单个文件，返回包含这个文件的列表
#     如果是目录，递归遍历其中所有文件
#     返回所有有效文件路径列表（自动忽略不支持的格式）
#     """
#     valid_extensions = (".pdf", ".docx", ".txt", ".xlsx", ".png", ".jpg")
#     result_files = []
#
#     if os.path.isfile(path):
#         result_files.append(path)
#     elif os.path.isdir(path):
#         for root, _, files in os.walk(path):
#             for file in files:
#                 if file.lower().endswith(valid_extensions):
#                     result_files.append(os.path.join(root, file))
#     else:
#         raise ValueError(f"路径无效：{path}")
#
#     return result_files

@mcp.tool(name="read_files", description="判断路径类型是单个文件还是文件夹")
async def read_files(path: str) -> str:
    valid_extensions = (".pdf", ".docx", ".txt", ".xlsx", ".png", ".jpg")
    file_names = []

    if os.path.isfile(path):
        print("处理单个文件")
        file_names.append(path)
    elif os.path.isdir(path):
        print("处理目录")
        for root, dirs, files in os.walk(path):
            for file in files:
                print(f"\n--- 处理文件: {file} ---")
                print(f"文件小写: {file.lower()}")
                if file.lower().endswith(valid_extensions):
                    file_names.append(os.path.join(root, file))
    else:
        raise ValueError(f"路径无效：{path}")

    print(f"最终返回的文件列表: {file_names}")
    result = '\n'.join(file_names)

    print(f"返回结果: {result}")
    return result

@mcp.tool(name="analyze_data", description="读取并分析指定路径的文件，生成描述信息")
async def analyze_data(file_path: str):
    """
    读取并分析文件内容，生成描述信息
    参数:
        file_path: 文件路径
    返回:
        包含文件描述信息的 JSON 字符串
    """
    print("开始测试：")
    try:
        result = data_tools.read_and_analyze(file_path)
        return result
    except Exception as e:
        return str(e)


@mcp.tool(name="generate_tags", description="根据文件描述生成标签")
async def generate_tags(description: str) -> str:
    """
    根据描述文本生成标签
    参数:
        description: 描述文本
    返回:
        用逗号分隔的标签字符串
    """
    tags = data_tools.generate_tags(description)
    return json.dumps(tags, ensure_ascii=False)

@mcp.tool(name="publish_to_datahub", description="发布信息到DataHub")
async def publish_to_datahub(file_path: str, description: str, tags: List[str])-> str:
    """
    将文件信息、标签和自定义属性发布到DataHub
    参数:
        file_path: 文件路径
        description: 描述信息
        tags: 标签列表
    返回:
        发布结果
    """
    return data_tools.publish_to_datahub(file_path, description, tags)

if __name__ == "__main__":
    print("Starting Search Tools MCP Server...")
    mcp.run(transport="sse")
