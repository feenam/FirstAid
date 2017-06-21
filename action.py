"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "<speak>First Aid here, What can I help you with?</speak>"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "<speak>What can I help you with?</speak>"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "<speak>Thanks for using First Aid, be safe!</speak>"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def get_call_911(intent, session):
    ### get call 911 response

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "<speak>Call 911</speak>"
    reprompt_text = "<speak>Call 911</speak>"
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_list_of_things_to_say(intent, session):
    ### get list of possible commands

    session_attributes = {}
    should_end_session = False
    reprompt_text = None
    if session.get('attributes', {}) and "onCPR" in session.get('attributes', {}): 
        speech_output = "<speak>how do i do chest compressions, <break time='0.5s'/>"\
                        "how do i do rescue breaths, <break time='0.5s'/>"\
                        "how do i do breaths, <break time='0.5s'/>"\
                        "restart chest compressions, <break time='0.5s'/>"\
                        "restart rescue breaths, <break time='0.5s'/>"\
                        "restart breaths, <break time='0.5s'/>"\
                        "stop CPR, <break time='0.5s'/>"\
                        "quit CPR</speak>"
    else :
        speech_output = "<speak>I need help with CPR, <break time='1s'/>" \
                        "i need help with checking an injured adult, <break time='1s'/>" \
                        "i need help with choking, <break time='1s'/>" \
                        "i need help with AED, <break time='1s'/>" \
                        "i need help with controlling bleeding, <break time='1s'/>" \
                        "i need help with stroke, <break time='1s'/>" \
                        "someone is bleeding, <break time='1s'/>" \
                        "someone is injured, <break time='1s'/>" \
                        "someone drank a poison, <break time='1s'/>" \
                        "someone hurt his neck. <break time='1s'/></speak>"
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def create_choking_attribute(choking_type):
    return {"chokingType": choking_type}

def get_choking_with_type_help(intent, session):
    ### get choking help prompt
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "<speak>Call 911</speak>"
    reprompt_text = None
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_choking_help(intent, session):
    ### get choking help prompt
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "<speak>Is the person conscious or unconscious<break time='0.5s'/>" \
                        "Say, conscious choking, or, unconscious choking.</speak>"
    reprompt_text = "<speak>Say, conscious choking, or, unconscious choking.</speak>"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def create_cpr_attributes(cpr_need, rep): ### CPR ATTRIBUTE
    return {"onCPR": cpr_need, "rep": rep}

def get_cpr_help(intent, session):
    ### get CPR instruction prompt
    card_title = intent['name']
    session_attributes = {}
    speech_output = ""
    should_end_session = False
    reprompt_text = None
    chest_compression = "<speak>Push hard, push fast in the middle of the chest at least two inches deep <break time='0.5s'/> and at least hundred compressions per minute <break time='0.5s'/></speak>"
    rescue_breath = "<speak>tilt the head back and lift the chin up <break time='0.5s'/>" \
                    "pinch the nose shut then make a complete seal over the person's mouth <break time='0.5s'/>"\
                    "blow in for about 1 second to make the chest clearly rise <break time='0.5s'/>"\
                    "give rescue breaths, one after other  <break time='0.5s'/>"\
                    "when are done with rescue breaths, say 'done'</speak>"

    ### Deal with Commands here
    if intent['name'] == "FinishIntent":
        speech_output = "<speak>Are you sure you want to stop?</speak>"
    elif intent['name'] == "YesIntent":
        speech_output = "<speak>good bye</speak>"
        should_end_session = True
    elif intent['name'] == "RestartIntent":
        if intent['slots']['stage']['value'] == "rescue breaths" or intent['slots']['stage']['value'] == "breaths":
            reprompt_text = "<speak>when are done with rescue breaths, say 'done'</speak>"
            if session['attributes']['rep'] == 0:
                speech_output = rescue_breath
                session_attributes = create_cpr_attributes("c", 1)
            else:
                speech_output = "<speak>when are done with rescue breaths, say 'done'</speak>"
                session_attributes = create_cpr_attributes("c", 1)
        else:
            speech_output = "<speak>when you are done with 30 compressions, say 'done'<audio src='https://s3.amazonaws.com/feenamsample/test.mp3'/></speak>"
            reprompt_text = "<speak>when you are done with 30 compressions, say 'done'</speak>"
            if session['attributes']['rep'] == 0:
                session_attributes = create_cpr_attributes("b", 0)
            else:
                session_attributes = create_cpr_attributes("b", 1)
    ### Rest of the cpr function
    elif session.get('attributes', {}) and "onCPR" in session.get('attributes', {}): 
        if session['attributes']['onCPR'] == "c":
            speech_output = "<speak>when you are done with 30 compressions, say 'done'<audio src='https://s3.amazonaws.com/feenamsample/test.mp3'/></speak>"
            reprompt_text = "<speak>when you are done with 30 compressions, say 'done'</speak>"
            if session['attributes']['rep'] == 0:
                session_attributes = create_cpr_attributes("b", 0)
            else:
                session_attributes = create_cpr_attributes("b", 1)
        elif session['attributes']['onCPR'] == "b":
            reprompt_text = "<speak>when are done with rescue breaths, say 'done'</speak>"
            if session['attributes']['rep'] == 0:
                speech_output = rescue_breath
                session_attributes = create_cpr_attributes("c", 1)
            else:
                speech_output = "<speak>when are done with rescue breaths, say 'done'</speak>"
                session_attributes = create_cpr_attributes("c", 1)
    else:
        speech_output = "I will help you with CPR, step by step <break time='0.5s'/>" \
                        "lay the person on a firm, flat surface <break time='0.5s'/>" \
                        "you will give 30 chest compressions <break time='0.5s'/>" \
                        "Push hard, push fast in the middle of the chest at least two inches deep, and at least hundred compressions per minute <break time='0.5s'/>" \
                        "when you are ready to begin, say 'ready'  <break time='0.5s'/>"\
                        "when you are done with 30 compressions, say 'done'</speak>"
        session_attributes = create_cpr_attributes("c", 0)

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def how_to_cpr(intent, session):
    card_title = intent['name']
    session_attributes = {}
    speech_output = ""
    should_end_session = False
    reprompt_text = None

    if intent['slots']['stage']['value'] == "chest compressions":
        speech_output = "<speak>Push hard, push fast in the middle of the chest at least two inches deep <break time='0.5s'/> and at least hundred compressions per minute <break time='0.5s'/></speak>"
    else:
        speech_output = "<speak>tilt the head back and lift the chin up <break time='0.5s'/>" \
                        "pinch the nose shut then make a complete seal over the person's mouth <break time='0.5s'/>"\
                        "blow in for about 1 second to make the chest clearly rise <break time='0.5s'/>"\
                        "give rescue breaths, one after other  <break time='0.5s'/></speak>"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetHelpIntent":
        return get_call_911(intent, session)
    elif intent_name == "GetChokingTypeIntent":
        return get_choking_with_type_help(intent, session)
    elif intent_name == "GetChokingIntent":
        return get_choking_help(intent, session)
    elif intent_name == "GetCPRHelpIntent":
        return get_cpr_help(intent, session)
    elif intent_name == "RestartIntent":
        return get_cpr_help(intent, session)
    elif intent_name == "CommandIntent" or intent_name == "FinishIntent" or intent_name == "YesIntent":
        return get_cpr_help(intent, session)
    elif intent_name == "HowIntent":
        return how_to_cpr(intent, session)
    elif intent_name == "GetListIntent":
        return get_list_of_things_to_say(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
