import os #line:2
import traceback #line:3
import sys #line:4
import requests #line:5
import time #line:6
import json #line:7
import base64 #line:8
from framework import app #line:10
from framework .logger import get_logger #line:11
from framework .util import Util #line:12
logger =get_logger ('tving_api')#line:13
session =requests .session ()#line:15
headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7','Referer':'',}#line:23
config ={'token':None ,'param':"&free=all&lastFrequency=y&order=broadDate",'program_param':'&free=all&order=frequencyDesc&programCode=%s','default_param':'&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610'}#line:30
def do_login (O00000000OO0OO000 ,OO0O0O0OOO0OO0000 ,O00000OO0O0OO00O0 ):#line:33
    try :#line:34
        OOOO0OO000O00OO0O ='https://user.tving.com/user/doLogin.tving'#line:35
        if O00000OO0O0OO00O0 =='0':#line:36
            OO0O00O00OOO00O0O ='10'#line:37
        else :#line:38
            OO0O00O00OOO00O0O ='20'#line:39
        OO00OO000O0OO0O0O ={'userId':O00000000OO0OO000 ,'password':OO0O0O0OOO0OO0000 ,'loginType':OO0O00O00OOO00O0O }#line:44
        O0OO0000O00O00OOO =session .post (OOOO0OO000O00OO0O ,data =OO00OO000O0OO0O0O )#line:45
        OOO00OO0000O0000O =O0OO0000O00O00OOO .headers ['Set-Cookie']#line:46
        for O00OO0000O0OOOOO0 in OOO00OO0000O0000O .split (','):#line:47
            O00OO0000O0OOOOO0 =O00OO0000O0OOOOO0 .strip ()#line:48
            if O00OO0000O0OOOOO0 .startswith ('_tving_token'):#line:49
                O0O000OO0OOOOOOO0 =O00OO0000O0OOOOO0 .split (';')[0 ]#line:50
                return O0O000OO0OOOOOOO0 #line:51
    except Exception as OO0OO00OOO00O0O0O :#line:52
        logger .error ('Exception:%s',OO0OO00OOO00O0O0O )#line:53
        logger .error (traceback .format_exc ())#line:54
def get_vod_list (p =None ,page =1 ):#line:57
    try :#line:58
        O00O0O00000OOO0OO ='http://api.tving.com/v1/media/episodes?pageNo=%s&pageSize=18&adult=all&guest=all&scope=all&personal=N'%page #line:59
        if p is not None :#line:60
            O00O0O00000OOO0OO +=p #line:61
        else :#line:62
            O00O0O00000OOO0OO +=config ['param']#line:63
        O00O0O00000OOO0OO +=config ['default_param']#line:64
        O0O00OO00OOO0O00O =requests .get (O00O0O00000OOO0OO )#line:65
        return O0O00OO00OOO0O00O .json ()#line:67
    except Exception as OO0OOOOOO000O00O0 :#line:68
        logger .error ('Exception:%s',OO0OOOOOO000O00O0 )#line:69
        logger .error (traceback .format_exc ())#line:70
