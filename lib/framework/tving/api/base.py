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
def do_login (OO0OOOO0OOO0O00O0 ,OO00O0OO0O00OO0OO ,OOO00OO0O00000OOO ):#line:33
    try :#line:34
        OOO00O0O000O00O0O ='https://user.tving.com/user/doLogin.tving'#line:35
        if OOO00OO0O00000OOO =='0':#line:36
            OO0OOO000O000000O ='10'#line:37
        else :#line:38
            OO0OOO000O000000O ='20'#line:39
        O00O00O00OO000OO0 ={'userId':OO0OOOO0OOO0O00O0 ,'password':OO00O0OO0O00OO0OO ,'loginType':OO0OOO000O000000O }#line:44
        O0O00000OO0O00OOO =session .post (OOO00O0O000O00O0O ,data =O00O00O00OO000OO0 )#line:45
        OO000000OO00O00O0 =O0O00000OO0O00OOO .headers ['Set-Cookie']#line:46
        for OOO00O00OOOOO0000 in OO000000OO00O00O0 .split (','):#line:47
            OOO00O00OOOOO0000 =OOO00O00OOOOO0000 .strip ()#line:48
            if OOO00O00OOOOO0000 .startswith ('_tving_token'):#line:49
                O000O00OOOOOOOO00 =OOO00O00OOOOO0000 .split (';')[0 ]#line:50
                return O000O00OOOOOOOO00 #line:51
    except Exception as OOOOOOO0O0OOOOO00 :#line:52
        logger .error ('Exception:%s',OOOOOOO0O0OOOOO00 )#line:53
        logger .error (traceback .format_exc ())#line:54
def get_vod_list (p =None ,page =1 ):#line:57
    try :#line:58
        O00O000OO0OOO000O ='http://api.tving.com/v1/media/episodes?pageNo=%s&pageSize=18&adult=all&guest=all&scope=all&personal=N'%page #line:59
        if p is not None :#line:60
            O00O000OO0OOO000O +=p #line:61
        else :#line:62
            O00O000OO0OOO000O +=config ['param']#line:63
        O00O000OO0OOO000O +=config ['default_param']#line:64
        O00OO0000000000O0 =requests .get (O00O000OO0OOO000O )#line:65
        return O00OO0000000000O0 .json ()#line:67
    except Exception as OO00000O0O0OOO0O0 :#line:68
        logger .error ('Exception:%s',OO00000O0O0OOO0O0 )#line:69
        logger .error (traceback .format_exc ())#line:70
