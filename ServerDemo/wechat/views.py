from django.shortcuts import render
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatConf
from wechat_sdk import WeChatBasic
from wechat_sdk.exceptions import ParserError
from wechat_sdk.message import (TextMessage,VoiceMessage,ImageMessage,VideoMessage)

MyConf=WechatConf(
		token='YOUR_TOKEN_HEAE',
		appid='YOUR_APPID',
		appsecret='YOUR_APPSECRET'
		encrypt_mode='YOUR_MODE',
		encoding_aes_key='YOUR_AES_KEY'
		)
# Create your views here.

def wechat_home(request):
	signature=request.GET.get('signature')
	timestamp=request.GET.get('timestamp')
	nonce = request.GET.get('nonce')
	wechat_instance = WechatBasic(conf=MyConf)
	if not wechat_instance.check_signature(signature=signature,timestamp=timestamp,nonce=nonce):
		return HttpResponseBadRequest('Verify Failed')
	else:
		if request.method == 'GET':
			response = request.GET.get('echostr','error')
		else:
			try:
				wechat_instance.parse_data(request.body)
				message = wechat_instance.get_message()
				if isinstance(message,TextMessage):
					reply_text='text'
				else:
					reply_text='other'
				response = wechat_instance.response_text(content=reply_text)
			except ParseError:
				return HttpResponseBadRequest("Invalid XML Data")
		return HttpResponse(reponse,content_type='application/xml')

