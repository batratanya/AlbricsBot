import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "jfile.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "lyrics-buyjbg"

from PyLyrics import *
from pymongo import MongoClient

client=MongoClient("mongodb+srv://test:test@cluster0-761nn.mongodb.net/test?retryWrites=true&w=majority")
data=client.get_database('user_data')
records=data.music_query


def get_albums(parameters):
	value = PyLyrics.getAlbums(parameters.get('music-artist'))
	return "\n".join([str(x) for x  in value])


def get_lyrics(parameters):
	return str(PyLyrics.getLyrics(parameters.get('music-artist'),parameters.get('songName')))[:1100]

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(query, session_id):
	response = detect_intent_from_text(query,session_id)
	records.insert_one(dict(response.parameters))
	if response.intent.display_name =='get_lyrics':
		return get_lyrics(dict(response.parameters))
	elif response.intent.display_name =='get_songs':
		return get_albums(dict(response.parameters))
	else:
		return response.fulfillment_text