def get_episode_json_default (OOO00O0OO0O00O0OO ,OOOO000000OOO0OOO ,OOOO0OO0O0O0O0000 ,proxy =None ):#line:73
    OOO00O0O00OOO0OOO ='%d'%time .time ()#line:75
    if OOOO0OO0O0O0O0000 is None :#line:76
        OOOO0OO0O0O0O0000 =config ['token']#line:77
    try :#line:78
        if OOOO000000OOO0OOO =='stream70':#line:79
            OO0OOO0000OOO0000 =config ['default_param'].replace ('CSSD0100','CSSD1200')#line:80
            O000O00000O000OO0 ='http://api.tving.com/v2/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(OO0OOO0000OOO0000 ,OOO00O0O00OOO0OOO ,OOO00O0OO0O00O0OO ,OOOO000000OOO0OOO )#line:81
        else :#line:82
            O000O00000O000OO0 ='http://api.tving.com/v2/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(config ['default_param'],OOO00O0O00OOO0OOO ,OOO00O0OO0O00O0OO ,OOOO000000OOO0OOO )#line:83
        OO0O0000OOOOO0OO0 =None #line:85
        if proxy is not None :#line:86
            OO0O0000OOOOO0OO0 ={"https":proxy ,'http':proxy }#line:87
        headers ['Cookie']=OOOO0OO0O0O0O0000 #line:88
        OOO000OOOOOOOOO00 =session .get (O000O00000O000OO0 ,headers =headers ,proxies =OO0O0000OOOOO0OO0 )#line:89
        OO0OO0000OO000OOO =OOO000OOOOOOOOO00 .json ()#line:90
        O000O00000O000OO0 =OO0OO0000OO000OOO ['body']['stream']['broadcast']['broad_url']#line:94
        logger .debug (O000O00000O000OO0 )#line:95
        O000O0OO0000OO00O =decrypt (OOO00O0OO0O00O0OO ,OOO00O0O00OOO0OOO ,O000O00000O000OO0 )#line:96
        logger .debug (O000O0OO0000OO00O )#line:97
        if O000O0OO0000OO00O .find ('m3u8')==-1 :#line:98
            O000O0OO0000OO00O =O000O0OO0000OO00O .replace ('rtmp','http')#line:99
            O000O0OO0000OO00O =O000O0OO0000OO00O .replace ('?','/playlist.m3u8?')#line:100
        if O000O0OO0000OO00O .find ('smil/playlist.m3u8')!=-1 and O000O0OO0000OO00O .find ('content_type=VOD')!=-1 :#line:102
            O00OO0OO0O0O00O0O =O000O0OO0000OO00O .split ('playlist.m3u8')#line:103
            OOO000OOOOOOOOO00 =session .get (O000O0OO0000OO00O ,headers =headers ,proxies =OO0O0000OOOOO0OO0 )#line:104
            OOOO00OO0000OOOOO =OOO000OOOOOOOOO00 .text .split ('\n')#line:105
            OOO0OO00O0OOOO0OO =-1 #line:106
            OO00000OO00O0OO00 =''#line:107
            while len (OO00000OO00O0OO00 )==0 :#line:108
                OO00000OO00O0OO00 =OOOO00OO0000OOOOO [OOO0OO00O0OOOO0OO ].strip ()#line:109
                OOO0OO00O0OOOO0OO -=1 #line:110
            O000O0OO0000OO00O ='%s%s'%(O00OO0OO0O0O00O0O [0 ],OO00000OO00O0OO00 )#line:111
        return OO0OO0000OO000OOO ,O000O0OO0000OO00O #line:112
    except Exception as OO00OOOO0OOOOOO00 :#line:113
        logger .error ('Exception:%s',OO00OOOO0OOOOOO00 )#line:114
        logger .error (traceback .format_exc ())#line:115
