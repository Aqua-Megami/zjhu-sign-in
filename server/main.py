from flask import Flask, request, jsonify, send_from_directory
import requests, pickle, base64, os, webbrowser, threading, time, sys
import config

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
}
session = requests.session()
PORT = 50351

# 修复运行路径
if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.dirname(sys.executable)
    os.chdir(BASE_PATH)
else:
    BASE_PATH = os.path.dirname(__file__)


app = Flask(__name__)

@app.route('/api/hasLogin', methods=['POST'])
def hasLogin():
    cookies = config.readConfig('cookies')
    if not cookies:
        return {'hasLogin': False, 'message': '没有cookies信息，请登录'}
    session.cookies = pickle.loads(base64.b64decode(cookies))
    url = 'https://aifdy.zjhu.edu.cn/api/auth/me'
    try:
        r = session.get(url, headers=HEADERS)
    except Exception as e:
        config.setConfig('', 'token')
        return {'hasLogin': True, 'message': str(e)}
    if r.status_code != 200:
        config.setConfig('', 'token')
        return {'hasLogin': False, 'message': r.json().get('message')}
    return {'hasLogin': True, 'message': r.json().get('message')}

@app.route('/api/login', methods=['POST'])
def login():
    props = request.get_json()
    props['rememberMe'] = True
    url = 'https://aifdy.zjhu.edu.cn/api/auth/login'
    try:
        r = session.post(url, json=props, headers=HEADERS)
    except Exception as e:
        return {'success': False, 'message': str(e)}
    result = r.json()
    if r.status_code != 200:
        return {'success': False, 'message': result.get('message')}
    cookies = base64.b64encode(pickle.dumps(session.cookies))
    config.setConfig(cookies.decode(), 'cookies')
    return {'success': True, 'message': result.get('message')}

@app.route('/api/signin', methods=['POST'])
def signin():
    props = request.get_json()
    props['deviceFingerprint'] = config.readConfig('fingerprint', 'Config')
    try:
        r = session.post('https://aifdy.zjhu.edu.cn/api/checkin', json=props, headers=HEADERS)
    except Exception as e:
        return {'success': False, 'message': str(e), 'data': None}
    result = r.json()
    if r.status_code != 200:
        return {'success': False, 'message': result.get('message'), 'data': None}
    return {'success': True, 'message': result.get('message'), 'data': result.get('data')}

@app.route('/page/<path:path>')
def provide(path):
    file_dir = os.path.join(BASE_PATH, 'dist')
    if not os.path.exists(os.path.join(file_dir, path)):
        response = jsonify({'error': 'Not Found'})
        response.status_code = 404
        return response
    return send_from_directory(file_dir, path)

class OpenSite(threading.Thread):
    def __init__(self, time, url, group = None, target = None, name = None, args = ..., kwargs = None, *, daemon = None):
        self.time = time
        self.url = url
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
    
    def run(self):
        time.sleep(self.time)
        webbrowser.open(self.url)
        return super().run()

if __name__ == '__main__':
    url = f'http://127.0.0.1:{PORT}/page/index.html'
    print(f'请访问: {url}\n\n\n\n')
    OpenSite(1, url).start()
    app.run('127.0.0.1', port=PORT)