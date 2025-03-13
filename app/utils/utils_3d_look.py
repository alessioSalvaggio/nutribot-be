import requests
import json
import os

def generate_headers_v2(header_type, ua, parsed_ua, UUID=None):
    base_headers = {
        'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'DNT': '1',
        'User-Agent': ua,
        'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
        'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
        'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"'
    }

    headers_variants = {
        0: {'Accept': '*/*', 'Authorization': os.getenv('LOOK3D_WIDGET_KEY'), 'Content-Type': 'application/json;charset=UTF-8'},
        1: {'Accept': '*/*', 'Authorization': f'UUID {UUID}', 'Content-Type': 'application/json;charset=UTF-8'},
        2: {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'priority': 'u=0, i'},
        3: {'Accept': '*/*', 'Access-Control-Request-Headers': 'authorization,content-type', 'Access-Control-Request-Method': 'POST', 'Origin': 'https://mtm-widget.3dlook.me'},
        4: {'Accept': '*/*', 'Access-Control-Request-Headers': 'authorization', 'Access-Control-Request-Method': 'GET', 'Origin': 'https://mtm-widget.3dlook.me'},
        5: {'Accept': 'application/json, text/plain, */*', 'Authorization': f'UUID {UUID}', 'Content-Type': 'application/json;charset=UTF-8', 'Origin': 'https://mtm-widget.3dlook.me'},
        6: {'Accept': '*/*', 'Authorization': f'UUID {UUID}', 'Origin': 'https://mtm-widget.3dlook.me'},
        7: {'Accept': '*/*', 'Authorization': f'UUID {UUID}', 'Content-Type': 'application/json;charset=UTF-8', 'Origin': 'https://mtm-widget.3dlook.me'},
        8: {'accept': 'image/avif,image/webp,*/*;q=0.8', 'if-modified-since': 'Wed, 19 Jun 2024 09:18:02 GMT', 'priority': 'i', 'referer': f'https://mtm-widget.3dlook.me/?key={UUID}'},
        9: {'Accept': 'application/json, text/plain, */*', 'Authorization': f'UUID {UUID}', 'Content-Type': 'application/json;charset=UTF-8', 'Origin': 'https://mtm-widget.3dlook.me'},
        10: {'accept': 'image/avif,image/webp,*/*;q=0.8', 'if-modified-since': 'Thu, 02 Apr 2020 11:34:59 GMT', 'priority': 'u=1, i', 'referer': f'https://mtm-widget.3dlook.me/?key={UUID}'},
        11: {'Accept': '*/*', 'Authorization': f'UUID {UUID}', 'Content-Type': 'application/json;charset=UTF-8', 'Origin': 'https://mtm-widget.3dlook.me'},
        12: {'Accept': '*/*', 'Access-Control-Request-Headers': 'authorization,content-type', 'Access-Control-Request-Method': 'PATCH', 'Origin': 'https://mtm-widget.3dlook.me'},
        13: {'Accept': '*/*', 'Authorization': f'UUID {UUID}', 'Origin': 'https://mtm-widget.3dlook.me'}
    }

    headers = {**base_headers, **headers_variants.get(header_type, {})}
    return headers

