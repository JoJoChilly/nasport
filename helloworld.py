#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import urllib3
import getpass
# 导入配置文件 - 修复导入路径
from synology_config import BASE_URL, USERNAME, PASSWORD, DEFAULT_FOLDER

# 禁用不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def login_to_synology(base_url, username, password, timeout=30):
    """登录到Synology NAS并获取sid - 增加超时时间"""
    login_api = f"{base_url}/webapi/auth.cgi"
    # 或者使用 entry.cgi
    # login_api = f"{base_url}/webapi/entry.cgi"
    
    params = {
        "api": "SYNO.API.Auth",
        "version": "3",  # 使用版本3
        "method": "login",
        "account": username,
        "passwd": password,
        "session": "FileStation",  # 修改会话名称为FileStation
        "format": "sid"  # 返回格式
    }
    
    try:
        print(f"正在登录到: {login_api}")
        response = requests.get(login_api, params=params, verify=False, timeout=timeout)
        response.raise_for_status()
        
        result = response.json()
        if result.get("success"):
            sid = result.get("data", {}).get("sid")
            print(f"登录成功！获取到会话ID")
            return sid
        else:
            error_code = result.get("error", {}).get("code")
            print(f"登录失败，错误代码: {error_code}")
            return None
    except Exception as e:
        print(f"登录请求失败: {str(e)}")
        if 'response' in locals():
            print(f"响应内容: {response.text[:200]}...")
        return None

def call_synology_api(base_url, sid=None):
    """调用Synology API并返回结果"""
    api_url = f"{base_url}/webapi/entry.cgi"
    
    params = {
        "api": "SYNO.API.Info",
        "version": "1",
        "method": "query",
        "query": "SYNO.API.Auth,SYNO.FileStation,SYNO.FileStation.List",  # 添加FileStation.List API
    }
    
    # 如果有会话ID，添加到请求参数中
    if sid:
        params["_sid"] = sid
    
    try:
        print(f"正在请求API: {api_url}")
        response = requests.get(api_url, params=params, verify=False, timeout=30)
        response.raise_for_status()
        
        # 简单检查内容类型是否为JSON
        if 'json' not in response.headers.get('content-type', '').lower():
            print(f"警告: 响应可能不是JSON格式 (内容类型: {response.headers.get('content-type')})")
        
        return response.json()
    except Exception as e:
        print(f"API请求失败: {str(e)}")
        if 'response' in locals():
            print(f"响应内容: {response.text[:200]}...")
        return None

