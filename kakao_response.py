import json

def simple_text(text) :
	res = {
		"version": "2.0",
		"template": {
			"outputs": [
			{
				"simpleText": {
					"text": text
				}
			}
			]
		}
	}
	return res;

def to_button(action,label,webLinkUrl=None,messageText=None) :
	
	res = {
		"action": action,
		"label": label,
	}

	if webLinkUrl is not None :
		res["webLinkUrl"]=webLinkUrl
	elif messageText is not None :
		res["messageText"]=messageText

	return res;


def to_item(title,description,imageUrl,buttons) :
	res = {
		"title": title,
		"description": description,
		"thumbnail": {
			"imageUrl": imageUrl
		},
		"buttons": buttons
	}
	return res;



def basic_card_carousel(items) :
	res = {
		"version": "2.0",
		"template": {
			"outputs": [
			{
				"carousel": {
					"type": "basicCard",
					"items": items
				}
			}
			]
		}
	}
	return res