def get_episode_json_default (O0OOOO00OOO000O00 ,OOOO00O00O00000OO ,OO00OO00000OOOOOO ,proxy =None ):#line:73
    OO0O0OOOOOO0O00OO ='%d'%time .time ()#line:75
    if OO00OO00000OOOOOO is None :#line:76
        OO00OO00000OOOOOO =config ['token']#line:77
    try :#line:78
        if OOOO00O00O00000OO =='stream70':#line:79
            O0O00O0OOOO0OO000 =config ['default_param'].replace ('CSSD0100','CSSD1200')#line:80
            OO0O0O0000OO000OO ='http://api.tving.com/v2/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(O0O00O0OOOO0OO000 ,OO0O0OOOOOO0O00OO ,O0OOOO00OOO000O00 ,OOOO00O00O00000OO )#line:81
        else :#line:82
            OO0O0O0000OO000OO ='http://api.tving.com/v2/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(config ['default_param'],OO0O0OOOOOO0O00OO ,O0OOOO00OOO000O00 ,OOOO00O00O00000OO )#line:83
        O00OOOO0000000OO0 =None #line:85
        if proxy is not None :#line:86
            O00OOOO0000000OO0 ={"https":proxy ,'http':proxy }#line:87
        headers ['Cookie']=OO00OO00000OOOOOO #line:88
        O0O0O0O000OOO00OO =session .get (OO0O0O0000OO000OO ,headers =headers ,proxies =O00OOOO0000000OO0 )#line:89
        OO000O000OOOOO000 =O0O0O0O000OOO00OO .json ()#line:90
        OO0O0O0000OO000OO =OO000O000OOOOO000 ['body']['stream']['broadcast']['broad_url']#line:94
        logger .debug (OO0O0O0000OO000OO )#line:95
        OOOO0000OOOOOOOO0 =decrypt (O0OOOO00OOO000O00 ,OO0O0OOOOOO0O00OO ,OO0O0O0000OO000OO )#line:96
        logger .debug (OOOO0000OOOOOOOO0 )#line:97
        if OOOO0000OOOOOOOO0 .find ('m3u8')==-1 :#line:98
            OOOO0000OOOOOOOO0 =OOOO0000OOOOOOOO0 .replace ('rtmp','http')#line:99
            OOOO0000OOOOOOOO0 =OOOO0000OOOOOOOO0 .replace ('?','/playlist.m3u8?')#line:100
        if OOOO0000OOOOOOOO0 .find ('smil/playlist.m3u8')!=-1 and OOOO0000OOOOOOOO0 .find ('content_type=VOD')!=-1 :#line:102
            O00OO0O000OOOOOOO =OOOO0000OOOOOOOO0 .split ('playlist.m3u8')#line:103
            O0O0O0O000OOO00OO =session .get (OOOO0000OOOOOOOO0 ,headers =headers ,proxies =O00OOOO0000000OO0 )#line:104
            OOOO0O0O00000O000 =O0O0O0O000OOO00OO .text .split ('\n')#line:105
            OO00OO000O00OO0OO =-1 #line:106
            O0000O0O0OOO0O0O0 =''#line:107
            while len (O0000O0O0OOO0O0O0 )==0 :#line:108
                O0000O0O0OOO0O0O0 =OOOO0O0O00000O000 [OO00OO000O00OO0OO ].strip ()#line:109
                OO00OO000O00OO0OO -=1 #line:110
            OOOO0000OOOOOOOO0 ='%s%s'%(O00OO0O000OOOOOOO [0 ],O0000O0O0OOO0O0O0 )#line:111
        return OO000O000OOOOO000 ,OOOO0000OOOOOOOO0 #line:112
    except Exception as O0OOOOOOO00000O00 :#line:113
        logger .error ('Exception:%s',O0OOOOOOO00000O00 )#line:114
        logger .error (traceback .format_exc ())#line:115
def get_episode_json_default_live (O000OOOO00O0O000O ,OO0O0OO0O0OO0OO0O ,O0O00OOO00O000O0O ,proxy =None ,inc_quality =True ):#line:119
    OOOOO0000O00OOOOO ='%d'%time .time ()#line:121
    if O0O00OOO00O000O0O is None :#line:122
        O0O00OOO00O000O0O =config ['token']#line:123
    try :#line:124
        if inc_quality :#line:125
            OOO0OO0000OOOO0O0 ='http://api.tving.com/v2/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(config ['default_param'],OOOOO0000O00OOOOO ,O000OOOO00O0O000O ,OO0O0OO0O0OO0OO0O )#line:126
        else :#line:127
            OOO0OO0000OOOO0O0 ='http://api.tving.com/v2/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&callingFrom=FLASH'%(config ['default_param'],OOOOO0000O00OOOOO ,O000OOOO00O0O000O )#line:128
        OO0O0O0000O0O000O =None #line:130
        if proxy is not None :#line:131
            OO0O0O0000O0O000O ={"https":proxy ,'http':proxy }#line:132
        headers ['Cookie']=O0O00OOO00O000O0O #line:133
        OOOOOO000O0O0OOO0 =session .get (OOO0OO0000OOOO0O0 ,headers =headers ,proxies =OO0O0O0000O0O000O )#line:134
        OOO00OOOOO0O0O00O =OOOOOO000O0O0OOO0 .json ()#line:135
        OOO0OO0000OOOO0O0 =OOO00OOOOO0O0O00O ['body']['stream']['broadcast']['broad_url']#line:139
        O0OO000O0O0OO0O0O =decrypt (O000OOOO00O0O000O ,OOOOO0000O00OOOOO ,OOO0OO0000OOOO0O0 )#line:141
        if O0OO000O0O0OO0O0O .find ('.mp4')!=-1 and O0OO000O0O0OO0O0O .find ('/VOD/')!=-1 :#line:145
            return OOO00OOOOO0O0O00O ,O0OO000O0O0OO0O0O #line:146
        if O0OO000O0O0OO0O0O .find ('Policy=')==-1 :#line:147
            OOO00OOOOO0O0O00O ,OO00000OOO00O00O0 =get_episode_json_default_live (O000OOOO00O0O000O ,OO0O0OO0O0OO0OO0O ,O0O00OOO00O000O0O ,proxy =proxy ,inc_quality =False )#line:148
            if OO0O0OO0O0OO0OO0O =='stream50'and OO00000OOO00O00O0 .find ('live2000.smil'):#line:149
                OO00000OOO00O00O0 =OO00000OOO00O00O0 .replace ('live2000.smil','live5000.smil')#line:150
                return OOO00OOOOO0O0O00O ,OO00000OOO00O00O0 #line:151
        return OOO00OOOOO0O0O00O ,O0OO000O0O0OO0O0O #line:153
    except Exception as O000OO0O00O0O00O0 :#line:154
        logger .error ('Exception:%s',O000OO0O00O0O00O0 )#line:155
        logger .error (traceback .format_exc ())#line:156
