import os
import mimetypes
from typing import List, Dict
from datetime import datetime
from dataclasses import dataclass

@dataclass
class FileMetadata:
    """文件元数据类"""
    file_path: str
    file_name: str
    file_type: str
    file_ext: str
    size: int
    last_modified: datetime
    basic_properties: Dict[str, str]


def get_basic_properties(file_metadata) -> Dict[str, str]:
    """获取文件的基础属性"""
    # 文件类型描述
    type_desc = "未知类型"
    if file_metadata.file_type.startswith('video/'):
        type_desc = "视频文件"
    elif file_metadata.file_type.startswith('audio/'):
        type_desc = "音频文件"
    elif file_metadata.file_type.startswith('image/'):
        type_desc = "图片文件"
    elif file_metadata.file_type.startswith('application/pdf'):
        type_desc = "PDF文档"
    elif 'word' in file_metadata.file_type or file_metadata.file_ext == '.docx':
        type_desc = "Word文档"

    # 文件大小描述
    size_mb = file_metadata.size / (1024 * 1024)
    if size_mb < 1:
        size_desc = "小文件"
    elif size_mb < 10:
        size_desc = "中等文件"
    else:
        size_desc = "大文件"

    # 更新时间描述
    days_diff = (datetime.now() - file_metadata.last_modified).days
    if days_diff < 7:
        time_desc = "最近更新"
    elif days_diff < 30:
        time_desc = "本月更新"
    else:
        time_desc = "较早更新"

    return {
        "file_type": file_metadata.file_type,
        "file_extension": file_metadata.file_ext,
        "size_bytes": str(file_metadata.size),
        "size_category": size_desc,
        "type_category": type_desc,
        "last_modified": file_metadata.last_modified.isoformat(),
        "update_status": time_desc,
        "full_path": file_metadata.file_path
    }


def get_file_metadata(file_path: str) -> FileMetadata:
    """获取文件的基本元数据"""
    file_stat = os.stat(file_path)
    file_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    file_ext = os.path.splitext(file_path)[1].lower()

    metadata = FileMetadata(
        file_path=file_path,
        file_name=os.path.basename(file_path),
        file_type=file_type,
        file_ext=file_ext,
        size=file_stat.st_size,
        last_modified=datetime.fromtimestamp(file_stat.st_mtime),
        tags=[],
        basic_properties={}
    )

    # 添加基础属性
    metadata.basic_properties = get_basic_properties(metadata)

    return metadata
#
#
# def process_files() -> List[FileMetadata]:
#     """处理所有文件并返回文件元数据列表"""
#     file_metadata_list = []
#
#     for root, _, files in os.walk(RESOURCE_DIR):
#         for file in files:
#             file_path = os.path.join(root, file)
#             try:
#                 metadata = get_file_metadata(file_path)
#                 file_metadata_list.append(metadata)
#                 print(f"已获取文件元数据: {file}")
#             except Exception as e:
#                 print(f"处理文件出错 {file}: {str(e)}")
#
#     return file_metadata_list