def get_episode_json_default_live (O000OO0000OOO000O ,OOO00OOOOOOOOOO00 ,O0O000OO00OOOOO00 ,proxy =None ,inc_quality =True ):#line:119
    OO00OOOOO0OOOOO0O ='%d'%time .time ()#line:121
    if O0O000OO00OOOOO00 is None :#line:122
        O0O000OO00OOOOO00 =config ['token']#line:123
    try :#line:124
        if inc_quality :#line:125
            OOO00O0OO0O0O000O ='http://api.tving.com/v2/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(config ['default_param'],OO00OOOOO0OOOOO0O ,O000OO0000OOO000O ,OOO00OOOOOOOOOO00 )#line:126
        else :#line:127
            OOO00O0OO0O0O000O ='http://api.tving.com/v2/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&callingFrom=FLASH'%(config ['default_param'],OO00OOOOO0OOOOO0O ,O000OO0000OOO000O )#line:128
        OO000OO0OOO00000O =None #line:130
        if proxy is not None :#line:131
            OO000OO0OOO00000O ={"https":proxy ,'http':proxy }#line:132
        headers ['Cookie']=O0O000OO00OOOOO00 #line:133
        OO00000O0O0O0O000 =session .get (OOO00O0OO0O0O000O ,headers =headers ,proxies =OO000OO0OOO00000O )#line:134
        O0000OOOOO0OOOO0O =OO00000O0O0O0O000 .json ()#line:135
        OOO00O0OO0O0O000O =O0000OOOOO0OOOO0O ['body']['stream']['broadcast']['broad_url']#line:139
        O00OOO0OOO0000O0O =decrypt (O000OO0000OOO000O ,OO00OOOOO0OOOOO0O ,OOO00O0OO0O0O000O )#line:141
        if O00OOO0OOO0000O0O .find ('.mp4')!=-1 and O00OOO0OOO0000O0O .find ('/VOD/')!=-1 :#line:145
            return O0000OOOOO0OOOO0O ,O00OOO0OOO0000O0O #line:146
        if O00OOO0OOO0000O0O .find ('Policy=')==-1 :#line:147
            O0000OOOOO0OOOO0O ,O0OO0OO0O0OOO00O0 =get_episode_json_default_live (O000OO0000OOO000O ,OOO00OOOOOOOOOO00 ,O0O000OO00OOOOO00 ,proxy =proxy ,inc_quality =False )#line:148
            if OOO00OOOOOOOOOO00 =='stream50'and O0OO0OO0O0OOO00O0 .find ('live2000.smil'):#line:149
                O0OO0OO0O0OOO00O0 =O0OO0OO0O0OOO00O0 .replace ('live2000.smil','live5000.smil')#line:150
                return O0000OOOOO0OOOO0O ,O0OO0OO0O0OOO00O0 #line:151
        return O0000OOOOO0OOOO0O ,O00OOO0OOO0000O0O #line:153
    except Exception as O00O00O0OOOO0OOOO :#line:154
        logger .error ('Exception:%s',O00O00O0OOOO0OOOO )#line:155
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
def get_episode_json (O00OO0000O000OOO0 ,O00O00O00O0O00OOO ,O0OO0OOOOO0O00000 ,proxy =None ,is_live =False ):#line:187
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
            return get_episode_json_default_live (O00OO0000O000OOO0 ,O00O00O00O0O00OOO ,O0OO0OOOOO0O00000 ,proxy =proxy )#line:205
        else :#line:206
            return get_episode_json_default (O00OO0000O000OOO0 ,O00O00O00O0O00OOO ,O0OO0OOOOO0O00000 ,proxy =proxy )#line:207
    except Exception as O000O0000OOOOOO0O :#line:208
        logger .error ('Exception:%s',O000O0000OOOOOO0O )#line:209
        logger .error (traceback .format_exc ())#line:210
def decrypt (OOOOOO0OOO0O0OO0O ,OOOO000000O00OO0O ,OO0O0OO00000OO0OO ):#line:214
    try :#line:215
        from Crypto .Cipher import DES3 #line:216
        O00OO0000O00OOOOO =base64 .decodestring (OO0O0OO00000OO0OO .encode ())#line:217
        O00OO0O00OO0OO000 ='cjhv*tving**good/%s/%s'%(OOOOOO0OOO0O0OO0O [-3 :],OOOO000000O00OO0O )#line:218
        OOOO000000O00OO0O =O00OO0O00OO0OO000 [:24 ]#line:219
        O0000000O0O00O0OO =DES3 .new (OOOO000000O00OO0O ,DES3 .MODE_ECB )#line:220
        O00O00000OO0OO000 =O0000000O0O00O0OO .decrypt (O00OO0000O00OOOOO )#line:221
        if app .config ['config']['is_py2']:#line:222
            O0OOO00OO00OOO000 =ord (O00O00000OO0OO000 [-1 ])#line:223
        else :#line:224
            O0OOO00OO00OOO000 =O00O00000OO0OO000 [-1 ]#line:225
        O00O00000OO0OO000 =O00O00000OO0OO000 [:-O0OOO00OO00OOO000 ]#line:226
        return O00O00000OO0OO000 .decode ()#line:227
    except Exception as OOO00O0OO00OO0OO0 :#line:228
        logger .error ('Exception:%s',OOO00O0OO00OO0OO0 )#line:229
        logger .error (traceback .format_exc ())#line:230