"""
def get_episode_json_proxy(episode_code, quality, proxy_url, token):
    ts = '%d' % time.time()
    if token is None:
        token = config['token']
    try:
        #https://www.tving.com/streaming/info?networkCode=CSND0900&apiKey=1e7952d0917d6aab1f0293a063697610&ooc=composed%3Dfalse%5ECAPTURING_PHASE%3D1%5Ecancelable%3Dfalse%5EreturnValue%3Dtrue%5EcancelBubble%3Dfalse%5Ebubbles%3Dfalse%5EdefaultPrevented%3Dfalse%5ENONE%3D0%5EAT_TARGET%3D2%5EBUBBLING_PHASE%3D3%5EtimeStamp%3D2158.7350000045262%5EisTrusted%3Dfalse%5Etype%3DoocCreate%5EeventPhase%3D0%5E&screenCode=CSSD0100&callingFrom=HTML5&deviceId=2357832822&osCode=CSOD0900&teleCode=CSCD0900&info=Y&adReq=none&streamCode=stream50&mediaCode=E002837703
        if quality == 'stream70':
            tmp_param = config['default_param'].replace('CSSD0100', 'CSSD1200')
            url = 'http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH' % (tmp_param, ts, episode_code, quality)
        else:
            url = 'http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH' % (config['default_param'], ts, episode_code, quality)

        data = {'url' : url, 'cookie' : token}
        res = session.post(proxy_url, data=data)
        data = res.json()
        url = data['body']['stream']['broadcast']['broad_url']
        decrypted_url = decrypt(episode_code, ts, url)
        if decrypted_url.find('m3u8') == -1:
            decrypted_url = decrypted_url.replace('rtmp', 'http')
            decrypted_url = decrypted_url.replace('?', '/playlist.m3u8?')
        return data, decrypted_url
    except Exception as exception:
        logger.error('Exception:%s', exception)
        logger.error(traceback.format_exc())

"""#line:185
def get_episode_json (OO00OO0OO00O00OOO ,OO00O0000OOOO0O00 ,O0O00O0OOO00OOO00 ,proxy =None ,is_live =False ):#line:187
    try :#line:188
        """
        use_proxy = False
        try:
            from tving import ModelSetting
            use_proxy = ModelSetting.get_bool('use_proxy')
            if use_proxy:
                proxy_url = ModelSetting.get('proxy_url')
        except:
            logger.debug('Not Import Tving plugin!!')
        if use_proxy:
            ret =  get_episode_json_proxy(episode_code, quality, proxy_url, token=token)
        else:
            ret = get_episode_json_default(episode_code, quality, token=token)
        return ret
        """#line:203
        if is_live :#line:204
            return get_episode_json_default_live (OO00OO0OO00O00OOO ,OO00O0000OOOO0O00 ,token =O0O00O0OOO00OOO00 ,proxy =proxy )#line:205
        else :#line:206
            return get_episode_json_default (OO00OO0OO00O00OOO ,OO00O0000OOOO0O00 ,token =O0O00O0OOO00OOO00 ,proxy =proxy )#line:207
    except Exception as OO0O0OOO000000000 :#line:208
        logger .error ('Exception:%s',OO0O0OOO000000000 )#line:209
        logger .error (traceback .format_exc ())#line:210
