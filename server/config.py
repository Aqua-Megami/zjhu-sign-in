from configparser import ConfigParser
import os, sys
from uuid import uuid4

FILENAME = 'config.ini'

# 修复运行路径
if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.dirname(sys.executable)
    os.chdir(BASE_PATH)
else:
    BASE_PATH = os.path.dirname(__file__)

def initConfig(config: ConfigParser):
    config.add_section('Config')
    config.add_section('Program')
    config.set('Program', 'cookies', '')
    config.set('Config', 'fingerprint', str(uuid4()))

def readConfig(kw:str, section:str='Program'):
    config = ConfigParser()
    if os.path.exists(FILENAME):
        config.read(FILENAME)
    else:
        initConfig(config)
        with open(FILENAME, 'w', encoding='utf-8') as fb:
            config.write(fb)
    result = config.get(section, kw)
    return result

def setConfig(value, kw:str, section:str='Program'):
    config = ConfigParser()
    if os.path.exists(FILENAME):
        config.read(FILENAME)
    else:
        initConfig(config)
    config.set(section, kw, value)
    with open(FILENAME, 'w', encoding='utf-8') as fb:
        config.write(fb)
    

if __name__ == '__main__':
    readConfig('fingerprint')