def get_filename (OO0O0O00O00OOOOOO ):#line:232
    try :#line:233
        OOO0O0OO0O000OO0O =OO0O0O00O00OOOOOO ["body"]["content"]["program_name"]#line:234
        OOO0O0OO0O000OO0O =OOO0O0OO0O000OO0O .replace ("<","").replace (">","").replace ("\\","").replace ("/","").replace (":","").replace ("*","").replace ("\"","").replace ("|","").replace ("?","").replace ("  "," ").strip ()#line:235
        O0O00000O0OO00000 =OO0O0O00O00OOOOOO ["body"]["content"]["frequency"]#line:236
        OO0000OO0OO0OO00O =str (OO0O0O00O00OOOOOO ["body"]["content"]["info"]["episode"]["broadcast_date"])[2 :]#line:237
        OO0O0OOOO000O0OOO =None #line:239
        if OO0O0O00O00OOOOOO ["body"]["stream"]["quality"]is None :#line:240
            OO0O0OOOO000O0OOO ="stream40"#line:241
        else :#line:242
            O0OOO0OOO0O0000OO =len (OO0O0O00O00OOOOOO ["body"]["stream"]["quality"])#line:243
            for OOOOOOOOO0OO00O0O in range (O0OOO0OOO0O0000OO ):#line:244
                if OO0O0O00O00OOOOOO ["body"]["stream"]["quality"][OOOOOOOOO0OO00O0O ]["selected"]=="Y":#line:245
                    OO0O0OOOO000O0OOO =OO0O0O00O00OOOOOO ["body"]["stream"]["quality"][OOOOOOOOO0OO00O0O ]["code"]#line:246
                    break #line:247
        if OO0O0OOOO000O0OOO is None :#line:248
            return #line:249
        OO000O00O0O000O00 =get_quality_to_res (OO0O0OOOO000O0OOO )#line:250
        OO00OO000OO00O0OO =str (O0O00000O0OO00000 )#line:251
        if O0O00000O0OO00000 <10 :#line:252
            OO00OO000OO00O0OO ='0'+OO00OO000OO00O0OO #line:253
        O0000O000OOOOO0OO ='%s.E%s.%s.%s-ST.mp4'%(OOO0O0OO0O000OO0O ,OO00OO000OO00O0OO ,OO0000OO0OO0OO00O ,OO000O00O0O000O00 )#line:255
        return O0000O000OOOOO0OO #line:256
    except Exception as OOO0OOOOOO00000O0 :#line:257
        logger .error ('Exception:%s',OOO0OOOOOO00000O0 )#line:258
        logger .error (traceback .format_exc ())#line:259
def get_quality_to_tving (OO0OO00OOOO0O0OO0 ):#line:262
    if OO0OO00OOOO0O0OO0 =='FHD':#line:263
        return 'stream50'#line:264
    elif OO0OO00OOOO0O0OO0 =='HD':#line:265
        return 'stream40'#line:266
    elif OO0OO00OOOO0O0OO0 =='SD':#line:267
        return 'stream30'#line:268
    elif OO0OO00OOOO0O0OO0 =='UHD':#line:269
        return 'stream70'#line:270
    return 'stream50'#line:271
def get_quality_to_res (O0OOO0000000O0OO0 ):#line:274
    if O0OOO0000000O0OO0 =='stream50':#line:275
        return '1080p'#line:276
    elif O0OOO0000000O0OO0 =='stream40':#line:277
        return '720p'#line:278
    elif O0OOO0000000O0OO0 =='stream30':#line:279
        return '480p'#line:280
    elif O0OOO0000000O0OO0 =='stream70':#line:281
        return '2160p'#line:282
    elif O0OOO0000000O0OO0 =='stream25':#line:283
        return '270p'#line:284
    return '1080p'#line:285