def decrypt (O0OOOOOO0OO00OOOO ,OOOO000OOO00O00O0 ,OO000O000O0O000OO ):#line:214
    try :#line:215
        from Crypto .Cipher import DES3 #line:216
        O0OOO00O0OO0OOOOO =base64 .decodestring (OO000O000O0O000OO .encode ())#line:217
        O0O0OOOO00OO00O0O ='cjhv*tving**good/%s/%s'%(O0OOOOOO0OO00OOOO [-3 :],OOOO000OOO00O00O0 )#line:218
        OOOO000OOO00O00O0 =O0O0OOOO00OO00O0O [:24 ]#line:219
        O0OOOOOOOO0000000 =DES3 .new (OOOO000OOO00O00O0 ,DES3 .MODE_ECB )#line:220
        OO0000O000OOO0O0O =O0OOOOOOOO0000000 .decrypt (O0OOO00O0OO0OOOOO )#line:221
        if app .config ['config']['is_py2']:#line:222
            O0000O00OO00OOOOO =ord (OO0000O000OOO0O0O [-1 ])#line:223
        else :#line:224
            O0000O00OO00OOOOO =OO0000O000OOO0O0O [-1 ]#line:225
        OO0000O000OOO0O0O =OO0000O000OOO0O0O [:-O0000O00OO00OOOOO ]#line:226
        return OO0000O000OOO0O0O .decode ()#line:227
    except Exception as OOOOOOOO00O000O00 :#line:228
        logger .error ('Exception:%s',OOOOOOOO00O000O00 )#line:229
        logger .error (traceback .format_exc ())#line:230
def get_filename (O0O0OO00OO000O000 ):#line:232
    try :#line:233
        O00O0O000OO0000OO =O0O0OO00OO000O000 ["body"]["content"]["program_name"]#line:234
        O00O0O000OO0000OO =O00O0O000OO0000OO .replace ("<","").replace (">","").replace ("\\","").replace ("/","").replace (":","").replace ("*","").replace ("\"","").replace ("|","").replace ("?","").replace ("  "," ").strip ()#line:235
        OO0OOO0O0OO000O0O =O0O0OO00OO000O000 ["body"]["content"]["frequency"]#line:236
        OO00O00O0O00OO0O0 =str (O0O0OO00OO000O000 ["body"]["content"]["info"]["episode"]["broadcast_date"])[2 :]#line:237
        O0O0O0000OO0OOOO0 =None #line:239
        if O0O0OO00OO000O000 ["body"]["stream"]["quality"]is None :#line:240
            O0O0O0000OO0OOOO0 ="stream40"#line:241
        else :#line:242
            O0OOO0OOO0OOO0000 =len (O0O0OO00OO000O000 ["body"]["stream"]["quality"])#line:243
            for O0O0OO000OOOOO00O in range (O0OOO0OOO0OOO0000 ):#line:244
                if O0O0OO00OO000O000 ["body"]["stream"]["quality"][O0O0OO000OOOOO00O ]["selected"]=="Y":#line:245
                    O0O0O0000OO0OOOO0 =O0O0OO00OO000O000 ["body"]["stream"]["quality"][O0O0OO000OOOOO00O ]["code"]#line:246
                    break #line:247
        if O0O0O0000OO0OOOO0 is None :#line:248
            return #line:249
        OO0O00O0O00OO0O00 =get_quality_to_res (O0O0O0000OO0OOOO0 )#line:250
        O0O0000OO0O000000 =str (OO0OOO0O0OO000O0O )#line:251
        if OO0OOO0O0OO000O0O <10 :#line:252
            O0O0000OO0O000000 ='0'+O0O0000OO0O000000 #line:253
        OOO00OO00O000O000 ='%s.E%s.%s.%s-ST.mp4'%(O00O0O000OO0000OO ,O0O0000OO0O000000 ,OO00O00O0O00OO0O0 ,OO0O00O0O00OO0O00 )#line:255
        return OOO00OO00O000O000 #line:256
    except Exception as O0O0O00OOOO00000O :#line:257
        logger .error ('Exception:%s',O0O0O00OOOO00000O )#line:258
        logger .error (traceback .format_exc ())#line:259
def get_quality_to_tving (OOOO00O00OO00OOO0 ):#line:262
    if OOOO00O00OO00OOO0 =='FHD':#line:263
        return 'stream50'#line:264
    elif OOOO00O00OO00OOO0 =='HD':#line:265
        return 'stream40'#line:266
    elif OOOO00O00OO00OOO0 =='SD':#line:267
        return 'stream30'#line:268
    elif OOOO00O00OO00OOO0 =='UHD':#line:269
        return 'stream70'#line:270
    return 'stream50'#line:271
def get_quality_to_res (OO00000OOO000OOOO ):#line:274
    if OO00000OOO000OOOO =='stream50':#line:275
        return '1080p'#line:276
    elif OO00000OOO000OOOO =='stream40':#line:277
        return '720p'#line:278
    elif OO00000OOO000OOOO =='stream30':#line:279
        return '480p'#line:280
    elif OO00000OOO000OOOO =='stream70':#line:281
        return '2160p'#line:282
    elif OO00000OOO000OOOO =='stream25':#line:283
        return '270p'#line:284
    return '1080p'#line:285
