#!/usr/bin/python3

import uuid
import os
import sys
import configparser

config = configparser.ConfigParser()
config.read('../smart_speaker.conf')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.get('dialogflow', 'google_app_credential')
project_id = config.get('dialogflow', 'project_id')
session_id = str(uuid.uuid4())
language_code = 'zh-TW'

query = sys.argv[1]

def detect_intent_texts(project_id, session_id, texts, language_code):
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print('Session path: {}'.format(session))

    text_input = dialogflow.types.TextInput(
        text=texts, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}'.format(
        response.query_result.fulfillment_text))


detect_intent_texts(project_id, session_id, query, language_code)

