import OlivOS
import OlivaBiliLive

import asyncio
from genericpath import exists
from aiohttp.client import ClientSession
import json
from .bilibili_bot import OlivaBiliLiveBot
from .file_loader import load_default_config, make_folder
from .plugins_loader import load_plugins
from .bilibili_api import get_cookies, login, user_cookies
from functools import wraps

SESSION_DATA_PATH = 'plugin/data/OlivaBiliLive/data/session.json'
CONNECT_ORDER = '直播间连接' # 设定连接直播间的指令
DISCONNECT_ORDER = '直播间断连' # 设定退出直播间的指令

GlobalProc = None

class Event(object):
    def init(plugin_event, Proc):
        global GlobalProc
        GlobalProc = Proc 

    def private_message(plugin_event, Proc):
        reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        reply(plugin_event, Proc)

    def poke(plugin_event, Proc):
        pass

    def save(plugin_event, Proc):
        logging_info("关闭服务ing...")

    def menu(plugin_event, Proc):
        if plugin_event.data.namespace == 'OlivaBiliLive':  # type: ignore
            if plugin_event.data.event == 'OlivaBiliLive_Menu_Config':  # type: ignore
                logging_info("有笨蛋打开了配置")
            elif plugin_event.data.event == 'OlivaBiliLive_Menu_About':  # type: ignore
                logging_info("有笨蛋打开了关于选项框")

def logging_info(msg,level=2):
    GlobalProc.log(level,f"[OlivaBiliLive] : {msg}")


# def decorator(func):
#     @wraps(func)
#     def wrapper(*args,**kwargs):
#         return f'{arg[0]}' #func(*args,**kwargs)
#     return wrapper

# # 使用装饰器
# @decorator
# def logging_info(msg):
#     GlobalProc.log(level=2, f"[OlivaBiliLive] : {msg}")

def reply(plugin_event,Proc):
    # TODO(2022年12月11日): 房间号由`congfig.yml`入参|指令触发时入参。
    
    if plugin_event.data.message[:len(CONNECT_ORDER)] == CONNECT_ORDER:
        make_folder('plugin/data/OlivaBiliLive/data')
        make_folder('plugin/conf/OlivaBiliLive/config')
        make_folder('plugin/data/OlivaBiliLive/plugins')
        
        data = load_default_config()

        # logging.basicConfig(level=logging.INFO if not data['debug'] else logging.DEBUG)

        room = data['roomid']

        OlivaBiliLiveBot.BOT_PLUGINS = load_plugins()
        asyncio.run(start(room))
    elif plugin_event.data.message[:len(DISCONNECT_ORDER)] == DISCONNECT_ORDER:
        pass


async def start(room: int):
    cookies = {}
    # 有上次的 session
    session_exist = exists(SESSION_DATA_PATH)
    if session_exist:
        with open(SESSION_DATA_PATH) as f:
            cookies = json.load(f)
    # 加到 cookies
    user_cookies.update_cookies(cookies)
    async with ClientSession(cookie_jar=user_cookies) as session:
        # 嘗試登入
        success = await login(session)
        # 成功登入
        if success:

            uid = get_cookies('DedeUserID')
            jct = get_cookies('bili_jct')

            if uid == None or jct == None:
                logging_info(f'获取 cookies 失败')
                return
            if not session_exist:

                for cookie in user_cookies:
                    cookies[cookie.key] = cookie.value

                logging_info(f'已储存 cookies: {cookies}')
                with open(SESSION_DATA_PATH, mode='w') as f:
                    json.dump(cookies, f)

            bot = OlivaBiliLiveBot(room_id=room, uid=int(uid), session=session, loop=session._loop)
            await bot.init_room()
            logging_info("已启动服务~")
            await bot.start()
            #while True:
            #    await asyncio.sleep(60)
            await bot.close()
            logging_info('已关闭服务~')
        else:
            exit()
    