def get_live_list (list_type =0 ,order ='rating'):#line:289
    if list_type ==0 or list_type =='0':#line:290
        O0OO0OO0OOO00O000 =['&channelType=CPCS0100']#line:291
    elif list_type ==1 or list_type =='1':#line:292
        O0OO0OO0OOO00O000 =['&channelType=CPCS0300']#line:293
    else :#line:294
        O0OO0OO0OOO00O000 =['&channelType=CPCS0100','&channelType=CPCS0300']#line:295
    OOOO0OO0OOOO0OO00 =[]#line:296
    for OOO000OO0OOOO0O0O in O0OO0OO0OOO00O000 :#line:297
        O0O0O000OOOO00O0O =1 #line:298
        while True :#line:299
            O0O00OOOOOO00O000 ,O0O0OO00OO00OOO00 =get_live_list2 (OOO000OO0OOOO0O0O ,O0O0O000OOOO00O0O ,order =order )#line:300
            for O0O00O0OOO00O0O00 in O0O0OO00OO00OOO00 :#line:301
                OOOO0OO0OOOO0OO00 .append (O0O00O0OOO00O0O00 )#line:302
            if O0O00OOOOOO00O000 =='N':#line:303
                break #line:304
            O0O0O000OOOO00O0O +=1 #line:305
    return OOOO0OO0OOOO0OO00 #line:306
def get_live_list2 (O0OOOO0OOOO0OOO0O ,OOO0O0OO00O0OO000 ,order ='rating'):#line:309
    O00O0OO0O0000O0O0 ='N'#line:310
    try :#line:311
        O0O000O00000O0O0O =[]#line:312
        OO0O00O0O000OO0O0 ='http://api.tving.com/v1/media/lives?pageNo=%s&pageSize=20&order=%s&adult=all&free=all&guest=all&scope=all'%(OOO0O0OO00O0OO000 ,order )#line:313
        if O0OOOO0OOOO0OOO0O is not None :#line:314
            OO0O00O0O000OO0O0 +=O0OOOO0OOOO0OOO0O #line:315
        OO0O00O0O000OO0O0 +=config ['default_param']#line:316
        OO0OO00OOO0OOO0O0 =requests .get (OO0O00O0O000OO0O0 )#line:317
        OOOOOO0O0OOOOO000 =OO0OO00OOO0OOO0O0 .json ()#line:318
        for OOOO0OO0OO00OO00O in OOOOOO0O0OOOOO000 ["body"]["result"]:#line:319
            try :#line:320
                if OOOO0OO0OO00OO00O ["live_code"]in ['C07381','C05661','C44441','C04601','C07382']:#line:322
                    continue #line:323
                OO0O00O0OOO0000OO ={}#line:324
                if True :#line:326
                    OO0O00O0OOO0000OO ['id']=OOOO0OO0OO00OO00O ["live_code"]#line:327
                    OO0O00O0OOO0000OO ['title']=OOOO0OO0OO00OO00O ['schedule']['channel']['name']['ko']#line:328
                    OO0O00O0OOO0000OO ['episode_title']=' '#line:329
                    OO0O00O0OOO0000OO ['img']='http://image.tving.com/upload/cms/caic/CAIC1900/%s.png'%OOOO0OO0OO00OO00O ["live_code"]#line:330
                    if OOOO0OO0OO00OO00O ['schedule']['episode']is not None :#line:331
                        OO0O00O0OOO0000OO ['episode_title']=OOOO0OO0OO00OO00O ['schedule']['episode']['name']['ko']#line:332
                        if OO0O00O0OOO0000OO ['title'].startswith ('CH.')and len (OOOO0OO0OO00OO00O ['schedule']['episode']['image'])>0 :#line:333
                            OO0O00O0OOO0000OO ['img']='http://image.tving.com'+OOOO0OO0OO00OO00O ['schedule']['episode']['image'][0 ]['url']#line:334
                    OO0O00O0OOO0000OO ['free']=(OOOO0OO0OO00OO00O ['schedule']['broadcast_url'][0 ]['broad_url1'].find ('drm')==-1 )#line:335
                    OO0O00O0OOO0000OO ['summary']=OO0O00O0OOO0000OO ['episode_title']#line:336
                O0O000O00000O0O0O .append (OO0O00O0OOO0000OO )#line:337
            except Exception as O00O000OOO0OO0OO0 :#line:338
                logger .error ('Exception:%s',O00O000OOO0OO0OO0 )#line:339
                logger .error (traceback .format_exc ())#line:340
        O00O0OO0O0000O0O0 =OOOOOO0O0OOOOO000 ["body"]["has_more"]#line:341
    except Exception as O00O000OOO0OO0OO0 :#line:342
        logger .error ('Exception:%s',O00O000OOO0OO0OO0 )#line:343
        logger .error (traceback .format_exc ())#line:344
    return O00O0OO0O0000O0O0 ,O0O000O00000O0O0O #line:345
