import requests
import json
import re 
import io
from bs4 import BeautifulSoup
import time
import uuid
################################################
def get_key(cookie,path):
    url = f'https://poe.com/{path}'
    headers = {
        'authority': 'poe.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    match = re.search(r'/_next/static/(\w+)/_buildManifest.js', response.text)
    key = match.group(1)
    return key
################################################
def get_chatid(cookie,key,path):
    url = f'https://poe.com/_next/data/{key}/{path}.json?handle={path}'
    headers = {
        'authority': 'poe.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    data = {
        'handle': 'ChatGPT'
    }
    response = requests.get(url, headers=headers, params=data)

    chat_id = re.search('"chatId":(\d+)', response.text).group(1)

    return int(chat_id)
################################################
def generate_uuid(s):
    # 将字符串转换为 UUID 对象
    uuid_object = uuid.uuid3(uuid.NAMESPACE_DNS, s)
    # 获取 UUID 对象的 bytes 值
    uuid_bytes = uuid_object.bytes
    # 将 bytes 值转换为字符串
    uuid_str = uuid_bytes.hex()[:8]
    return uuid_str
################################################
def send_query(query,bot,bot_dict,cookie,poe_formkey,poe_tchannel):
    

    url = 'https://poe.com/api/gql_POST'
    headers = {
    'authority':'poe.com',
    'method':'POST',
    'path':'/api/gql_POST',
    'scheme':'https',
    'accept':'*/*',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-length':'1584',
    'content-type': 'application/json',
    'cookie':cookie,
    'origin':'https://poe.com',
    'poe-formkey':poe_formkey,
    'poe-tchannel':poe_tchannel,
    'pragma':'no-cache',
    'sec-ch-ua':'"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39'
    }
    data = {
        "queryName":
        "chatHelpers_sendMessageMutation_Mutation",
        "variables": {
            "chatId": bot_dict['chatid'][bot],
            "bot": bot_dict['botname'][bot],
            "query": query,
            "source": None,
            "withChatBreak": False,
            "clientNonce": "aFqdtuLYX9q9jmiO"
        },
        "query":
        "mutation chatHelpers_sendMessageMutation_Mutation(\n  $chatId: BigInt!\n  $bot: String!\n  $query: String!\n  $source: MessageSource\n  $withChatBreak: Boolean!\n  $clientNonce: String\n) {\n  messageEdgeCreate(chatId: $chatId, bot: $bot, query: $query, source: $source, withChatBreak: $withChatBreak, clientNonce: $clientNonce) {\n    chatBreak {\n      cursor\n      node {\n        id\n        messageId\n        text\n        author\n        suggestedReplies\n        creationTime\n        state\n      }\n      id\n    }\n    message {\n      cursor\n      node {\n        id\n        messageId\n        text\n        author\n        suggestedReplies\n        creationTime\n        state\n        clientNonce\n        chat {\n          shouldShowDisclaimer\n          id\n        }\n      }\n      id\n    }\n  }\n}\n"
    }
    with requests.Session() as session:
        session.headers.update(headers)
        response = session.post(url, data=json.dumps(data))

    json_data = json.loads(response.content)
    time = json_data['data']['messageEdgeCreate']['message']['node']['creationTime']
    return time
################################################
def get_answer(cookie,bot_path):
    # 带有请求头的 HTTP GET 请求示例

    headers = {
        'authority': 'poe.com',
        'method': 'GET',
        'path': f'/{bot_path}',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'cookie': cookie,
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39'
    }

    session = requests.Session()
    response = session.get(f'https://poe.com/{bot_path}', headers=headers)
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">*(.*?)</script>', response.text, re.DOTALL)

    json_data = match.group(1)
    json_obj = json.loads(json_data)

    chat_list_raw = json_obj["props"]["pageProps"]["payload"]["chatOfBotDisplayName"]["messagesConnection"]["edges"]

    chat_list_raw = [a["node"] for a in chat_list_raw]
    chat_list_text = [a["text"] for a in chat_list_raw]
    chat_suggest = [a["suggestedReplies"] for a in chat_list_raw]
    last_time = chat_list_raw[-1]['creationTime']
    return chat_list_text,chat_suggest,chat_list_raw,last_time

################################################
def create_bot(nickname,prompt,model,dict_path,cookie,poe_formkey,poe_tchannel,):
    url = 'https://poe.com/api/gql_POST'
    true_id = str(generate_uuid(nickname))
    model_dict = {"gpt3_5":"chinchilla","claude":"a2"}
    headers = {
        'authority': 'poe.com',
        'method': 'POST',
        'path': '/api/gql_POST',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '2141',
        'content-type': 'application/json',
        'cookie': cookie,
        'origin': 'https://poe.com',
        'poe-formkey': poe_formkey,
        'poe-tchannel': poe_tchannel,
        'referer': 'https://poe.com/create_bot',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    data = {
        "queryName": "CreateBotMain_poeBotCreate_Mutation",
        "variables": {
            "model": model_dict[model],
            "handle": true_id,
            "prompt": prompt,
            "isPromptPublic": True,
            "introduction": "",
            "description": "",
            "profilePictureUrl": None,
            "apiUrl": None,
            "apiKey": "S7G9lossJOCEOB6iYFUkcBTH7RN3hStW",
            "isApiBot": False,
            "hasLinkification": True,
            "hasMarkdownRendering": True,
            "hasSuggestedReplies": True,
            "isPrivateBot": True
        },
        "query": "mutation CreateBotMain_poeBotCreate_Mutation(\n  $model: String!\n  $handle: String!\n  $prompt: String!\n  $isPromptPublic: Boolean!\n  $introduction: String!\n  $description: String!\n  $profilePictureUrl: String\n  $apiUrl: String\n  $apiKey: String\n  $isApiBot: Boolean\n  $hasLinkification: Boolean\n  $hasMarkdownRendering: Boolean\n  $hasSuggestedReplies: Boolean\n  $isPrivateBot: Boolean\n) {\n  poeBotCreate(model: $model, handle: $handle, promptPlaintext: $prompt, isPromptPublic: $isPromptPublic, introduction: $introduction, description: $description, profilePicture: $profilePictureUrl, apiUrl: $apiUrl, apiKey: $apiKey, isApiBot: $isApiBot, hasLinkification: $hasLinkification, hasMarkdownRendering: $hasMarkdownRendering, hasSuggestedReplies: $hasSuggestedReplies, isPrivateBot: $isPrivateBot) {\n    status\n    bot {\n      id\n      ...BotHeader_bot\n    }\n  }\n}\n\nfragment BotHeader_bot on Bot {\n  displayName\n  messageLimit {\n    dailyLimit\n  }\n  ...BotImage_bot\n  ...BotLink_bot\n  ...IdAnnotation_node\n  ...botHelpers_useViewerCanAccessPrivateBot\n  ...botHelpers_useDeletion_bot\n}\n\nfragment BotImage_bot on Bot {\n  displayName\n  ...botHelpers_useDeletion_bot\n  ...BotImage_useProfileImage_bot\n}\n\nfragment BotImage_useProfileImage_bot on Bot {\n  image {\n    __typename\n    ... on LocalBotImage {\n      localName\n    }\n    ... on UrlBotImage {\n      url\n    }\n  }\n  ...botHelpers_useDeletion_bot\n}\n\nfragment BotLink_bot on Bot {\n  displayName\n}\n\nfragment IdAnnotation_node on Node {\n  __isNode: __typename\n  id\n}\n\nfragment botHelpers_useDeletion_bot on Bot {\n  deletionState\n}\n\nfragment botHelpers_useViewerCanAccessPrivateBot on Bot {\n  isPrivateBot\n  viewerIsCreator\n}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data)) 
    path = true_id
    key = get_key(cookie,path)
    chatid = get_chatid(cookie,key,path)
    with open(dict_path, 'r') as f:
        bot_dict = json.load(f)
    bot_dict['botname'][nickname] = true_id
    bot_dict['chatid'][nickname] = chatid # 这里的0是chatid的默认值
    bot_dict['path'][nickname] = true_id    
    # 将更新后的字典写回到JSON文件中
    with open(dict_path, 'w') as f:
        json.dump(bot_dict, f)
    return true_id
################################################
def refresh_bot(bot,dict_bot,cookie,poe_formkey,poe_tchannel):
    url = 'https://poe.com/api/gql_POST'
    headers = {
        'authority': 'poe.com',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'content-length': '738',
        'cookie': f'{cookie}; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1',
        'origin': 'https://poe.com',
        'poe-formkey': poe_formkey,
        'poe-tchannel': poe_tchannel,
        'referer': f'https://poe.com/{dict_bot["path"][bot]}',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    data = {
    "query": "mutation chatHelpers_addMessageBreakEdgeMutation_Mutation(\n  $chatId: BigInt!\n) {\n  messageBreakEdgeCreate(chatId: $chatId) {\n    message {\n      cursor\n      node {\n        id\n        messageId\n        text\n        author\n        suggestedReplies\n        creationTime\n        state\n      }\n      id\n    }\n    introductionMessage {\n      cursor\n      node {\n        id\n        messageId\n        text\n        author\n        suggestedReplies\n        creationTime\n        state\n      }\n      id\n    }\n  }\n}\n",
    "variables": {
        "chatId": dict_bot['chatid'][bot],
        "connections": ["client:Q2hhdDo4MTE0MTI5:__ChatMessagesView_chat_messagesConnection_connection"]
    },
    "queryName": "chatHelpers_addMessageBreakEdgeMutation_Mutation"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return "is_final" in response.text
################################################
def use_bot(query,bot,bot_dict,cookie,poe_formkey,poe_tchannel):
    print('running')
    require_time = send_query(query,bot=bot,cookie=cookie,bot_dict=bot_dict,poe_formkey=poe_formkey,poe_tchannel=poe_tchannel)

    chat_list_text,chat_suggest,chat_list_raw,last_time = get_answer(cookie=cookie,bot_path=bot_dict['path'][bot])

    while last_time < require_time or len(chat_list_text[-1]) == 0:
        chat_list_text,chat_suggest,chat_list_raw,last_time = get_answer(cookie=cookie,bot_path=bot_dict['path'][bot])
        time.sleep(1)
    chat_suggest = [suggest for suggest in chat_suggest if len(suggest) > 0 ]
    return chat_list_text[-1],chat_suggest,chat_list_text,chat_list_raw
    