def generate_headers(header_type, ua, parsed_ua, UUID=None):
    if header_type == 0:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Authorization': os.getenv('LOOK3D_WIDGET_KEY'),
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'DNT': '1',
            'Origin': '',
            'Referer': '',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': ua,
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"'
        }
    elif header_type == 1:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Authorization': f'UUID {UUID}',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'DNT': '1',
            'Origin': '',
            'Referer': '',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': ua,
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"'
        }
    elif header_type == 2:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'dnt': '1',
            'priority': 'u=0, i',
            'referer': '',
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-storage-access': 'active',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'User-Agent': ua
        }
    elif header_type == 3:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Access-Control-Request-Headers': 'authorization,content-type',
            'Access-Control-Request-Method': 'POST',
            'Connection': 'keep-alive',
            'Origin': 'https://mtm-widget.3dlook.me',
            'Referer': 'https://mtm-widget.3dlook.me/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': ua
        }
    elif header_type == 4:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Access-Control-Request-Headers': 'authorization',
            'Access-Control-Request-Method': 'GET',
            'Connection': 'keep-alive',
            'Origin': 'https://mtm-widget.3dlook.me',
            'Referer': 'https://mtm-widget.3dlook.me/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': ua
        }
    elif header_type == 5:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Authorization": f"UUID {UUID}",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "DNT": "1",
            "Origin": "https://mtm-widget.3dlook.me",
            "Referer": "https://mtm-widget.3dlook.me/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            'User-Agent': ua,
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"'
        }
    elif header_type == 6:
        headers = {
            "Accept": "*/*",
            "Accept-Language": "it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Authorization": f"UUID {UUID}",
            "Connection": "keep-alive",
            "DNT": "1",
            "Origin": "https://mtm-widget.3dlook.me",
            "Referer": "https://mtm-widget.3dlook.me/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            'User-Agent': ua,
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"'
        }
    elif header_type == 7:
        headers = {
            "Accept": "*/*",
            "Accept-Language": "it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Authorization": f"UUID {UUID}",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "DNT": "1",
            "Origin": "https://mtm-widget.3dlook.me",
            "Referer": "https://mtm-widget.3dlook.me/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            'User-Agent': ua,
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"'
        }
    elif header_type == 8:
        headers = {
            "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "accept-language": "it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "dnt": "1",
            "if-modified-since": "Wed, 19 Jun 2024 09:18:02 GMT",
            "if-none-match": '"8770bb3a9753f970ae9be3076ce7d429"',
            "priority": "i",
            "referer": f"https://mtm-widget.3dlook.me/?key={UUID}",
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"',
            "sec-fetch-dest": "image",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-origin",
            "sec-fetch-storage-access": "active",
            "user-agent": ua
        }
    elif header_type == 9:
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Authorization': f'UUID {UUID}',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'DNT': '1',
            'Origin': 'https://mtm-widget.3dlook.me',
            'Referer': 'https://mtm-widget.3dlook.me/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': ua,
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"'
        }
    elif header_type == 10:
        headers = {
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'dnt': '1',
            'if-modified-since': 'Thu, 02 Apr 2020 11:34:59 GMT',
            'if-none-match': '"5c6d68f07c3c811ac4ad6929441d9263"',
            'priority': 'u=1, i',
            'referer': f'https://mtm-widget.3dlook.me/?key={UUID}',
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-storage-access': 'active',
            'user-agent': ua
        }
    elif header_type == 11:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Authorization': f'UUID {UUID}',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'DNT': '1',
            'Origin': 'https://mtm-widget.3dlook.me',
            'Referer': 'https://mtm-widget.3dlook.me/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': ua,
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"'
        }
    elif header_type == 12:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Access-Control-Request-Headers': 'authorization,content-type',
            'Access-Control-Request-Method': 'PATCH',
            'Connection': 'keep-alive',
            'Origin': 'https://mtm-widget.3dlook.me',
            'Referer': 'https://mtm-widget.3dlook.me/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': ua
        }
    elif header_type == 13:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Authorization': f'UUID {UUID}',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': 'https://mtm-widget.3dlook.me',
            'Referer': 'https://mtm-widget.3dlook.me/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': ua,
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"'
        }
    elif header_type == 14:
        headers = {
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'dnt': '1',
            'if-modified-since': 'Wed, 19 Jun 2024 09:18:02 GMT',
            'if-none-match': '"fa6b528b2b10bd3a642ee86759bc64e5"',
            'priority': 'i',
            'referer': f'https://mtm-widget.3dlook.me/?key={UUID}',
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-storage-access': 'active',
            'user-agent': ua
        }
    elif header_type == 15:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Access-Control-Request-Headers': 'authorization,content-type',
            'Access-Control-Request-Method': 'POST',
            'Connection': 'keep-alive',
            'Origin': 'https://mtm-widget.3dlook.me',
            'Referer': 'https://mtm-widget.3dlook.me/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': ua,
        }
    elif header_type == 16:
        headers = {
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'dnt': '1',
            'if-modified-since': 'Wed, 19 Jun 2024 09:18:02 GMT',
            'if-none-match': '"04898251a93bd3016fbaf46b5cbcff1f"',
            'priority': 'i',
            'referer': f'https://mtm-widget.3dlook.me/?key={UUID}',
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-storage-access': 'active',
            'user-agent': ua
        }
    elif header_type == 17:
        headers = {
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'dnt': '1',
            'if-modified-since': 'Wed, 19 Jun 2024 09:18:02 GMT',
            'if-none-match': '"8882bdbffacf8025557a34c7514f1364"',
            'priority': 'u=1, i',
            'referer': f'https://mtm-widget.3dlook.me/?key={UUID}',
            'sec-ch-ua': f'"{parsed_ua["browser"]["name"]}";v="{parsed_ua["browser"]["version"]}"',
            'sec-ch-ua-mobile': '?0' if parsed_ua['platform']['name'] != 'Android' else '?1',
            'sec-ch-ua-platform': f'"{parsed_ua["platform"]["name"]}"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-storage-access': 'active',
            'user-agent': ua
        }
    return headers