def get_movie_json (OOO0000OO0000O0O0 ,O000O0O0OOOOO00O0 ,O0O0OOO0O0OOO00O0 ,proxy =None ):#line:348
    O0OO0OOOO0O0O0O00 ='%d'%time .time ()#line:349
    if O0O0OOO0O0OOO00O0 is None :#line:350
        O0O0OOO0O0OOO00O0 =config ['token']#line:351
    try :#line:352
        O0O0OO0OO0OO0O0OO ='stream70'#line:353
        if O0O0OO0OO0OO0O0OO =='stream70':#line:354
            O0O0O0O0OOO0O00OO =config ['default_param'].replace ('CSSD0100','CSSD1200')#line:355
            OOOO0OOOOO0OO0OO0 ='http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(O0O0O0O0OOO0O00OO ,O0OO0OOOO0O0O0O00 ,OOO0000OO0000O0O0 ,O0O0OO0OO0OO0O0OO )#line:356
        else :#line:357
            OOOO0OOOOO0OO0OO0 ='http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(config ['default_param'],O0OO0OOOO0O0O0O00 ,OOO0000OO0000O0O0 ,O0O0OO0OO0OO0O0OO )#line:358
        OOOO0OOOOO0OO0OO0 +='&deviceId=%s'%O000O0O0OOOOO00O0 #line:360
        O0O0OOO0O000O0O0O =None #line:361
        if proxy is not None :#line:362
            O0O0OOO0O000O0O0O ={"https":proxy ,'http':proxy }#line:363
        headers ['Cookie']=O0O0OOO0O0OOO00O0 #line:364
        OO000O0O0OO000000 =session .get (OOOO0OOOOO0OO0OO0 ,headers =headers ,proxies =O0O0OOO0O000O0O0O )#line:365
        OO00OOO0O0O0OOOOO =OO000O0O0OO000000 .json ()#line:366
        logger .debug (OO00OOO0O0O0OOOOO )#line:368
        OO00OOO0O0O0OOOOO ['ret']={}#line:370
        if OO00OOO0O0O0OOOOO ['body']['result']['code']=="000":#line:371
            if '4k_nondrm_url'in OO00OOO0O0O0OOOOO ['body']['stream']['broadcast']:#line:372
                O00000OOOOO000OO0 =decrypt (OOO0000OO0000O0O0 ,O0OO0OOOO0O0O0O00 ,OO00OOO0O0O0OOOOO ['body']['stream']['broadcast']['4k_nondrm_url'])#line:373
                if O00000OOOOO000OO0 .find ('5000k_PC.mp4')!=-1 :#line:375
                    OO00OOO0O0O0OOOOO ['ret']['ret']='ok'#line:376
                    OO00OOO0O0O0OOOOO ['ret']['decrypted_url']=O00000OOOOO000OO0 #line:377
                    OO00OOO0O0O0OOOOO ['ret']['filename']=Util .change_text_for_use_filename ('%s.%s.%s.2160p-ST.mp4'%(OO00OOO0O0O0OOOOO ['body']['content']['info']['movie']['name']['ko'],str (OO00OOO0O0O0OOOOO ['body']['content']['info']['movie']['release_date'])[:4 ],OO00OOO0O0O0OOOOO ['body']['content']['info']['movie']['name']['en']))#line:378
                else :#line:379
                    OO00OOO0O0O0OOOOO ['ret']['ret']='no_4k'#line:380
                    OO00OOO0O0O0OOOOO ['ret']['decrypted_url']=O00000OOOOO000OO0 #line:381
        else :#line:382
            OO00OOO0O0O0OOOOO ['ret']['ret']='need_pay'#line:383
        return OO00OOO0O0O0OOOOO #line:385
    except Exception as O0OO0O00OOO000O0O :#line:386
        logger .error ('Exception:%s',O0OO0O00OOO000O0O )#line:387
        logger .error (traceback .format_exc ())#line:388
