# web_poe_api
some useful api from poe.com  
存储的数据格式请直接看json文件
```
import os
from web_poe_api import use_bot,refresh_bot,create_bot
import json
import re
################################################
Path = os.path.dirname(os.path.abspath(__file__))
cookie = 'p-b=cktSb3s2AtYuPthsaZURfQ%3D%3D'
poe_formkey = '130f5fe51cb31eeeb056890004a17a89'
poe_tchannel =  'poe-chan53-8888-ejnafarqnmuzwuvbncmf'
#封包原函数，方便使用
def create_mybot(nickname,prompt,model):
    return create_bot(nickname=nickname,prompt=prompt,model=model,dict_path=rf'{Path}\bot_dict.json',cookie=cookie,poe_formkey=poe_formkey,poe_tchannel=poe_tchannel)

def use_mybot(query,bot):
    with open(rf'{Path}\bot_dict.json', 'r') as f:
        bot_dict = json.load(f)
        return use_bot(query,bot,bot_dict=bot_dict,cookie=cookie,poe_formkey=poe_formkey,poe_tchannel=poe_tchannel)
    
def refresh_mybot(nickname):
    with open(rf'{Path}\bot_dict.json', 'r') as f:
        bot_dict = json.load(f)
    refresh_bot(nickname,bot_dict,cookie,poe_formkey=poe_formkey,poe_tchannel=poe_tchannel)
################################################
# 创建bot，参数依次为nickname，预设prompt，模型（gpt3_5或者claude）
# create_mybot("xhssss","省略一下~~~",'gpt3_5')
# 刷新当前指定bot的对话，参数为nickname
# refresh_mybot('xhssss')
# 与指定bot问答，参数为问题query，nickname询问对象
last_answer,chat_suggest,chat_list_text,chat_list_raw = use_mybot(query="你是谁",bot='xhssss')
print(last_answer)
print(*chat_suggest)




```