def c1(ua, parsed_ua):
    url = "https://saia.3dlook.me/api/v2/persons/widget/"
    payload_dict = {
        "state": {
            "status": "created",
            "units": "in",
            "height": None,
            "email": None,
            "weight": None,
            "weightLb": None,
            "disabledEmail": False,
            "disableEmailScreen": False
        }
    }
    payload = json.dumps(payload_dict)
    headers = generate_headers(0, ua, parsed_ua)

    response = requests.request("POST", url, headers=headers, data=payload).json()

    return response['uuid']

def c2(UUID, ua, parsed_ua):
    url = "https://saia.3dlook.me/api/v2/measurements/mtm-clients/"
    headers = generate_headers(1, ua, parsed_ua, UUID)
    payload = json.dumps({
    "source": "widget"
    })
    
    response = requests.request("POST", url, headers=headers, data=payload).json()

    return response['id']

def welcome_page(UUID, mtm_client, return_url, ua, parsed_ua):
    url = f"https://mtm-widget.3dlook.me/?key={UUID}"
    headers = generate_headers(2, ua, parsed_ua, UUID)
    response_0 = requests.get(url, headers=headers)
    
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(3, ua, parsed_ua, UUID)
    payload = {}
    response_1 = requests.request("OPTIONS", url, headers=headers, data=payload)
    
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/"
    payload = {}
    headers = generate_headers(4, ua, parsed_ua, UUID)
    response_2 = requests.request("OPTIONS", url, headers=headers, data=payload)
    
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(5, ua, parsed_ua, UUID)
    data = {
        "name": "WELCOME_SCREEN_ENTER",
        "data": {
            "device": "web browser",
            "browser": "edge-chromium"
        }
    }
    response_3 = requests.post(url, headers=headers, json=data)
    
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(5, ua, parsed_ua, UUID)
    data = {
        "name": "WIDGET_OPEN",
        "data": {}
    }
    response_4 = requests.post(url, headers=headers, json=data)

    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/"
    headers = generate_headers(6, ua, parsed_ua, UUID)
    response_5 = requests.get(url, headers=headers)

    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/"
    headers = generate_headers(7, ua, parsed_ua, UUID)
    data = {
        "source": "widget",
        "mtm_client": mtm_client,
        "state": {
            "status": "created",
            "email": None,
            "units": "in",
            "height": None,
            "weight": None,
            "weightLb": None,
            "disabledEmail": False,
            "disableEmailScreen": False,
            "returnUrl": return_url,
            "fakeSize": False,
            "productId": None
        }
    }
    response_6 = requests.patch(url, headers=headers, json=data)
 
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(5, ua, parsed_ua, UUID)
    data = {
        "name": "WELCOME_SCREEN_CLOSE",
        "data": {}
    }
    response_7 = requests.post(url, headers=headers, json=data)