def get_prefer_url (O0O0O000OO0O0OO0O ):#line:391
    try :#line:392
        O00O00000OO00OO0O =session .get (O0O0O000OO0O0OO0O ,headers =config ['headers'])#line:393
        OO0O000000O00000O =O00O00000OO00OO0O .text .strip ()#line:394
        OO0OO00O00OO0O00O =None #line:395
        for OOOOO00O00OO00O00 in reversed (OO0O000000O00000O .split ('\n')):#line:396
            if OOOOO00O00OO00O00 .strip ().find ('chunklist.m3u8')!=-1 :#line:397
                OO0OO00O00OO0O00O =OOOOO00O00OO00O00 #line:398
                break #line:399
        if OO0OO00O00OO0O00O is not None and OO0OO00O00OO0O00O !='':#line:400
            OO0OO00O00OO0O00O =O0O0O000OO0O0OO0O .split ('chunklist')[0 ]+OO0OO00O00OO0O00O #line:401
            return OO0OO00O00OO0O00O #line:402
    except Exception as O0OO000O0O0OO000O :#line:403
        logger .error ('Exception:%s',O0OO000O0O0OO000O )#line:404
        logger .error (traceback .format_exc ())#line:405
    return O0O0O000OO0O0OO0O #line:406
def get_vod_list2 (param =None ,page =1 ,genre ='all'):#line:425
    try :#line:426
        O0000O00000000000 ='https://api.tving.com/v2/media/episodes?pageNo=%s&pageSize=24&order=new&adult=all&free=all&guest=all&scope=all&lastFrequency=y&personal=N'%(page )#line:427
        if genre !='all':#line:428
            O0000O00000000000 +='&categoryCode=%s'%genre #line:429
        if param is not None :#line:430
            O0000O00000000000 +=param #line:431
        O0000O00000000000 +=config ['default_param']#line:432
        OO0000O0O00000OOO =requests .get (O0000O00000000000 )#line:434
        return OO0000O0O00000OOO .json ()#line:436
    except Exception as OO000O0O0OO0O0OO0 :#line:437
        logger .error ('Exception:%s',OO000O0O0OO0O0OO0 )#line:438
        logger .error (traceback .format_exc ())#line:439
def get_program_programid (O0OOO0O00OO0O0O0O ):#line:443
    try :#line:444
        O0OOO0O0O00OO0O0O ='https://api.tving.com/v2/media/program/%s?pageNo=1&pageSize=10&order=name'%O0OOO0O00OO0O0O0O #line:445
        O0OOO0O0O00OO0O0O +=config ['default_param']#line:446
        OOO0000OO00OOOO00 =requests .get (O0OOO0O0O00OO0O0O )#line:447
        return OOO0000OO00OOOO00 .json ()#line:449
    except Exception as O00000000000OOO0O :#line:450
        logger .error ('Exception:%s',O00000000000OOO0O )#line:451
        logger .error (traceback .format_exc ())#line:452
def get_frequency_programid (O000O0000OO0O00OO ,page =1 ):#line:457
    try :#line:458
        O00OOOOO00O00OO0O ='https://api.tving.com/v2/media/frequency/program/%s?pageNo=%s&pageSize=10&order=new&free=all&adult=all&scope=all'%(O000O0000OO0O00OO ,page )#line:459
        O00OOOOO00O00OO0O +=config ['default_param']#line:460
        O00OO00000000OO00 =requests .get (O00OOOOO00O00OO0O )#line:461
        return O00OO00000000OO00 .json ()#line:463
    except Exception as O00O0OO00OO000O0O :#line:464
        logger .error ('Exception:%s',O00O0OO00OO000O0O )#line:465
        logger .error (traceback .format_exc ())#line:466
def get_movies (page =1 ,category ='all'):#line:477
    try :#line:478
        OO0OO0O0OOOOOO000 ='https://api.tving.com/v2/media/movies?pageNo=%s&pageSize=24&order=viewDay&free=all&adult=all&guest=all&scope=all&productPackageCode=338723&personal=N&diversityYn=N'%(page )#line:479
        if category !='all':#line:480
            OO0OO0O0OOOOOO000 +='&multiCategoryCode=%s'%category #line:481
        OO0OO0O0OOOOOO000 +=config ['default_param']#line:482
        OOOO00000O0OOO000 =requests .get (OO0OO0O0OOOOOO000 )#line:483
        return OOOO00000O0OOO000 .json ()#line:494
    except Exception as O0OOOO00O000O00OO :#line:495
        logger .error ('Exception:%s',O0OOOO00O000O00OO )#line:496
        logger .error (traceback .format_exc ())#line:497
