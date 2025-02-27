import requests

# 消除https告警
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置NAS相关信息
nas_ip = 'syn6-2kwxntnrk7iparzj6sgyxe7nxieqeyuiakynuwbeqj2d774uuqfq.a20240219.direct.quickconnect.cn'
nas_port = 5001
username = 'jojojoan'
password = 'Zh118qsj'

# API和参数
api_endpoint = f'https://{nas_ip}:{nas_port}/webapi/entry.cgi'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
# 登录参数
login_params = {
	'api': 'SYNO.API.Auth',
	'version': '6',
	'method': 'login',
	'account': username,
	'passwd': password,
	'session': 'FileStation',
	'format': 'sid'
}

# 发送登录请求
login_response = requests.get(api_endpoint, params=login_params,headers=headers, verify=False)
print(login_response.json())

# 获取会话sid
# session_id = login_response.json()['data']['sid']