def get_live_list (list_type =0 ,order ='rating'):#line:289
    if list_type ==0 or list_type =='0':#line:290
        OO0OO0OOO00OOOO0O =['&channelType=CPCS0100']#line:291
    elif list_type ==1 or list_type =='1':#line:292
        OO0OO0OOO00OOOO0O =['&channelType=CPCS0300']#line:293
    else :#line:294
        OO0OO0OOO00OOOO0O =['&channelType=CPCS0100','&channelType=CPCS0300']#line:295
    O0O0OOOOOOO00O0O0 =[]#line:296
    for O0O0OO00OO00O0000 in OO0OO0OOO00OOOO0O :#line:297
        OO00OOO000OO000OO =1 #line:298
        while True :#line:299
            O000O0000OO0O0O0O ,OOO0OOO00OO0O000O =get_live_list2 (O0O0OO00OO00O0000 ,OO00OOO000OO000OO ,order =order )#line:300
            for O0OO0OOOO00O000OO in OOO0OOO00OO0O000O :#line:301
                O0O0OOOOOOO00O0O0 .append (O0OO0OOOO00O000OO )#line:302
            if O000O0000OO0O0O0O =='N':#line:303
                break #line:304
            OO00OOO000OO000OO +=1 #line:305
    return O0O0OOOOOOO00O0O0 #line:306
def get_live_list2 (O0O000OOOOOOOOO0O ,O00OOO00OOOO0OOOO ,order ='rating'):#line:309
    O00O00O000O00OO00 ='N'#line:310
    try :#line:311
        OO0000O000O0O0OO0 =[]#line:312
        O0O00OO0O00OO0OO0 ='http://api.tving.com/v1/media/lives?pageNo=%s&pageSize=20&order=%s&adult=all&free=all&guest=all&scope=all'%(O00OOO00OOOO0OOOO ,order )#line:313
        if O0O000OOOOOOOOO0O is not None :#line:314
            O0O00OO0O00OO0OO0 +=O0O000OOOOOOOOO0O #line:315
        O0O00OO0O00OO0OO0 +=config ['default_param']#line:316
        O00OO0OO0OOOO0000 =requests .get (O0O00OO0O00OO0OO0 )#line:317
        O0OO00O0OO0O0O000 =O00OO0OO0OOOO0000 .json ()#line:318
        for O0O00O0OOO0000OOO in O0OO00O0OO0O0O000 ["body"]["result"]:#line:319
            try :#line:320
                if O0O00O0OOO0000OOO ["live_code"]in ['C07381','C05661','C44441','C04601','C07382']:#line:322
                    continue #line:323
                OO0O0OO0OO0OOOOO0 ={}#line:324
                if True :#line:326
                    OO0O0OO0OO0OOOOO0 ['id']=O0O00O0OOO0000OOO ["live_code"]#line:327
                    OO0O0OO0OO0OOOOO0 ['title']=O0O00O0OOO0000OOO ['schedule']['channel']['name']['ko']#line:328
                    OO0O0OO0OO0OOOOO0 ['episode_title']=' '#line:329
                    OO0O0OO0OO0OOOOO0 ['img']='http://image.tving.com/upload/cms/caic/CAIC1900/%s.png'%O0O00O0OOO0000OOO ["live_code"]#line:330
                    if O0O00O0OOO0000OOO ['schedule']['episode']is not None :#line:331
                        OO0O0OO0OO0OOOOO0 ['episode_title']=O0O00O0OOO0000OOO ['schedule']['episode']['name']['ko']#line:332
                        if OO0O0OO0OO0OOOOO0 ['title'].startswith ('CH.')and len (O0O00O0OOO0000OOO ['schedule']['episode']['image'])>0 :#line:333
                            OO0O0OO0OO0OOOOO0 ['img']='http://image.tving.com'+O0O00O0OOO0000OOO ['schedule']['episode']['image'][0 ]['url']#line:334
                    OO0O0OO0OO0OOOOO0 ['free']=(O0O00O0OOO0000OOO ['schedule']['broadcast_url'][0 ]['broad_url1'].find ('drm')==-1 )#line:335
                    OO0O0OO0OO0OOOOO0 ['summary']=OO0O0OO0OO0OOOOO0 ['episode_title']#line:336
                OO0000O000O0O0OO0 .append (OO0O0OO0OO0OOOOO0 )#line:337
            except Exception as OO0OO000OO0O0OOOO :#line:338
                logger .error ('Exception:%s',OO0OO000OO0O0OOOO )#line:339
                logger .error (traceback .format_exc ())#line:340
        O00O00O000O00OO00 =O0OO00O0OO0O0O000 ["body"]["has_more"]#line:341
    except Exception as OO0OO000OO0O0OOOO :#line:342
        logger .error ('Exception:%s',OO0OO000OO0O0OOOO )#line:343
        logger .error (traceback .format_exc ())#line:344
    return O00O00O000O00OO00 ,OO0000O000O0O0OO0 #line:345