"""
https://api.tving.com/v2/media/movies?pageNo=1&pageSize=24&order=viewDay&free=all&adult=all&guest=all&scope=all&personal=N&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610&_=1603081489117&drm_yn=N

https://api.tving.com/v2/media/movies?callback=jQuery112307642887056924332_1603081489114&pageNo=1&pageSize=24&order=viewDay&free=all&adult=all&guest=all&scope=all&productPackageCode=1513561%2C338723&personal=N&diversityYn=N&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610&_=1603081489120


https://api.tving.com/v2/media/movies?callback=jQuery112307642887056924332_1603081489114&pageNo=1&pageSize=24&order=viewDay&free=all&adult=all&guest=all&scope=all&productPackageCode=338723&multiCategoryCode=MG100%2CMG190%2CMG230%2CMG270%2CMG290&personal=N&diversityYn=N&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610&_=1603081489122

https://api.tving.com/v2/media/movies?callback=jQuery112307642887056924332_1603081489114&pageNo=1&pageSize=24&order=new&free=all&adult=all&guest=all&scope=all&productPackageCode=338723&personal=N&diversityYn=N&screenCode=CSSD0100&networkCode=CSND0900&osCode=CSOD0900&teleCode=CSCD0900&apiKey=1e7952d0917d6aab1f0293a063697610&_=1603081489123

&multiCategoryCode=MG100%2CMG190%2CMG230%2CMG270%2CMG290  %2C = ,

"""#line:511
def get_movie_json2 (OOOO00O00O0OOOOO0 ,O0000OOOOO00O000O ,OO0OOO00O00OOOOOO ,proxy =None ,quality ='stream50'):#line:513
    O0O0OOO0O0O00O000 ='%d'%time .time ()#line:514
    if OO0OOO00O00OOOOOO is None :#line:515
        OO0OOO00O00OOOOOO =config ['token']#line:516
    try :#line:517
        O0000OO0000000000 ='http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(config ['default_param'],O0O0OOO0O0O00O000 ,OOOO00O00O0OOOOO0 ,quality )#line:518
        O0000OO0000000000 +='&deviceId=%s'%O0000OOOOO00O000O #line:519
        O0O0OO0O0OO00OO0O =None #line:520
        if proxy is not None :#line:521
            O0O0OO0O0OO00OO0O ={"https":proxy ,'http':proxy }#line:522
        headers ['Cookie']=OO0OOO00O00OOOOOO #line:523
        O0OO0OOOO0OOO0O00 =session .get (O0000OO0000000000 ,headers =headers ,proxies =O0O0OO0O0OO00OO0O )#line:524
        OO00O0O0O0OO00O0O =O0OO0OOOO0OOO0O00 .json ()#line:525
        if 'broad_url'in OO00O0O0O0OO00O0O ['body']['stream']['broadcast']:#line:530
            OO00O0O0O0OO00O0O ['body']['decrypted_url']=decrypt (OOOO00O00O0OOOOO0 ,O0O0OOO0O0O00O000 ,OO00O0O0O0OO00O0O ['body']['stream']['broadcast']['broad_url'])#line:532
        return OO00O0O0O0OO00O0O #line:535
    except Exception as O00O0O00O0O0OOOOO :#line:536
        logger .error ('Exception:%s',O00O0O00O0O0OOOOO )#line:537
        logger .error (traceback .format_exc ())#line:538
def get_schedules (OO0O00O00O0000O0O ,O0OOOO0OO0OOO0O00 ,OO00O000O0000O000 ,OO000OO0O0O0OO00O ):#line:541
    try :#line:543
        OOO0O000OO00O0O00 ='https://api.tving.com/v2/media/schedules?pageNo=1&pageSize=20&order=chno&scope=all&adult=n&free=all&broadDate=%s&broadcastDate=%s&startBroadTime=%s&endBroadTime=%s&channelCode=%s'%(O0OOOO0OO0OOO0O00 ,O0OOOO0OO0OOO0O00 ,OO00O000O0000O000 ,OO000OO0O0O0OO00O ,','.join (OO0O00O00O0000O0O ))#line:545
        OOO0O000OO00O0O00 +=config ['default_param']#line:546
        O00OO0000OOO00000 =requests .get (OOO0O000OO00O0O00 )#line:547
        return O00OO0000OOO00000 .json ()#line:549
    except Exception as O00OOOOOOO000OO00 :#line:550
        logger .error ('Exception:%s',O00OOOOOOO000OO00 )#line:551
        logger .error (traceback .format_exc ())#line:552
