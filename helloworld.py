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

def login_to_synology(base_url, username, password):
    """登录到Synology NAS并获取sid"""
    login_api = f"{base_url}/webapi/auth.cgi"
    # 或者使用 entry.cgi
    # login_api = f"{base_url}/webapi/entry.cgi"
    
    params = {
        "api": "SYNO.API.Auth",
        "version": "3",  # 使用版本3
        "method": "login",
        "account": username,
        "passwd": password,
        "session": "DownloadStation",  # 会话名称
        "format": "sid"  # 返回格式
    }
    
    try:
        print(f"正在登录到: {login_api}")
        response = requests.get(login_api, params=params, verify=False, timeout=30)
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
        "query": "SYNO.API.Auth,SYNO.FileStation"
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
        "session": "DownloadStation",
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

def main():
    """主函数"""
    # 使用配置文件中的BASE_URL
    base_url = BASE_URL
    
    # 使用配置文件中的USERNAME和PASSWORD
    username = USERNAME
    password = PASSWORD
    
    # 登录并获取会话ID
    sid = login_to_synology(base_url, username, password)
    
    if sid:
        # 使用会话ID调用API
        print("\n正在调用API...")
        result = call_synology_api(base_url, sid)
        
        if result:
            print("API调用成功！结果如下:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 这里可以使用DEFAULT_FOLDER进行其他操作
            print(f"默认文件夹路径: {DEFAULT_FOLDER}")
        else:
            print("API调用失败")
        
        # 注销
        logout_from_synology(base_url, sid)
    else:
        print("由于登录失败，无法继续操作")

if __name__ == "__main__":
    main() 