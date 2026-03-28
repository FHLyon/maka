from requests import session as s
import re, time,sys,random
from bs4 import BeautifulSoup
from datetime import datetime as dt

import base64
import struct
import datetime
import binascii
import json
import os
import getpass
import requests

#pip install base64,bs4,requests
#apt update && apt upgrade -y
#pkg install clang python libffi openssl libsodium
#pip install pycryptodomex pycryptodome
#SODIUM_INSTALL=system pip install pynacl  

from Cryptodome import Random
from Cryptodome.Cipher import AES
from nacl.public import PublicKey, SealedBox


def Check_Live_Fb(uid):
    url = f"https://graph2.facebook.com/v3.3/{uid}/picture?redirect=0"
    response = requests.get(url, timeout=30)
    check_data = response.json()
    
    if not check_data.get('data', {}).get('height') or not check_data.get('data', {}).get('width'):
        return 'DIE'
    return 'LIVE'


#print(Check_Live_Fb("100089200214741"))
#print(Check_Live_Fb("100010153714683"))
#exit()


def get_keyid_public_key(html_source):

  pattern_flexible = r'EncryptPassword.*?,\s*(\d+)\s*,\s*"([a-fA-F0-9]{64})"'
  pattern_flexible = r'EncryptPassword.*?,\s*(\d+).*?"(.*?)"'

  match = re.search(pattern_flexible, html_source)
  if match:
    key_id = int(match.group(1))
    public_key = match.group(2)
    return key_id, public_key
  else:
    return False

def facebook_web_encrypt_password(html, password):
  try:
    key_id,pub_key=get_keyid_public_key(html)
    version=5
    key = Random.get_random_bytes(32)
    iv = bytes([0] * 12)

    time = int(datetime.datetime.now().timestamp())

    aes = AES.new(key, AES.MODE_GCM, nonce=iv, mac_len=16)
    aes.update(str(time).encode('utf-8'))
    encrypted_password, cipher_tag = aes.encrypt_and_digest(password.encode('utf-8'))

    pub_key_bytes = binascii.unhexlify(pub_key)
    seal_box = SealedBox(PublicKey(pub_key_bytes))
    encrypted_key = seal_box.encrypt(key)

    encrypted = bytes([1,
                       key_id,
                       *list(struct.pack('<h', len(encrypted_key))),
                       *list(encrypted_key),
                       *list(cipher_tag),
                       *list(encrypted_password)])
    encrypted = base64.b64encode(encrypted).decode('utf-8')

    return f'#PWD_BROWSER:{version}:{time}:{encrypted}'
  except:
    print('Error !!')
    return False


cookies = {
    #'datr': 'ktWIaEMcwTVST2IZSCpYfRb_',
    #'sb': 'ktWIaN8ZwSW5vOb90Ew3xup5',
    'm_pixel_ratio': '2.75',
    'wd': '393x786',
    'ps_l': '1',
    'ps_n': '1',
    #'fr': '04gGDrf1sJXLw6ywE..BoiNWS..AAA.0.0.BoiNWU.AWdZG2HFQFodC5DyLGjakGsb3iM',
}

headers = {
    'authority': 'm.facebook.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    # 'cookie': 'datr=ktWIaEMcwTVST2IZSCpYfRb_; sb=ktWIaN8ZwSW5vOb90Ew3xup5; m_pixel_ratio=2.75; wd=393x786; ps_l=1; ps_n=1; fr=04gGDrf1sJXLw6ywE..BoiNWS..AAA.0.0.BoiNWU.AWdZG2HFQFodC5DyLGjakGsb3iM',
    'dpr': '2.75',
    'pragma': 'no-cache',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="24.0.0.0", "Chromium";v="116.0.5845.240"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-model': '"Redmi 5 Plus"',
    'sec-ch-ua-platform': '"Android"',
    'sec-ch-ua-platform-version': '"8.1.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'viewport-width': '980',
}

params = {
    'lid': '0PicWNTo94TBir2hS',
    'bn': 'Y29tLmFuZHJvaWQuY2hyb21l',
}


response = requests.get('https://m.facebook.com/ig/login_via/app/', params=params, cookies=cookies, headers=headers)

cookies=response.cookies.get_dict()

#exit()

