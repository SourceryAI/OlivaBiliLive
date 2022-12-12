import OlivOS
import OlivaBiliLive

from os import listdir
from os.path import isfile, join
import inspect
from .file_loader import make_folder
from importlib.machinery import SourceFileLoader
from .plugin import BotPlugin

def logg(msg:str,level=2):
    OlivaBiliLive.main.GlobalProc.log(level,f"[OlivaBiliLive] : {msg}")

PLUGINS_DIR = 'plugin/data/OlivaBiliLive/plugins'
make_folder(PLUGINS_DIR)

def load_plugins():
    plugins = [f for f in listdir(PLUGINS_DIR) if isfile(join(PLUGINS_DIR, f)) and f.endswith('.py')]
    bot_plugins = []
    for plugin in plugins:
        try:
            module = SourceFileLoader(plugin[:-3], f'{PLUGINS_DIR}/{plugin}').load_module()
            for (name, cs) in inspect.getmembers(module, inspect.isclass):
                if cs.__base__ == BotPlugin:
                    logg(f'加载插件中... {plugin} ({name})')
                    bot_plugins.append(cs())
                    break
        except Exception as e:
            logg(f'加载插件 {plugin} 时出现错误: {e}')
            
    return bot_plugins
        