def email_and_full_name(UUID, user_email, user_first_name, ua, parsed_ua):       
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(5, ua, parsed_ua, UUID)
    data = {
        "name": "EMAIL_PAGE_ENTER",
        "data": {}
    }
    response_1 = requests.post(url, headers=headers, json=data)
    
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(5, ua, parsed_ua, UUID)
    data = {
        "name": "CHECK_TERMS_AND_POLICY",
        "data": {"value": True}
    }
    response_2 = requests.post(url, headers=headers, json=data)
    
    url = "https://mtm-widget.3dlook.me/widget-assets/checkbox.96c8cd3065553a22cedf44c2009a182b.svg"
    headers = generate_headers(8, ua, parsed_ua, UUID)
    response_3 = requests.get(url, headers=headers)
    
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(5, ua, parsed_ua, UUID)
    data = {
        "name": "EMAIL_PAGE_ENTER_EMAIL",
        "data": {
            "email": user_email,
            "firstName": user_first_name
        }
    }
    response_4 = requests.post(url, headers=headers, data=json.dumps(data))
    
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(5, ua, parsed_ua, UUID)
    data = {
        "name": "EMAIL_PAGE_LEAVE",
        "data": {}
    }
    response_5 = requests.post(url, headers=headers, data=json.dumps(data))
    
def gender_page(UUID, user_gender_tag, ua, parsed_ua):    
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(5, ua, parsed_ua, UUID)
    data = {
        "name": "GENDER_PAGE_ENTER",
        "data": {}
    }
    response_0 = requests.post(url, headers=headers, data=json.dumps(data))
    
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(5, ua, parsed_ua, UUID)
    data = {
        "name": user_gender_tag,
        "data": {}
    }
    response_1 = requests.post(url, headers=headers, data=json.dumps(data))
    
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(5, ua, parsed_ua, UUID)
    data = {
        "name": "GENDER_PAGE_LEAVE",
        "data": {}
    }
    response_2 = requests.post(url, headers=headers, data=json.dumps(data))
        
def height_weight_page(UUID, user_weight, user_height, ua, parsed_ua):
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(5, ua, parsed_ua, UUID)
    data = {
        "name": "HEIGHT_PAGE_ENTER",
        "data": {}
    }
    response_0 = requests.post(url, headers=headers, data=json.dumps(data))
        
    url = f"https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/"
    headers = generate_headers(5, ua, parsed_ua, UUID)
    data = {
        "name": "HEIGHT_PAGE_METRIC_SELECTED",
        "data": {}
    }
    response_1 = requests.post(url, headers=headers, data=json.dumps(data))
    
    url = f'https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/'
    headers = generate_headers(9, ua, parsed_ua, UUID)
    data = {
        "name": "HEIGHT_PAGE_HEIGHT_SELECTED",
        "data": {
            "height": user_height
        }
    }
    response_2 = requests.post(url, headers=headers, data=json.dumps(data))
    
    url = f'https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/'
    headers = generate_headers(9, ua, parsed_ua, UUID)
    data = {
        "name": "HEIGHT_PAGE_LEAVE",
        "data": {}
    }
    response_3 = requests.post(url, headers=headers, data=json.dumps(data))

    url = f'https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/'
    headers = generate_headers(9, ua, parsed_ua, UUID)
    data = {
        "name": "WEIGHT_PAGE_ENTER",
        "data": {}
    }
    response_4 = requests.post(url, headers=headers, data=json.dumps(data))

    url = f'https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/'
    headers = generate_headers(9, ua, parsed_ua, UUID)
    data = {
        "name": "WEIGHT_PAGE_WEIGHT_SELECTED",
        "data": {
            "value": f"{user_weight}"
        }
    }
    response_5 = requests.post(url, headers=headers, data=json.dumps(data))

    url = f'https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/'
    headers = generate_headers(9, ua, parsed_ua, UUID)
    data = {
        "name": "WEIGHT_PAGE_LEAVE",
        "data": {}
    }
    response_6 = requests.post(url, headers=headers, data=json.dumps(data))
 