def get_movie_json (OOO00O00O0OOO0OO0 ,O00O000OOO00O000O ,O00O0OO00OOO00O00 ,proxy =None ):#line:348
    O00OOOO00O00O0OO0 ='%d'%time .time ()#line:349
    if O00O0OO00OOO00O00 is None :#line:350
        O00O0OO00OOO00O00 =config ['token']#line:351
    try :#line:352
        O00OO0O00O000OOOO ='stream70'#line:353
        if O00OO0O00O000OOOO =='stream70':#line:354
            OOOOO0O0O0O000OO0 =config ['default_param'].replace ('CSSD0100','CSSD1200')#line:355
            O0OO00O000000OO00 ='http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(OOOOO0O0O0O000OO0 ,O00OOOO00O00O0OO0 ,OOO00O00O0OOO0OO0 ,O00OO0O00O000OOOO )#line:356
        else :#line:357
            O0OO00O000000OO00 ='http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(config ['default_param'],O00OOOO00O00O0OO0 ,OOO00O00O0OOO0OO0 ,O00OO0O00O000OOOO )#line:358
        O0OO00O000000OO00 +='&deviceId=%s'%O00O000OOO00O000O #line:360
        OOOOOO0OO00O0OOOO =None #line:361
        if proxy is not None :#line:362
            OOOOOO0OO00O0OOOO ={"https":proxy ,'http':proxy }#line:363
        headers ['Cookie']=O00O0OO00OOO00O00 #line:364
        O00OOO00OOO000O00 =session .get (O0OO00O000000OO00 ,headers =headers ,proxies =OOOOOO0OO00O0OOOO )#line:365
        OO00OO0OOOOOO00OO =O00OOO00OOO000O00 .json ()#line:366
        logger .debug (OO00OO0OOOOOO00OO )#line:368
        OO00OO0OOOOOO00OO ['ret']={}#line:370
        if OO00OO0OOOOOO00OO ['body']['result']['code']=="000":#line:371
            if '4k_nondrm_url'in OO00OO0OOOOOO00OO ['body']['stream']['broadcast']:#line:372
                O000OOOO0O000O00O =decrypt (OOO00O00O0OOO0OO0 ,O00OOOO00O00O0OO0 ,OO00OO0OOOOOO00OO ['body']['stream']['broadcast']['4k_nondrm_url'])#line:373
                if O000OOOO0O000O00O .find ('5000k_PC.mp4')!=-1 :#line:375
                    OO00OO0OOOOOO00OO ['ret']['ret']='ok'#line:376
                    OO00OO0OOOOOO00OO ['ret']['decrypted_url']=O000OOOO0O000O00O #line:377
                    OO00OO0OOOOOO00OO ['ret']['filename']=Util .change_text_for_use_filename ('%s.%s.%s.2160p-ST.mp4'%(OO00OO0OOOOOO00OO ['body']['content']['info']['movie']['name']['ko'],str (OO00OO0OOOOOO00OO ['body']['content']['info']['movie']['release_date'])[:4 ],OO00OO0OOOOOO00OO ['body']['content']['info']['movie']['name']['en']))#line:378
                else :#line:379
                    OO00OO0OOOOOO00OO ['ret']['ret']='no_4k'#line:380
                    OO00OO0OOOOOO00OO ['ret']['decrypted_url']=O000OOOO0O000O00O #line:381
        else :#line:382
            OO00OO0OOOOOO00OO ['ret']['ret']='need_pay'#line:383
        return OO00OO0OOOOOO00OO #line:385
    except Exception as OO0O0O0OOOO000000 :#line:386
        logger .error ('Exception:%s',OO0O0O0OOOO000000 )#line:387
        logger .error (traceback .format_exc ())#line:388