def logout_from_synology(base_url, sid):
    """从Synology NAS注销"""
    logout_api = f"{base_url}/webapi/auth.cgi"
    # 或者使用 entry.cgi
    # logout_api = f"{base_url}/webapi/entry.cgi"
    
    params = {
        "api": "SYNO.API.Auth",
        "version": "1",
        "method": "logout",
        "session": "FileStation",  # 修改会话名称为FileStation，与登录保持一致
        "_sid": sid
    }
    
    try:
        print("正在注销...")
        response = requests.get(logout_api, params=params, verify=False, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get("success"):
            print("注销成功！")
            return True
        else:
            print(f"注销失败，错误代码: {result.get('error', {}).get('code')}")
            return False
    except Exception as e:
        print(f"注销请求失败: {str(e)}")
        return False

def list_shares(base_url, sid):
    """列出所有共享文件夹"""
    api_url = f"{base_url}/webapi/entry.cgi"
    
    params = {
        "api": "SYNO.FileStation.List",
        "version": "2",
        "method": "list_share",
        "_sid": sid
    }
    
    try:
        print("\n正在获取共享文件夹列表...")
        response = requests.get(api_url, params=params, verify=False, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get("success"):
            shares = result.get("data", {}).get("shares", [])
            print(f"成功获取到 {len(shares)} 个共享文件夹")
            
            if len(shares) > 0:
                # 打印共享文件夹列表
                print("\n共享文件夹:")
                print("-" * 80)
                print(f"{'名称':<30} {'路径':<40} {'描述':<30}")
                print("-" * 80)
                
                for share in shares:
                    name = share.get("name", "未知")
                    path = share.get("path", "未知")
                    desc = share.get("desc", "")
                    
                    print(f"{name:<30} {path:<40} {desc:<30}")
            else:
                print("没有找到共享文件夹")
            
            return shares
        else:
            error_code = result.get("error", {}).get("code")
            print(f"获取共享文件夹列表失败，错误代码: {error_code}")
            return None
    except Exception as e:
        print(f"获取共享文件夹列表请求失败: {str(e)}")
        if 'response' in locals():
            print(f"响应内容: {response.text[:200]}...")
        return None

def list_folder_contents(base_url, sid, folder_path):
    """列出指定文件夹的内容"""
    api_url = f"{base_url}/webapi/entry.cgi"
    
    params = {
        "api": "SYNO.FileStation.List",
        "version": "2",
        "method": "list",
        "folder_path": folder_path,
        "additional": "size,time,perm,type",
        "_sid": sid
    }
    
    try:
        print(f"\n正在获取 '{folder_path}' 的内容...")
        response = requests.get(api_url, params=params, verify=False, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get("success"):
            files = result.get("data", {}).get("files", [])
            print(f"成功获取到 {len(files)} 个文件/文件夹")
            
            if len(files) > 0:
                # 打印文件列表
                print("\n目录内容:")
                print("-" * 80)
                print(f"{'名称':<30} {'类型':<10} {'大小':<15} {'修改时间':<20}")
                print("-" * 80)
                
                for file in files:
                    name = file.get("name", "未知")
                    is_dir = "文件夹" if file.get("isdir", False) else "文件"
                    
                    # 获取文件大小
                    size = file.get("additional", {}).get("size", 0)
                    if size < 1024:
                        size_str = f"{size} 字节"
                    elif size < 1024 * 1024:
                        size_str = f"{size/1024:.2f} KB"
                    else:
                        size_str = f"{size/(1024*1024):.2f} MB"
                    
                    # 获取修改时间
                    mtime = file.get("additional", {}).get("time", {}).get("mtime", 0)
                    from datetime import datetime
                    mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                    
                    print(f"{name:<30} {is_dir:<10} {size_str:<15} {mtime_str:<20}")
            else:
                print("文件夹是空的")
            
            return files
        else:
            error_code = result.get("error", {}).get("code")
            print(f"获取文件夹内容失败，错误代码: {error_code}")
            return None
    except Exception as e:
        print(f"获取文件夹内容请求失败: {str(e)}")
        if 'response' in locals():
            print(f"响应内容: {response.text[:200]}...")
        return None

def get_api_info(base_url, sid):
    """获取FileStation API的详细信息"""
    api_url = f"{base_url}/webapi/entry.cgi"
    
    params = {
        "api": "SYNO.API.Info",
        "version": "1",
        "method": "query",
        "query": "all",  # 获取所有API信息
        "_sid": sid
    }
    
    try:
        print("\n正在获取API信息...")
        response = requests.get(api_url, params=params, verify=False, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get("success"):
            # 只列出与FileStation相关的API
            fs_apis = {k: v for k, v in result.get("data", {}).items() if "FileStation" in k}
            print("可用的FileStation API:")
            for api_name, api_info in fs_apis.items():
                print(f"  - {api_name} (版本: {api_info.get('maxVersion')})")
            return fs_apis
        else:
            print(f"获取API信息失败: {result}")
            return None
    except Exception as e:
        print(f"获取API信息请求失败: {str(e)}")
        return None

def search_videos(base_url, sid, search_path=None, extension=None):
    """搜索指定路径中的视频文件"""
    api_url = f"{base_url}/webapi/entry.cgi"
    
    # 常见视频文件扩展名
    video_extensions = [
        "mp4", "mkv", "avi", "mov", "wmv", "flv", "webm", "m4v", 
        "mpg", "mpeg", "3gp", "ts", "mts", "m2ts"
    ]
    
    # 如果没有指定扩展名，使用所有视频扩展名
    if extension is None:
        extensions = video_extensions
    else:
        extensions = [extension]
    
    # 构建扩展名过滤条件
    extension_filter = "|".join(f"*.{ext}" for ext in extensions)
    
    params = {
        "api": "SYNO.FileStation.Search",
        "version": "2",
        "method": "start",
        "folder_path": search_path if search_path else None,
        "pattern": extension_filter,
        "extension": ",".join(extensions),
        "additional": "size,time",
        "recursive": True,  # 添加递归搜索
        "_sid": sid
    }
    
    try:
        print(f"\n正在搜索视频文件...")
        response = requests.get(api_url, params=params, verify=False, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get("success"):
            task_id = result.get("data", {}).get("taskid")
            print(f"搜索任务已启动，任务ID: {task_id}")
            
            # 检查搜索状态并获取结果
            return get_search_results(base_url, sid, task_id)
        else:
            error_code = result.get("error", {}).get("code")
            print(f"启动搜索任务失败，错误代码: {error_code}")
            return None
    except Exception as e:
        print(f"搜索请求失败: {str(e)}")
        if 'response' in locals():
            print(f"响应内容: {response.text[:200]}...")
        return None

def get_search_results(base_url, sid, task_id, max_retries=10):
    """获取搜索结果"""
    api_url = f"{base_url}/webapi/entry.cgi"
    
    retries = 0
    files_found = []
    finished = False
    
    while not finished and retries < max_retries:
        params = {
            "api": "SYNO.FileStation.Search",
            "version": "2",
            "method": "list",
            "taskid": task_id,
            "offset": len(files_found),
            "limit": 100,  # 每次获取100个结果
            "sort_by": "name",
            "sort_direction": "ASC",
            "additional": "size,time",
            "_sid": sid
        }
        
        try:
            response = requests.get(api_url, params=params, verify=False, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                finished = data.get("finished", False)
                current_files = data.get("files", [])
                files_found.extend(current_files)
                
                if not current_files:
                    # 如果没有新的结果，等待一下再重试
                    import time
                    time.sleep(1)
                    
                print(f"已找到 {len(files_found)} 个视频文件，搜索完成: {finished}")
                retries += 1
            else:
                error_code = result.get("error", {}).get("code")
                print(f"获取搜索结果失败，错误代码: {error_code}")
                break
        except Exception as e:
            print(f"获取搜索结果请求失败: {str(e)}")
            break
    
    # 完成搜索，清理任务
    clean_search_task(base_url, sid, task_id)
    
    # 搜索完成，显示结果
    if files_found:
        print("\n找到的视频文件:")
        print("-" * 100)
        print(f"{'名称':<60} {'大小':<15} {'修改时间':<20}")
        print("-" * 100)
        
        for file in files_found:
            name = file.get("name", "未知")
            path = file.get("path", "未知")
            
            # 获取文件大小
            size = file.get("additional", {}).get("size", 0)
            if size < 1024:
                size_str = f"{size} 字节"
            elif size < 1024 * 1024:
                size_str = f"{size/1024:.2f} KB"
            elif size < 1024 * 1024 * 1024:
                size_str = f"{size/(1024*1024):.2f} MB"
            else:
                size_str = f"{size/(1024*1024*1024):.2f} GB"
            
            # 获取修改时间
            mtime = file.get("additional", {}).get("time", {}).get("mtime", 0)
            from datetime import datetime
            mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"{name:<60} {size_str:<15} {mtime_str:<20}")
            # 打印完整路径
            print(f"  路径: {path}")
            print("-" * 100)
    else:
        print("未找到任何视频文件")
    
    return files_found

def clean_search_task(base_url, sid, task_id):
    """清理搜索任务"""
    api_url = f"{base_url}/webapi/entry.cgi"
    
    params = {
        "api": "SYNO.FileStation.Search",
        "version": "2",
        "method": "stop",
        "taskid": task_id,
        "_sid": sid
    }
    
    try:
        response = requests.get(api_url, params=params, verify=False, timeout=30)
        response.raise_for_status()
        # 不需要检查结果，这只是清理操作
    except Exception as e:
        print(f"清理搜索任务失败: {str(e)}")

def search_videos_alternative(base_url, sid, search_path=None, timeout=30):
    """使用list_files方式递归查找视频文件 - 增加超时时间"""
    api_url = f"{base_url}/webapi/entry.cgi"
    
    # 常见视频文件扩展名
    video_extensions = [
        "mp4", "mkv", "avi", "mov", "wmv", "flv", "webm", "m4v", 
        "mpg", "mpeg", "3gp", "ts", "mts", "m2ts"
    ]
    
    all_videos = []
    folders_to_check = [search_path]
    checked_folders = set()
    
    print(f"\n开始在 {search_path} 及其子文件夹中查找视频文件...")
    print(f"已将请求超时时间设置为 {timeout} 秒")
    
    while folders_to_check:
        current_folder = folders_to_check.pop(0)
        if current_folder in checked_folders:
            continue
            
        checked_folders.add(current_folder)
        print(f"正在检查文件夹: {current_folder}")
        
        # 列出当前文件夹内容
        params = {
            "api": "SYNO.FileStation.List",
            "version": "2",
            "method": "list",
            "folder_path": current_folder,
            "additional": "size,time",
            "_sid": sid
        }
        
        # 添加重试机制
        max_retries = 3
        retry_count = 0
        success = False
        
        while not success and retry_count < max_retries:
            try:
                retry_count += 1
                response = requests.get(api_url, params=params, verify=False, timeout=timeout)
                response.raise_for_status()
                success = True
                
                result = response.json()
                if result.get("success"):
                    files = result.get("data", {}).get("files", [])
                    
                    for file in files:
                        name = file.get("name", "")
                        path = file.get("path", "")
                        is_dir = file.get("isdir", False)
                        
                        if is_dir:
                            # 将子文件夹添加到待检查列表
                            folders_to_check.append(path)
                        else:
                            # 检查文件是否为视频文件
                            file_ext = name.split(".")[-1].lower() if "." in name else ""
                            if file_ext in video_extensions:
                                all_videos.append(file)
                                print(f"找到视频文件: {path}")
                else:
                    error_code = result.get("error", {}).get("code")
                    print(f"获取文件夹内容失败，错误代码: {error_code}")
            except requests.exceptions.Timeout:
                if retry_count < max_retries:
                    print(f"请求超时，正在进行第 {retry_count}/{max_retries} 次重试...")
                else:
                    print(f"多次请求超时，跳过文件夹: {current_folder}")
            except Exception as e:
                if retry_count < max_retries:
                    print(f"请求失败: {str(e)}，正在进行第 {retry_count}/{max_retries} 次重试...")
                else:
                    print(f"多次请求失败，跳过文件夹: {current_folder}")
                    print(f"错误详情: {str(e)}")
    
    # 显示所有找到的视频文件
    if all_videos:
        print(f"\n总共找到 {len(all_videos)} 个视频文件:")
        print("-" * 100)
        print(f"{'名称':<60} {'大小':<15} {'修改时间':<20}")
        print("-" * 100)
        
        for file in all_videos:
            name = file.get("name", "未知")
            path = file.get("path", "未知")
            
            # 获取文件大小
            size = file.get("additional", {}).get("size", 0)
            if size < 1024:
                size_str = f"{size} 字节"
            elif size < 1024 * 1024:
                size_str = f"{size/1024:.2f} KB"
            elif size < 1024 * 1024 * 1024:
                size_str = f"{size/(1024*1024):.2f} MB"
            else:
                size_str = f"{size/(1024*1024*1024):.2f} GB"
            
            # 获取修改时间
            mtime = file.get("additional", {}).get("time", {}).get("mtime", 0)
            from datetime import datetime
            mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"{name:<60} {size_str:<15} {mtime_str:<20}")
            print(f"  路径: {path}")
            print("-" * 100)
        
        # 保存文件名到文本文件
        save_video_filenames_to_txt(all_videos, "video_files.txt", mp4_only=True)  # 只保存MP4文件
        # 如果您想保存所有视频文件，将mp4_only设置为False
    else:
        print("未找到任何视频文件")
    
    return all_videos

def save_video_filenames_to_txt(videos, output_file="video_files.txt", mp4_only=True):
    """将视频文件名保存到文本文件"""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            total_saved = 0
            f.write("# 视频文件列表\n")
            f.write("# 格式：文件名 (文件路径)\n")
            f.write("-" * 80 + "\n\n")
            
            for video in videos:
                name = video.get("name", "未知")
                path = video.get("path", "未知")
                
                # 如果只保存MP4文件
                if mp4_only and not name.lower().endswith(".mp4"):
                    continue
                    
                f.write(f"{name} ({path})\n")
                total_saved += 1
            
            f.write(f"\n# 总计: {total_saved} 个文件")
            
        print(f"\n已将{'' if not mp4_only else 'MP4'}视频文件名保存到 {output_file}，共 {total_saved} 个文件")
        return True
    except Exception as e:
        print(f"保存文件名到文本文件失败: {str(e)}")
        return False

def main():
    """主函数"""
    # 使用配置文件中的BASE_URL
    base_url = BASE_URL
    
    # 使用配置文件中的USERNAME和PASSWORD
    username = USERNAME
    password = PASSWORD
    
    # 设置更长的超时时间
    timeout = 300  # 5分钟
    
    # 登录并获取会话ID
    sid = login_to_synology(base_url, username, password, timeout=timeout)
    
    if sid:
        # 使用会话ID调用API
        print("\n正在调用API...")
        result = call_synology_api(base_url, sid)
        
        if result:
            print("API调用成功！结果如下:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 获取API信息
            api_info = get_api_info(base_url, sid)
            
            # 获取共享文件夹列表
            shares = list_shares(base_url, sid)
            
            if shares and len(shares) > 0:
                # 查找名为"video"的共享文件夹
                video_share = next((share for share in shares if share.get("name") == "video"), None)
                if video_share:
                    video_path = video_share.get("path")
                    print(f"\n在video共享文件夹中搜索视频文件: {video_path}")
                    
                    # 使用新的递归查找方法，传递超时时间
                    videos = search_videos_alternative(base_url, sid, video_path, timeout=timeout)
                    
                    if videos:
                        # 询问用户是否只保存MP4文件
                        save_mp4_only = input("\n是否只保存MP4文件？(Y/N): ").upper() == 'Y'
                        output_file = input("请输入保存文件名 (默认: video_files.txt): ") or "video_files.txt"
                        save_video_filenames_to_txt(videos, output_file, mp4_only=save_mp4_only)
                else:
                    print("没有找到video共享文件夹")
        else:
            print("API调用失败")
        
        # 注销
        logout_from_synology(base_url, sid)
    else:
        print("由于登录失败，无法继续操作")

if __name__ == "__main__":
    main() 