open('3.html','w').write(response.text)

print('etape post ...')



# bk.action.array.Make waterfalid
#######


def post_login(USER_ID,password,html,referer,ses):

    headers = {
    'authority': 'm.facebook.com',
    'accept': '*/*',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    # 'cookie': 'datr=tmKGaItA-LaXE7ZpCPZeLwTD; sb=tmKGaKJw6ScEDI8xxMphm4GN; m_pixel_ratio=2.75; wd=393x786; fr=0rIPEeic4Q4HHIgJ8..BohmK2..AAA.0.0.BohmLU.AWeYqbO-b6JWImEOBbfb_UJaBtE',
    'origin': 'https://m.facebook.com',
    'referer': referer,
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="24.0.0.0", "Chromium";v="116.0.5845.240"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-model': '"Redmi 5 Plus"',
    'sec-ch-ua-platform': '"Android"',
    'sec-ch-ua-platform-version': '"8.1.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    }

    params = {
    'appid': 'com.bloks.www.bloks.caa.login.async.send_login_request',
    'type': 'action',
    '__bkv': '7dc3df7a1c2b41c2ef275eac1130af6da64453b8e5de853b8cf45b43c64d127b',# __bkv=re.search(r'"WebBloksVersioningID",\[],{versioningID:"(.*?)"',html).group(1)
    }

    hs=re.search(r'"haste_session":"(.*?)"',html).group(1)
    lsd=re.search(r'"lsd":"(.*?)"',html).group(1)
    fb_dtsg = re.search('"dtsg":{"token":"(.*?)"',html).group(1)
    jazoest = re.search(r'"jazoest", "(.*?)"',html).group(1)
    username_text_input_id = re.search(r'"password", "(.*?)"',html).group(1)
    password_text_input_id = re.search(r'"pass"\s*,.*?"(.*?)"',html).group(1)
    INTERNAL__latency_qpl_instance_id = re.search(r'bk.action.i64.Const.*?,\s*(\d+)',html).group(1)
    waterfall_id = re.search(r'bk.action.i64.Const.*?"(.*?)"',html).group(1)
    rev=re.search(r'{rev:(.*?)}',html).group(1)
    hsi=re.search(r'"hsi":"(.*?)"',html).group(1)

    PASSWORD = facebook_web_encrypt_password(html, password)

    #print(hs,rev,hsi,fb_dtsg,jazoest,lsd,username_text_input_id,password_text_input_id,INTERNAL__latency_qpl_instance_id,waterfall_id,PASSWORD)

    data = {
    '__aaid': '0',
    '__user': '0',
    '__a': '1',
    '__req': '8',
    '__hs': hs,
    'dpr': '3',
    '__ccg': 'GOOD',
    '__rev': rev, 
    '__s': ':o38cid:nn2ilm',
    '__hsi': hsi,
    '__dyn': '0wzpawlE72fDg9ppo5S12wAxu13wqobE6u7E39x60lW4o3Bw4Ewk9E4W099w2s8hw73wGw6tw5Uw64w8W1uwf20n6aw8m0zE2ZwrU6q3a0le0iS2eU2dwde0UE',
    'fb_dtsg': fb_dtsg,
    'jazoest': jazoest,
    'lsd': lsd,
    'params': '{"params":"{\\"server_params\\":{\\"credential_type\\":\\"password\\",\\"username_text_input_id\\":\\"'+username_text_input_id+'\\",\\"password_text_input_id\\":\\"'+password_text_input_id+'\\",\\"login_source\\":\\"Login\\",\\"login_credential_type\\":\\"none\\",\\"server_login_source\\":\\"login\\",\\"ar_event_source\\":\\"login_home_page\\",\\"should_trigger_override_login_success_action\\":0,\\"should_trigger_override_login_2fa_action\\":0,\\"is_caa_perf_enabled\\":0,\\"reg_flow_source\\":\\"login_home_native_integration_point\\",\\"caller\\":\\"gslr\\",\\"is_from_landing_page\\":0,\\"is_from_empty_password\\":0,\\"is_from_aymh\\":0,\\"is_from_password_entry_page\\":0,\\"is_from_assistive_id\\":0,\\"is_from_msplit_fallback\\":0,\\"two_step_login_type\\":\\"one_step_login\\",\\"is_vanilla_password_page_empty_password\\":0,\\"INTERNAL__latency_qpl_marker_id\\":36707139,\\"INTERNAL__latency_qpl_instance_id\\":\\"'+INTERNAL__latency_qpl_instance_id+'\\",\\"device_id\\":null,\\"family_device_id\\":null,\\"waterfall_id\\":\\"'+waterfall_id+'\\",\\"offline_experiment_group\\":null,\\"layered_homepage_experiment_group\\":null,\\"is_platform_login\\":0,\\"is_from_logged_in_switcher\\":0,\\"is_from_logged_out\\":0,\\"access_flow_version\\":\\"pre_mt_behavior\\"},\\"client_input_params\\":{\\"machine_id\\":\\"\\",\\"cloud_trust_token\\":null,\\"block_store_machine_id\\":\\"\\",\\"contact_point\\":\\"'+ USER_ID +'\\",\\"password\\":\\"'+ PASSWORD +'\\",\\"accounts_list\\":[],\\"fb_ig_device_id\\":[],\\"secure_family_device_id\\":\\"\\",\\"encrypted_msisdn\\":\\"\\",\\"headers_infra_flow_id\\":\\"\\",\\"try_num\\":1,\\"login_attempt_count\\":1,\\"event_flow\\":\\"login_manual\\",\\"event_step\\":\\"home_page\\",\\"openid_tokens\\":{},\\"auth_secure_device_id\\":\\"\\",\\"client_known_key_hash\\":\\"\\",\\"has_whatsapp_installed\\":0,\\"sso_token_map_json_string\\":\\"\\",\\"should_show_nested_nta_from_aymh\\":0,\\"password_contains_non_ascii\\":\\"false\\",\\"has_granted_read_contacts_permissions\\":0,\\"has_granted_read_phone_permissions\\":0,\\"app_manager_id\\":\\"\\",\\"aymh_accounts\\":[{\\"id\\":\\"\\",\\"profiles\\":{\\"id\\":{\\"user_id\\":\\"\\",\\"name\\":\\"\\",\\"profile_picture_url\\":\\"\\",\\"small_profile_picture_url\\":null,\\"notification_count\\":0,\\"credential_type\\":\\"none\\",\\"token\\":\\"\\",\\"last_access_time\\":0,\\"is_derived\\":0,\\"username\\":\\"\\",\\"password\\":\\"\\",\\"has_smartlock\\":0,\\"account_center_id\\":\\"\\",\\"account_source\\":\\"\\",\\"credentials\\":[],\\"nta_eligibility_reason\\":null,\\"from_accurate_privacy_result\\":0,\\"dbln_validated\\":0}}}],\\"lois_settings\\":{\\"lois_token\\":\\"\\"}}}"}',
    }


    print(data)
    time.sleep(12)
    response = requests.post('https://m.facebook.com/async/wbloks/fetch/', params=params, cookies=cookies, headers=headers, data=data)
    open('r.html','wb').write(response.content)
    print(response.url)
    cookies2=dict(cookies)
    cookies2.update(response.cookies.get_dict())
    print(cookies2)

    if 'c_user' in cookies2:return True

    headers = {
    'authority': 'm.facebook.com',
    'accept': '*/*',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    # 'cookie': 'datr=tmKGaItA-LaXE7ZpCPZeLwTD; sb=tmKGaKJw6ScEDI8xxMphm4GN; m_pixel_ratio=2.75; wd=393x786; fr=0rIPEeic4Q4HHIgJ8..BohmK2..AAA.0.0.BohmLq.AWeXl1HCv_39wtLpLFRImtCi9vo',
    'origin': 'https://m.facebook.com',
    'referer': response.url,
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="24.0.0.0", "Chromium";v="116.0.5845.240"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-model': '"Redmi 5 Plus"',
    'sec-ch-ua-platform': '"Android"',
    'sec-ch-ua-platform-version': '"8.1.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    }

    params = {
    'appid': 'com.bloks.www.ap.two_step_verification.entrypoint_async',
    'type': 'action',
    '__bkv': '7dc3df7a1c2b41c2ef275eac1130af6da64453b8e5de853b8cf45b43c64d127b',
    }

    html=response.text.replace('\\','')

    matchs=re.search(r'(\s*"INTERNAL__latency_qpl_instance_id").*?\s*(bk.action.array.Make.*?,\s*"(.*?)".*?"(.*?)")',html)


    context_data=matchs.group(3)
    device_id=matchs.group(4)

    INTERNAL__latency_qpl_instance_id = re.search(r'bk.action.i64.Const.*?,\s*(\d+)',html).group(1)

    data = {
    '__aaid': '0',
    '__user': '0',
    '__a': '1',
    '__req': 'o',
    '__hs': hs,
    'dpr': '3',
    '__ccg': 'GOOD',
    '__rev': rev,
    '__s': ':hdtz3n:36ylw7',
    '__hsi': hsi,
    '__dyn': '0wzpawlE72fDg9ppo5S12wAxu13wqobE6u7E39x60lW4o3Bw4Ewk9E4W099w2s8hw73wGw6tw5Uw64w8W1uwf20n6aw8m0zE2ZwrU6q3a0le0iS2eU2dwde0UE',
    'fb_dtsg': fb_dtsg,
    'jazoest': jazoest,
    'lsd': lsd,
    'params': '{"params":"{\\"server_params\\":{\\"context_data\\":\\"'+context_data+'\\",\\"device_id\\":\\"'+device_id+'\\",\\"INTERNAL__latency_qpl_marker_id\\":36707139,\\"INTERNAL__latency_qpl_instance_id\\":\\"'+INTERNAL__latency_qpl_instance_id+'\\"},\\"client_input_params\\":{\\"has_whatsapp_installed\\":0,\\"machine_id\\":\\"\\",\\"auth_secure_device_id\\":\\"\\",\\"accounts_list\\":[]}}"}',
    }

    print(data)

    response = requests.post('https://m.facebook.com/async/wbloks/fetch/', params=params, cookies=cookies2, headers=headers, data=data)

    cookies2.update(response.cookies.get_dict())

    open('r2.html','w').write(response.text)

    headers = {
    'authority': 'm.facebook.com',
    'accept': '*/*',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    # 'cookie': 'datr=DSKJaLThbyX1xMIzktXtZNIo; sb=DSKJaG2GVTQjZ-LOBYceFTeA; ps_l=1; ps_n=1; m_pixel_ratio=2.75; wd=393x786; fr=0OtratjJtmAMUsBOw..BoiSIN..AAA.0.0.BoiltS.AWcVamWNEhpnjJSpLE_HEn9r1ac',
    'origin': 'https://m.facebook.com',
    'pragma': 'no-cache',
    'referer': response.url,
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="24.0.0.0", "Chromium";v="116.0.5845.240"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-model': '"Redmi 5 Plus"',
    'sec-ch-ua-platform': '"Android"',
    'sec-ch-ua-platform-version': '"8.1.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    }

    params = {
    'appid': 'com.bloks.www.ap.two_step_verification.approve_from_another_device',
    'type': 'app',
    '__bkv': '7dc3df7a1c2b41c2ef275eac1130af6da64453b8e5de853b8cf45b43c64d127b',
    }

    html=response.text.replace('\\','')
    matchs = re.search(r'(\s*"INTERNAL_INFRA_screen_id").*?\s*(bk.action.array.Make.*?,\s*"(.*?)".*?"(.*?)")', html)
    context_data=matchs.group(3)
    device_id=matchs.group(4)

    data = {
    '__aaid': '0',
    '__user': '0',
    '__a': '1',
    '__req': 'p',
    '__hs': hs,
    'dpr': '3',
    '__ccg': 'GOOD',
    '__rev': rev,
    '__s': ':hdtz3n:36ylw7',
    '__hsi': hsi,
    '__dyn': '0wzpawlE72fDg9ppo5S12wAxu13wqobE6u7E39x60lW4o3Bw4Ewk9E4W099w2s8hw73wGw6tw5Uw64w8W1uwf20n6aw8m0zE2ZwrU6q3a0le0iS2eU2dwde0UE',
    'fb_dtsg': fb_dtsg,
    'jazoest': jazoest,
    'lsd': lsd,
    'params': '{"params":"{\\"server_params\\":{\\"context_data\\":\\"'+context_data+'\\",\\"device_id\\":\\"'+device_id+'\\",\\"INTERNAL_INFRA_screen_id\\":\\"approve_from_another_device\\"}}"}',
    }
    print(data)

    response = requests.post('https://m.facebook.com/async/wbloks/fetch/', params=params, cookies=cookies, headers=headers, data=data)

    open('r3.html','w').write(response.text)

    cookies2.update(response.cookies.get_dict())

    headers = {
    'authority': 'm.facebook.com',
    'accept': '*/*',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    # 'cookie': 'datr=DSKJaLThbyX1xMIzktXtZNIo; sb=DSKJaG2GVTQjZ-LOBYceFTeA; ps_l=1; ps_n=1; m_pixel_ratio=2.75; wd=393x786; fr=0OtratjJtmAMUsBOw..BoiSIN..AAA.0.0.BoiltU.AWcGDCM1wUXAephq6xcivnKZFV8',
    'origin': 'https://m.facebook.com',
    'pragma': 'no-cache',
    'referer': response.url,
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="24.0.0.0", "Chromium";v="116.0.5845.240"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-model': '"Redmi 5 Plus"',
    'sec-ch-ua-platform': '"Android"',
    'sec-ch-ua-platform-version': '"8.1.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    }

    params = {
    'appid': 'com.bloks.www.two_step_verification.afad_state.async',
    'type': 'action',
    '__bkv': '7dc3df7a1c2b41c2ef275eac1130af6da64453b8e5de853b8cf45b43c64d127b',
    }

    html=response.text.replace('\\','')

    for i in range(15):

      two_step_verification_context = re.search(r'(\s*"block_store_machine_id").*?\s*(bk.action.array.Make.*?,\s*"(.*?)".*?"(.*?)")',html).group(3)

      machine_id = re.search(r'(\s*"block_store_machine_id").*?\s*(bk.action.array.Make.*?,\s*"(.*?)".*?"(.*?)".*?"(.*?)")', html).group(5)

      INTERNAL__latency_qpl_instance_id = re.search(r'bk.action.i64.Const.*?,\s*(\d+)',html).group(1)

      device_id = re.search(r'(\s*"INTERNAL_INFRA_screen_id").*?\s*(bk.action.array.Make.*?,\s*"(.*?)".*?"(.*?)")',html).group(4)

      data = {
    '__aaid': '0',
    '__user': '0',
    '__a': '1',
    '__req': 'q',
    '__hs': hs,
    'dpr': '3',
    '__ccg': 'GOOD',
    '__rev': rev,
    '__s': ':hdtz3n:36ylw7',
    '__hsi': hsi,
    '__dyn': '0wzpawlE72fDg9ppo5S12wAxu13wqobE6u7E39x60lW4o3Bw4Ewk9E4W099w2s8hw73wGw6tw5Uw64w8W1uwf20n6aw8m0zE2ZwrU6q3a0le0iS2eU2dwde0UE',
    'fb_dtsg': fb_dtsg,
    'jazoest': jazoest,
    'lsd': lsd,
    'params': '{"params":"{\\"server_params\\":{\\"two_step_verification_context\\":\\"'+two_step_verification_context+'\\",\\"flow_source\\":\\"login_challenges\\",\\"machine_id\\":\\"'+machine_id+'\\",\\"device_id\\":\\"'+device_id+'\\",\\"INTERNAL__latency_qpl_marker_id\\":36707139,\\"INTERNAL__latency_qpl_instance_id\\":\\"'+INTERNAL__latency_qpl_instance_id+'\\",\\"cloud_trust_token\\":null,\\"block_store_machine_id\\":null}}"}',
    }
      print(data)
      time.sleep(5)
      response = requests.post('https://m.facebook.com/async/wbloks/fetch/', params=params, cookies=cookies, headers=headers, data=data)
      print(response.text)
      print(response.cookies.get_dict())
      open('r4.html','w').write(response.text)
      input(' continue ?? >> ')


USER_ID  = ['mikmak.mik.73','maurice.fortunah'][1]
password = ['lataka','VUDUvudu667'][1]
html     = response.text.replace('\\','')
referer  = response.url
ses=s()
post_login(USER_ID,password,html,referer,ses)


