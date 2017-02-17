import json
import urllib.request`

def getVTT(url):
	vtt_response = urllib.request.urlopen(urllib.request.Request(url)).read()
	return getTranscript(vtt_response)

def getTranscript(response):
	vtt_response = response.decode('utf-8')
	vtt_list = vtt_response.split("\n\n")
	transcript = ""
	for i in range(0,len(vtt_list)):
		vtt_lines = vtt_list[i].split("\n")
		number_of_lines = len(vtt_lines) - 2
		for j in range(0,number_of_lines):
			transcript = transcript + vtt_lines[2+j] + " "
	return transcript

print(getVTT('https://www.coursera.org/api/subtitleAssetProxy.v1/OajtTUNVSJqo7U1DVcia_w?expiry=1487376000000&hmac=td2gpjX_kGkbscujImStOqiF-umhDEQwwCBgR7RB8LQ&fileExtension=srt'))