def get_prefer_url (O0O000O000O00O0O0 ):#line:391
    try :#line:392
        O0000OO0O0O0OOO00 =session .get (O0O000O000O00O0O0 ,headers =config ['headers'])#line:393
        OO00OO0000OO00O0O =O0000OO0O0O0OOO00 .text .strip ()#line:394
        O0O0O0O000OO00OOO =None #line:395
        for OOOO0000OO0000O0O in reversed (OO00OO0000OO00O0O .split ('\n')):#line:396
            if OOOO0000OO0000O0O .strip ().find ('chunklist.m3u8')!=-1 :#line:397
                O0O0O0O000OO00OOO =OOOO0000OO0000O0O #line:398
                break #line:399
        if O0O0O0O000OO00OOO is not None and O0O0O0O000OO00OOO !='':#line:400
            O0O0O0O000OO00OOO =O0O000O000O00O0O0 .split ('chunklist')[0 ]+O0O0O0O000OO00OOO #line:401
            return O0O0O0O000OO00OOO #line:402
    except Exception as O0O0O00OOOOO0OOOO :#line:403
        logger .error ('Exception:%s',O0O0O00OOOOO0OOOO )#line:404
        logger .error (traceback .format_exc ())#line:405
    return O0O000O000O00O0O0 #line:406
def get_vod_list2 (param =None ,page =1 ,genre ='all'):#line:425
    try :#line:426
        OO0000O0OOO0OOOO0 ='https://api.tving.com/v2/media/episodes?pageNo=%s&pageSize=24&order=new&adult=all&free=all&guest=all&scope=all&lastFrequency=y&personal=N'%(page )#line:427
        if genre !='all':#line:428
            OO0000O0OOO0OOOO0 +='&categoryCode=%s'%genre #line:429
        if param is not None :#line:430
            OO0000O0OOO0OOOO0 +=param #line:431
        OO0000O0OOO0OOOO0 +=config ['default_param']#line:432
        OO000O00OOOO00000 =requests .get (OO0000O0OOO0OOOO0 )#line:434
        return OO000O00OOOO00000 .json ()#line:436
    except Exception as O00OO0O00O0OOOO0O :#line:437
        logger .error ('Exception:%s',O00OO0O00O0OOOO0O )#line:438
        logger .error (traceback .format_exc ())#line:439
def get_program_programid (O000O0O0OOO0O0000 ):#line:443
    try :#line:444
        O0OO0OOOO0OOOO000 ='https://api.tving.com/v2/media/program/%s?pageNo=1&pageSize=10&order=name'%O000O0O0OOO0O0000 #line:445
        O0OO0OOOO0OOOO000 +=config ['default_param']#line:446
        OOOO00OOO0OO0O0OO =requests .get (O0OO0OOOO0OOOO000 )#line:447
        return OOOO00OOO0OO0O0OO .json ()#line:449
    except Exception as O00OOOOOOOO000OOO :#line:450
        logger .error ('Exception:%s',O00OOOOOOOO000OOO )#line:451
        logger .error (traceback .format_exc ())#line:452
def get_frequency_programid (O0O0O0OO0OO00OOO0 ,page =1 ):#line:457
    try :#line:458
        OOOO000O000O0O0O0 ='https://api.tving.com/v2/media/frequency/program/%s?pageNo=%s&pageSize=10&order=new&free=all&adult=all&scope=all'%(O0O0O0OO0OO00OOO0 ,page )#line:459
        OOOO000O000O0O0O0 +=config ['default_param']#line:460
        O0O00O0OO0000OO0O =requests .get (OOOO000O000O0O0O0 )#line:461
        return O0O00O0OO0000OO0O .json ()#line:463
    except Exception as OOOO00O0OOO0O0000 :#line:464
        logger .error ('Exception:%s',OOOO00O0OOO0O0000 )#line:465
        logger .error (traceback .format_exc ())#line:466