def final_page(UUID, user_email, user_first_name, user_gender, user_height, user_weight, return_url, mtm_client, ua, parsed_ua):
    url = 'https://mtm-widget.3dlook.me/widget-assets/flags.5c6d68f07c3c811ac4ad6929441d9263.png'
    headers = generate_headers(10, ua, parsed_ua, UUID)
    response_0 = requests.get(url, headers=headers)
    
    url = f'https://saia.3dlook.me/api/v2/persons/widget/{UUID}/'
    headers = generate_headers(11, ua, parsed_ua, UUID)

    data = {
        "unit": "cm",
        "email": user_email,
        "state": {
            "status": "set metadata",
            "email": user_email,
            "units": "cm",
            "height": user_height,
            "weight": user_weight,
            "weightLb": None,
            "disabledEmail": False,
            "disableEmailScreen": False,
            "returnUrl": return_url,
            "fakeSize": False,
            "productId": None,
            "processStatus": "",
            "gender": user_gender,
            "settings": {
                "final_page": "measurements"
            }
        }
    }
    response_1 = requests.patch(url, headers=headers, data=json.dumps(data))
    
    url = 'https://mtm-widget.3dlook.me/widget-assets/preloader.90a0c3ee9b4c01704adc94c6ec727757.svg'
    headers = generate_headers(17, ua, parsed_ua, UUID)

    response_2 = requests.get(url, headers=headers)
    
    url = 'https://mtm-widget.3dlook.me/widget-assets/phone-for-loader.6f86eda9d632c69c83647124f77eae78.svg'
    headers = generate_headers(16, ua, parsed_ua, UUID)
    response_3 = requests.get(url, headers=headers)

    url = f'https://saia.3dlook.me/api/v2/persons/widget/{UUID}/events/'
    headers = generate_headers(9, ua, parsed_ua, UUID)
    data = {
        "name": "SCAN_QR_CODE_PAGE_ENTER",
        "data": {}
    }
    response_4 = requests.post(url, headers=headers, json=data)
    
    url = 'https://saia.3dlook.me/api/v2/measurements/shorting-link/'
    headers = generate_headers(15, ua, parsed_ua, UUID)
    response_5 = requests.options(url, headers=headers)
    
    url = 'https://mtm-widget.3dlook.me/widget-assets/loader-for-phone.ada88f8169a63ea05099d198e6b55320.svg'
    headers = generate_headers(14, ua, parsed_ua, UUID)
    response_6 = requests.get(url, headers=headers)
    
    url = 'https://saia.3dlook.me/api/v2/measurements/shorting-link/'
    headers = generate_headers(11, ua, parsed_ua, UUID)
    payload = {
        'link': f'https://mtm-widget.3dlook.me/#/mobile/{UUID}'
    }
    response_7 = requests.post(url, json=payload, headers=headers).json()

    url = f'https://saia.3dlook.me/api/v2/measurements/mtm-clients/{mtm_client}/'
    headers = generate_headers(12, ua, parsed_ua, UUID)
    response_8 = requests.options(url, headers=headers)
    
    url = f'https://saia.3dlook.me/api/v2/measurements/mtm-clients/{mtm_client}/'
    headers = generate_headers(11, ua, parsed_ua, UUID)
    data = {
        "first_name": user_first_name
    }
    response_9 = requests.patch(url, headers=headers, data=json.dumps(data))

    url = f'https://saia.3dlook.me/api/v2/persons/widget/{UUID}/'
    headers = generate_headers(11, ua, parsed_ua, UUID)
    data = {
        "state": {
            "status": "set metadata",
            "email": user_email,
            "units": "cm",
            "height": user_height,
            "weight": user_weight,
            "weightLb": None,
            "disabledEmail": False,
            "disableEmailScreen": False,
            "returnUrl": return_url,
            "fakeSize": False,
            "productId": None,
            "processStatus": "",
            "gender": user_gender,
            "settings": {
                "final_page": "measurements"
            },
            "widgetUrl": response_7['short_link']
        }
    }
    response_10 = requests.patch(url, headers=headers, data=json.dumps(data))
    
    url = f'https://saia.3dlook.me/api/v2/persons/widget/{UUID}/'
    headers = generate_headers(13, ua, parsed_ua, UUID)
    response_11 = requests.get(url, headers=headers).json()

    return response_11

def get_mtm_widget_data(UUID: str, ua: str, parsed_ua):
    url = f'https://saia.3dlook.me/api/v2/persons/widget/{UUID}/'
    headers = generate_headers(13, ua, parsed_ua, UUID)
    response = requests.get(url, headers=headers).json()
    return response