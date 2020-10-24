import os #line:4
import traceback #line:5
import random #line:6
import json #line:7
import string #line:8
import codecs #line:9
import requests #line:12
from flask import Blueprint ,request ,Response ,send_file ,render_template ,redirect ,jsonify #line:13
from framework .logger import get_logger #line:16
from framework import path_app_root ,app #line:17
from framework .util import Util #line:18
from .plugin import package_name ,logger #line:21
from .model import ModelSetting #line:22
class SystemLogicAuth (object ):#line:24
    @staticmethod #line:25
    def process_ajax (OOOOOOO000O0O0000 ,OOO00OOOOO000OOO0 ):#line:26
        logger .debug (OOOOOOO000O0O0000 )#line:27
        try :#line:28
            if OOOOOOO000O0O0000 =='apikey_generate':#line:29
                OOO00OO0OOOOO000O =SystemLogicAuth .apikey_generate ()#line:30
                return jsonify (OOO00OO0OOOOO000O )#line:31
            elif OOOOOOO000O0O0000 =='do_auth':#line:32
                OOO00OO0OOOOO000O =SystemLogicAuth .do_auth ()#line:33
                return jsonify (OOO00OO0OOOOO000O )#line:34
        except Exception as O000000O0O0O0OOO0 :#line:35
            logger .error ('Exception:%s',O000000O0O0O0OOO0 )#line:36
            logger .error (traceback .format_exc ())#line:37
    @staticmethod #line:42
    def apikey_generate ():#line:43
        try :#line:44
            O00O000OO00OO0OO0 =''.join (random .choice (string .ascii_uppercase +string .digits )for _O0OOOOOOOOOO0OOOO in range (10 ))#line:45
            return O00O000OO00OO0OO0 #line:46
        except Exception as OOO0OOOOOO000OOOO :#line:47
            logger .error ('Exception:%s',OOO0OOOOOO000OOOO )#line:48
            logger .error (traceback .format_exc ())#line:49
    @staticmethod #line:52
    def get_auth_status (retry =True ):#line:53
        try :#line:54
            OO0OOOO000O0OO000 =ModelSetting .get ('auth_status')#line:55
            OOO0O00OOOOO00O00 ={'ret':False ,'desc':'','level':0 ,'point':0 }#line:56
            if OO0OOOO000O0OO000 =='':#line:57
                OOO0O00OOOOO00O00 ['desc']='미인증'#line:58
            elif OO0OOOO000O0OO000 =='wrong_id':#line:59
                OOO0O00OOOOO00O00 ['desc']='미인증 - 홈페이지 아이디가 없습니다.'#line:60
            elif OO0OOOO000O0OO000 =='too_many_sjva':#line:61
                OOO0O00OOOOO00O00 ['desc']='미인증 - 너무 많은 SJVA를 사용중입니다.'#line:62
            elif OO0OOOO000O0OO000 =='wrong_apikey':#line:63
                OOO0O00OOOOO00O00 ['desc']='미인증 - 홈페이지에 등록된 APIKEY와 다릅니다.'#line:64
            else :#line:65
                O0000OO0O0O000O0O =SystemLogicAuth .check_auth_status (OO0OOOO000O0OO000 )#line:66
                if O0000OO0O0O000O0O is not None and O0000OO0O0O000O0O ['ret']:#line:67
                    OOO0O00OOOOO00O00 ['ret']=O0000OO0O0O000O0O ['ret']#line:68
                    OOO0O00OOOOO00O00 ['desc']='인증되었습니다. (회원등급:%s, 포인트:%s)'%(O0000OO0O0O000O0O ['level'],O0000OO0O0O000O0O ['point'])#line:69
                    OOO0O00OOOOO00O00 ['level']=O0000OO0O0O000O0O ['level']#line:70
                    OOO0O00OOOOO00O00 ['point']=O0000OO0O0O000O0O ['point']#line:71
                else :#line:72
                    if retry :#line:73
                        SystemLogicAuth .do_auth ()#line:74
                        return SystemLogicAuth .get_auth_status (retry =False )#line:76
                    else :#line:77
                        OOO0O00OOOOO00O00 ['desc']='잘못된 값입니다. 다시 인증하세요.'#line:78
            return OOO0O00OOOOO00O00 #line:79
        except Exception as OOOO0OOOOO0OOO0O0 :#line:80
            logger .error ('Exception:%s',OOOO0OOOOO0OOO0O0 )#line:81
            logger .error (traceback .format_exc ())#line:82
    @staticmethod #line:84
    def check_auth_status (value =None ):#line:85
        try :#line:86
            from framework .common .util import AESCipher #line:88
            if app .config ['config']['is_py2']:#line:103
                OOOOOOOO0O0OO000O =AESCipher .decrypt (value ,mykey =(SystemLogicAuth .get_ip ().encode ('hex')+ModelSetting .get ('auth_apikey').encode ("hex")).zfill (32 )[:32 ]).split ('_')#line:104
            else :#line:105
                OO00O0000O000O000 =(codecs .encode (SystemLogicAuth .get_ip ().encode (),'hex').decode ()+codecs .encode (ModelSetting .get ('auth_apikey').encode (),'hex').decode ()).zfill (32 )[:32 ].encode ()#line:106
                logger .debug (OO00O0000O000O000 )#line:107
                OOOOOOOO0O0OO000O =AESCipher .decrypt (value ,mykey =OO00O0000O000O000 ).decode ()#line:108
                OOOOOOOO0O0OO000O =OOOOOOOO0O0OO000O .split ('_')#line:109
            OO00OOOOO00O0O0OO ={}#line:110
            OO00OOOOO00O0O0OO ['ret']=(ModelSetting .get ('sjva_id')==OOOOOOOO0O0OO000O [0 ])#line:111
            OO00OOOOO00O0O0OO ['level']=int (OOOOOOOO0O0OO000O [1 ])#line:112
            OO00OOOOO00O0O0OO ['point']=int (OOOOOOOO0O0OO000O [2 ])#line:113
            return OO00OOOOO00O0O0OO #line:114
        except Exception as OOOO0OOOO0OOOO00O :#line:115
            logger .error ('Exception:%s',OOOO0OOOO0OOOO00O )#line:116
            logger .error (traceback .format_exc ())#line:117
    @staticmethod #line:119
    def make_auth_status (O000OO0O0OO0OOO0O ,O00OOO000O000000O ):#line:120
        try :#line:121
            from framework .common .util import AESCipher #line:122
            if app .config ['config']['is_py2']:#line:123
                O0O0O0O0OOOOO0O0O =AESCipher .encrypt (str ('%s_%s_%s'%(ModelSetting .get ('sjva_id'),O000OO0O0OO0OOO0O ,O00OOO000O000000O )),mykey =(codecs .encode (SystemLogicAuth .get_ip ().encode (),'hex')+codecs .encode (ModelSetting .get ('auth_apikey').encode (),'hex')).zfill (32 )[:32 ])#line:124
            else :#line:125
                O0OO000O0OOOO00O0 =(codecs .encode (SystemLogicAuth .get_ip ().encode (),'hex').decode ()+codecs .encode (ModelSetting .get ('auth_apikey').encode (),'hex').decode ()).zfill (32 )[:32 ].encode ()#line:126
                O0O0O0O0OOOOO0O0O =AESCipher .encrypt (str ('%s_%s_%s'%(ModelSetting .get ('sjva_id'),O000OO0O0OO0OOO0O ,O00OOO000O000000O )),mykey =O0OO000O0OOOO00O0 )#line:127
            logger .debug (O0O0O0O0OOOOO0O0O )#line:128
            return O0O0O0O0OOOOO0O0O #line:129
        except Exception as O0OO00OO0O0OO0000 :#line:130
            logger .error ('Exception:%s',O0OO00OO0O0OO0000 )#line:131
            logger .error (traceback .format_exc ())#line:132
    @staticmethod #line:135
    def get_ip ():#line:136
        import socket #line:137
        OO0OO0OOOO00000OO =socket .socket (socket .AF_INET ,socket .SOCK_DGRAM )#line:138
        try :#line:139
            OO0OO0OOOO00000OO .connect (('10.255.255.255',1 ))#line:141
            OO00OO0OOOOO0000O =OO0OO0OOOO00000OO .getsockname ()[0 ]#line:142
        except Exception :#line:143
            OO00OO0OOOOO0000O ='127.0.0.1'#line:144
        finally :#line:145
            OO0OO0OOOO00000OO .close ()#line:146
        logger .debug ('IP:%s',OO00OO0OOOOO0000O )#line:147
        return OO00OO0OOOOO0000O #line:148
    @staticmethod #line:150
    def do_auth ():#line:151
        try :#line:152
            O0O0OOOOO0OOO00OO ={'ret':False ,'msg':'','level':0 ,'point':0 }#line:153
            O000OO0OOO0OOOO0O =ModelSetting .get ('auth_apikey')#line:154
            OO0000O000OOO0OO0 =ModelSetting .get ('sjva_me_user_id')#line:155
            if len (O000OO0OOO0OOOO0O )!=10 :#line:156
                O0O0OOOOO0OOO00OO ['msg']='APIKEY 문자 길이는 10자리여야합니다.'#line:157
                return O0O0OOOOO0OOO00OO #line:158
            if OO0000O000OOO0OO0 =='':#line:159
                O0O0OOOOO0OOO00OO ['msg']='홈페이지 ID가 없습니다.'#line:160
                return O0O0OOOOO0OOO00OO #line:161
            OO00O000OO0O0OOO0 =requests .post ('https://sjva.me/sjva/auth.php',data ={'apikey':O000OO0OOO0OOOO0O ,'user_id':OO0000O000OOO0OO0 ,'sjva_id':ModelSetting .get ('sjva_id')}).json ()#line:164
            if OO00O000OO0O0OOO0 ['result']=='success':#line:165
                O0O0OOOOO0OOO00OO ['ret']=True #line:166
                O0O0OOOOO0OOO00OO ['msg']=u'총 %s개 등록<br>레벨:%s, 포인트:%s'%(OO00O000OO0O0OOO0 ['count'],OO00O000OO0O0OOO0 ['level'],OO00O000OO0O0OOO0 ['point'])#line:167
                O0O0OOOOO0OOO00OO ['level']=int (OO00O000OO0O0OOO0 ['level'])#line:168
                O0O0OOOOO0OOO00OO ['point']=int (OO00O000OO0O0OOO0 ['point'])#line:169
                ModelSetting .set ('auth_status',SystemLogicAuth .make_auth_status (O0O0OOOOO0OOO00OO ['level'],O0O0OOOOO0OOO00OO ['point']))#line:170
            else :#line:171
                ModelSetting .set ('auth_status',OO00O000OO0O0OOO0 ['result'])#line:172
                OOOO0OO0000000O00 =SystemLogicAuth .get_auth_status (retry =False )#line:173
                O0O0OOOOO0OOO00OO ['ret']=OOOO0OO0000000O00 ['ret']#line:174
                O0O0OOOOO0OOO00OO ['msg']=OOOO0OO0000000O00 ['desc']#line:175
            return O0O0OOOOO0OOO00OO #line:176
        except Exception as O00OOO0OOOOOOO0OO :#line:177
            logger .error ('Exception:%s',O00OOO0OOOOOOO0OO )#line:178
            logger .error (traceback .format_exc ())#line:179