def get_movies (page =1 ,category ='all'):#line:477
    try :#line:478
        O00OO000OOOOOO0OO ='https://api.tving.com/v2/media/movies?pageNo=%s&pageSize=24&order=viewDay&free=all&adult=all&guest=all&scope=all&productPackageCode=338723&personal=N&diversityYn=N'%(page )#line:479
        if category !='all':#line:480
            O00OO000OOOOOO0OO +='&multiCategoryCode=%s'%category #line:481
        O00OO000OOOOOO0OO +=config ['default_param']#line:482
        OOO00O0000O000000 =requests .get (O00OO000OOOOOO0OO )#line:483
        return OOO00O0000O000000 .json ()#line:494
    except Exception as O000O0OOOOOOO0O0O :#line:495
        logger .error ('Exception:%s',O000O0OOOOOOO0O0O )#line:496
        logger .error (traceback .format_exc ())#line:497

def get_movie_json2 (O000000OOOOOOO0OO ,OO000O00O0O0O0000 ,O0OO0O00O000O0OO0 ,proxy =None ,quality ='stream50'):#line:513
    O00OOO000OO0OOO00 ='%d'%time .time ()#line:514
    if O0OO0O00O000O0OO0 is None :#line:515
        O0OO0O00O000O0OO0 =config ['token']#line:516
    try :#line:517
        OO00OOO0O00OO0OOO ='http://api.tving.com/v1/media/stream/info?info=y%s&noCache=%s&mediaCode=%s&streamCode=%s&callingFrom=FLASH'%(config ['default_param'],O00OOO000OO0OOO00 ,O000000OOOOOOO0OO ,quality )#line:518
        OO00OOO0O00OO0OOO +='&deviceId=%s'%OO000O00O0O0O0000 #line:519
        OO0OOOO000000OOOO =None #line:520
        if proxy is not None :#line:521
            OO0OOOO000000OOOO ={"https":proxy ,'http':proxy }#line:522
        headers ['Cookie']=O0OO0O00O000O0OO0 #line:523
        O00OOO00000OOO0O0 =session .get (OO00OOO0O00OO0OOO ,headers =headers ,proxies =OO0OOOO000000OOOO )#line:524
        O000O0OO000O00O0O =O00OOO00000OOO0O0 .json ()#line:525
        if 'broad_url'in O000O0OO000O00O0O ['body']['stream']['broadcast']:#line:530
            O000O0OO000O00O0O ['body']['decrypted_url']=decrypt (O000000OOOOOOO0OO ,O00OOO000OO0OOO00 ,O000O0OO000O00O0O ['body']['stream']['broadcast']['broad_url'])#line:532
        return O000O0OO000O00O0O #line:535
    except Exception as O0O00O0O000O000O0 :#line:536
        logger .error ('Exception:%s',O0O00O0O000O000O0 )#line:537
        logger .error (traceback .format_exc ())#line:538
def get_schedules (O0O0OOOOO0OO00O0O ,OOO000000OO00OO00 ,O0O00O00OOO0000OO ,O0O0O0OOOO0OOOOO0 ):#line:541
    try :#line:543
        OO000O000OO0000O0 ='https://api.tving.com/v2/media/schedules?pageNo=1&pageSize=20&order=chno&scope=all&adult=n&free=all&broadDate=%s&broadcastDate=%s&startBroadTime=%s&endBroadTime=%s&channelCode=%s'%(OOO000000OO00OO00 ,OOO000000OO00OO00 ,O0O00O00OOO0000OO ,O0O0O0OOOO0OOOOO0 ,','.join (O0O0OOOOO0OO00O0O ))#line:545
        OO000O000OO0000O0 +=config ['default_param']#line:546
        O0000O0OOOO000O0O =requests .get (OO000O000OO0000O0 )#line:547
        return O0000O0OOOO000O0O .json ()#line:549
    except Exception as OO00OOO0O0OOOO00O :#line:550
        logger .error ('Exception:%s',OO00OOO0O0OOOO00O )#line:551
        logger .error (traceback .format_exc ())#line:552
