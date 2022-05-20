# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.  
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import requests
import json
from urllib3._collections import HTTPHeaderDict
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from threading import Thread
from ask_sdk_core.utils import is_intent_name, get_slot_value
from ask_sdk_model import Response, DialogState, Intent
from ask_sdk_core.utils import is_intent_name, get_dialog_state, get_slot_value
from ask_sdk_model.dialog import ElicitSlotDirective
from ask_sdk_model.request_envelope import RequestEnvelope 
from ask_sdk_model.response_envelope import ResponseEnvelope
from ask_sdk_model import (Intent , IntentConfirmationStatus, Slot, SlotConfirmationStatus)
import random
from ask_sdk_runtime.skill_builder import AbstractSkillBuilder
from ask_sdk_runtime.view_resolvers import AbstractTemplateLoader
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler,AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.response_helper import (get_plain_text_content, get_rich_text_content)
import urllib.request
from ask_sdk_model.interfaces.display import (ImageInstance, Image, RenderTemplateDirective, ListTemplate1,BackButtonBehavior, ListItem, BodyTemplate2, BodyTemplate1)
from ask_sdk_model import ui, Response
from ask_sdk_model.dialog import DelegateDirective
from ask_sdk_model.intent_confirmation_status import IntentConfirmationStatus
from ask_sdk_model.directive import Directive
from ask_sdk_core.response_helper import ResponseFactory
import ask_sdk_model.dialog as dialog

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

platform_id =  None
ids =  None
#question_text= None
#attr[question_text]= None
okay_msg = "If you need assistance, say “Help” anytime. Let's begin OpenEyes survey, okay?"

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global intent
        intent=0
        global repeat
        repeat=0
        global resume
        resume=0
        global arry
        arry=[]
        attr = handler_input.attributes_manager.session_attributes
        speak_output = "OpenEyes Surveys ready to Use. Tell me your Survey ID."
        handler_input.attributes_manager.session_attributes = attr
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Please tell me your Survey I D to begin.")
            .response
        )

class SurveyIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SurveyIntent")(handler_input)
        
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global intent
        intent=1
        global repeat
        repeat=1
        global resume
        resume=1
        attr = handler_input.attributes_manager.session_attributes
        idd=get_slot_value( 
            handler_input=handler_input, slot_name="survey")
        idds = len(idd)
        attr["counter"]= 0
        attr["options"]= 0
        attr["rating"]= 0
        #attr["question_text"] =0
        arry.append(idd) 
        arrys = len(arry)
        if arrys <=3 :
            surveyid = requests.get("Company_API" + str(idd))
            respss= surveyid.json()
            codes= (respss["code"])
            if str(codes) == "200":
                data_id = (respss["data"]["id"])
                r=requests.get("Company_API" + str(data_id) )
                resp= r.json()
                global datas
                datas=(resp["data"]["surveyDetails"])
                global ids
                ids=(datas["id"])
                global platform_id
                platform_id=(datas["platform_id"])
                global survey_name
                survey_name = (datas["survey_name"])
                urls="Company_API"    
                headers = {'Content-Type':'application/json','Accept':'application/json','Authorization':'mNIPg8r7wMnOhnQByiX1KpwjHwz3CzCnr7O9hQY0uZ1AXcwGcFVnxApaFKIY6Rs0keYaaVyoH1gaTqTBgQX2b1YRLVIlFdQfDCHLcWzRdxO7pCJlcV0aqaeYEJSABoXS'}
                myobj = {
                    "survey_id":ids,
                    "platform_id": platform_id
        
                        }           
                y = requests.post(url=urls,headers=headers,data=json.dumps(myobj))
                global resps
                resps=y.json()
                #messages=(resps["message"])
                global datass
                datass=(resps["data"]["Questions"])
                ids=(datass[attr["counter"]]["question_id"])
                survey_id=(datass[attr["counter"]]["survey_id"])
                platform_id=(datass[attr["counter"]]["platform_id"])
                question_option_id=(datass[attr["counter"]]["question_option_id"])
                ques=(datass[attr["counter"]]["question"])
                global question_text
                question_text = (ques["question_text"])
                attr["question_text"]=(ques["question_text"])
                question_type_id=(ques["question_type_id"])
                handler_input.attributes_manager.session_attributes = attr
                global description
                description = (datas["description"])
                global pop_description
                pop_description = "1"
                #if str(pop_description) == "1":   
                    #speak_output =  str(description)  +  "If you need assistance, say “Help” anytime. Let's begin OpenEyes survey, okay?"
                #elif str(pop_description) == "0":
                global msgs
                msgs =1
                speak_output =  "If you need assistance, say “Help” anytime. Let's begin OpenEyes survey, okay?"
                #else:
                    #speak_output =  "If you need assistance, say “Help” anytime. Let's begin OpenEyes survey, okay?"
            else:
                if arrys <=2: 
                    global msgss
                    msgss = 2
                    speak_output = "Invalid Survey ID. Please Try Again."
                else:
                    global msgsss
                    msgsss=3
                    speak_output = "Sorry, I am unable to find your Survey ID. Say 'Stop' to end the skill, and try again later." 
        
        else:
            msg=5
            speak_output = "Sorry, I am unable to find your Survey ID. Say 'Stop' to end the skill, and try again later. " 
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
            )

class QuestionIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("QuestionIntent")(handler_input) 
        
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr = handler_input.attributes_manager.session_attributes
        #global attr["answer"]
        attr["answer"]=get_slot_value( 
            handler_input=handler_input, slot_name="answer")
        intent_name = ask_utils.get_intent_name(handler_input)
        global intent
        intent=2
        global repeat
        repeat=2
        global resume
        resume=2
        try:
            Descriptive = 'b16631e5-0740-11ec-af38-1908de41ac9c'
            Dropdownwithsingleselection = 'b1662a30-0740-11ec-af38-1908de41ac9c'
            MCQ = 'b166063b-0740-11ec-af38-1908de41ac9c'
            MCQwithmultipleselection = 'b1662e42-0740-11ec-af38-1908de41ac9c'
            ShortAnswer = 'b1662dde-0740-11ec-af38-1908de41ac9c'
            Rating = '77b55f4a-639e-4708-9412-5b46f7e3972b'
            GroupRating = 'ec856a6e-a071-4496-829e-ce407ad3d3fa'
            #messages=(resps["message"])
            datass=(resps["data"]["Questions"])
            thank_you_message = (datas["thank_you_message"])
            thank_you_msg_pop = (datas["populate_thankyou_message"])
            ques=(datass[attr["counter"]]["question"])
            global questions
            questions=(datass[attr["options"]-1]["question"])
            attr["question_text"]=(ques["question_text"])
            global ratingss
            ratingss=(ques["rating"])
            #rattingsss = int(ratingss)
            global question_type_id
            question_type_id=(ques["question_type_id"])
            is_other=(ques["is_other"])
            global is_others
            is_others=(questions["is_other"])
            if str(is_others) == "1":
                global flag
                flag = 1
            options_keys=[]
            response=[]
            global num
            num=[1,2,3,4,5]
            dictionary={}
            global mcq_options
            mcq_options=[]
            global mcqsthatnotdisplay
            mcqsthatnotdisplay=[]
            global ratingsss
            ratingsss=[]
            global ratingsthatnotdisply
            ratingsthatnotdisply =[]
            optionss= len(ques["options"])
            global QuestionLimits
            QuestionLimits=(resps["data"]["QuestionLimits"])
            global optionsthatnotdisplay
            optionsthatnotdisplay= len(questions["options"])
            if str(question_type_id) == MCQwithmultipleselection:
                dictionary.clear()
                mcq_options.clear()
                for i in range(optionss):
                    options=(ques["options"])
                    option_texts=((options[i]["option_text"]))
                    mcq_options.append(option_texts.lower())
                    optionss=len(options)
                if str(is_other) == "0":
                    speech_output= "Question " + str(attr["counter"]+1) +  " " + attr["question_text"]  + " Choose multiple from "+ str(mcq_options) 
                else:
                    speech_output="Question " + str(attr["counter"]+1) +  " " + attr["question_text"] + " Choose multiple from "+ str(mcq_options) +" Other"

            elif str(question_type_id) == Descriptive:
                handler_input.attributes_manager.session_attributes = attr
                speech_output= "Question " + str(attr["counter"]+1) +  " " + attr["question_text"] + " Reply in Detail."  
            elif str(question_type_id) == ShortAnswer:
                handler_input.attributes_manager.session_attributes = attr
                speech_output="Question " + str(attr["counter"]+1) +  " " + attr["question_text"] + " Reply briefly." 
            elif str(question_type_id) == MCQ:
                dictionary.clear()
                mcq_options.clear()
                for i in range(optionss):
                    options=(ques["options"])
                    option_texts=((options[i]["option_text"]))
                    mcq_options.append(option_texts.lower())
                    optionss=len(options)
                if str(is_other) == "0":
                    speech_output= "Question " + str(attr["counter"]+1) +  " " + attr["question_text"] + " Choose only one from  " + str(mcq_options)  
                else: 
                    speech_output= "Question " + str(attr["counter"]+1) +  " " + attr["question_text"] + " Choose multiple from " + str(mcq_options) + " Other" 
            elif str(question_type_id) == Dropdownwithsingleselection:
                dictionary.clear()
                mcq_options.clear()
                for i in range(optionss):
                    options=(ques["options"])
                    option_texts=((options[i]["option_text"]))
                    mcq_options.append(option_texts.lower())
                    optionss=len(options)
                if str(is_other)=="0":
                    speech_output = "Question " + str(attr["counter"]+1) +  " " + attr["question_text"]  + str(mcq_options) 
                else:
                    speech_output = "Question " + str(attr["counter"]+1) +  " " + attr["question_text"] + " Choose multiple from "+ str(mcq_options) + " Other"  
            
            elif str(question_type_id) == Rating:
                global rating
                rating=get_slot_value( 
                    handler_input=handler_input, slot_name="rating")
                handler_input.attributes_manager.session_attributes = attr
                for i in range(ratingss + 1):
                    ratingsss.append(i)
                speech_output= "Question " + str(attr["counter"]+1) +  " " + attr["question_text"] +  " Rate out of 5."
                
            elif str(question_type_id) == GroupRating:
                for i in range(ratingss + 1):
                    ratingsss.append(i)
                global rating_group
                rating_group=(ques["rating_group"])
                grp_question_text= (rating_group[attr["rating"]]["question_text"])
                #speech_output= str(grp_question_text)
                global grp_question_text_len
                grp_question_text_len= len(rating_group)
                global group_parent_question_id
                group_parent_question_id= (rating_group[attr["rating"]]["group_parent_question_id"])
                global grp_question_id
                grp_question_id= (rating_group[attr["rating"]-1]["id"])
                #speech_output= str(grp_question_text)
                if attr["rating"]==0:
                    speech_output= "Question " + str(attr["counter"]+1) +  " " + attr["question_text"] +  " Rate out of 5. " + grp_question_text
                else:
                    speech_output=  grp_question_text
                
            else:
                dictionary.clear()
                mcq_options.clear()
                for i in range(optionss):
                    options=(ques["options"])
                    option_texts=((options[i]["option_text"]))
                    mcq_options.append(option_texts)
                speech_output = "Question " + str(attr["counter"]+1) +  " " + attr["question_text"]  + str(mcq_options)
                handler_input.attributes_manager.session_attributes = attr
            
				attr["counter"]= 0
				attr["options"]= 0
				attr["rating"]= 0
			return (
				handler_input.response_builder
				.add_directive(directive = dialog.ElicitSlotDirective(
                        slot_to_elicit = 'answer'
                        )
                    )
				.speak(speech_output )
				.ask(speech_output)
				.response
				)

class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for repeating the response to the user."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #logger.info("In RepeatHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        #if "recent_response" in attr:
        cached_response_str = json.dumps(attr["recent_response"])
        cached_response = DefaultSerializer().deserialize(cached_response_str, Response)
        #return cached_response
        speak_output=str(question_text)
        return cached_response.handler_input.response_builder.speak(speak_output).ask(speak_output).add_directive(DelegateDirective(updated_intent= {"name":"QuestionIntent", "confirmationStatus": "None", "slots" : {}})).response

        #else:
            #response_builder.speak(data.FALLBACK_ANSWER).ask(data.HELP_MESSAGE)
            #return response_builder.response

class HomeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("HomeIntent")(handler_input)
    
    def handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        global repeat
        repeat=3
        global resume
        resume =3
        if intent==4:
            speak_output="Just say, “Alexa home” for me to end the skill. If you want to continue then say “Resume”"
        else:
            attr["counter"]= 0
            speak_output = "OpenEyes Surveys ready to Use. Tell me your Survey ID." 
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
            )
    
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global intent
        intent=4
        global repeat
        repeat =9
        help_=get_slot_value( 
            handler_input=handler_input, slot_name="help")
        if help_ == "options":
            speak_output="Help Options Include: Repeat, Home Or you can resume what you were doing."
        elif help_ == "repeat":
            speak_output="Just say, “Alexa repeat” for me to repeat the last thing I said"
        elif help_ == "stop":    
            speak_output="Just say, “Alexa Stop” for me to end the skill."
        elif help_ == "resume":
            speak_output = "If you need further assistance you can contact us through your Alexa app."
        elif help_ == "home":
            speak_output = "Just say, “Alexa home” for me to return to the start of the skill”"
        elif help_ == "report question":
            speak_output = "please give the reason for that question! or u can continue the survey!”"
        elif help_ == "report survey":
            speak_output = "please give the reason for that survey! or u can continue the survey!”"
        else:
            speak_output="Sorry? I don't understand. How may I help you?"
        return (
            handler_input.response_builder
            .add_directive(directive = dialog.ElicitSlotDirective(
                        slot_to_elicit = 'help'
                        )
                    )
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class StopIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = "Thank you for using OpenEyes Survey, please rate our skill in the your Alexa app. Goodbye"
        return (
            handler_input.response_builder
                .speak(speak_output)
                #.ask(speak_output)
                .response
        )

class PauseIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.PauseIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr = handler_input.attributes_manager.session_attributes
        speak_output =  "i will wait for 10 seconds..."
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

class ResumeIntentHandler(AbstractRequestHandler):
    """Handler for Resume Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.ResumeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr = handler_input.attributes_manager.session_attributes
        if resume==0:
            speech_output="Welcome Back...OpenEyes Surveys ready to Use. Tell me your Survey ID."
            return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(speech_output)
                .response
            )
        elif resume == 3:
            speech_output="Welcome Back...OpenEyes Surveys ready to Use. Tell me your Survey ID."
            return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(speech_output)
                .response
            )
        elif resume==1:
            #if str(pop_description) == "1":
                #speech_output ="Welcome Back..." + str(description)  +  "If you need assistance, say “Help” anytime. Let's begin OpenEyes survey, okay?"
            if msgs==1:
                speech_output ="Welcome Back...If you need assistance, say “Help” anytime. Let's begin OpenEyes survey, okay?"
            elif msgss==2:
                speech_output ="Welcome Back...Invalid Survey ID. Please Try Again."
            elif msgsss==3:
                speech_output ="Welcome Back...Sorry, I am unable to find your Survey ID. Say 'Stop' to end the skill, and try again later."
            else:
                speech_output ="Welcome Back...If you need assistance, say “Help” anytime. Let's begin OpenEyes survey, okay?"
            return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(speech_output)
                .response
            )
        elif resume==2:
            attr["counter"] -= 1
            attr["question_text"] -= 1
            attr["options"] -= 1
            speech_output= "welcome back..." +  question_texts + str(mcq_options) 
            attr["counter"] += 1
            attr["question_text"] += 1
            attr["options"] += 1
            
            
            return (
            handler_input.response_builder
            .add_directive(directive = dialog.ElicitSlotDirective(
                        slot_to_elicit = 'answer'
                        )
                    )
            .speak(speech_output )
            .ask(speech_output)
            .response
            )
        elif resume==5:
            speech_output="Welcome Back...OpenEyes Surveys ready to Use. Tell me your Survey ID."
            return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(speech_output)
                .response
            )
        else:
            speech_output="If you need further assistance you can contact us through your Alexa app."
            
            return (
                handler_input.response_builder
                    .speak(speech_output)
                    .ask(speech_output)
                    .response
            )

class feedbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("feedbackIntent")(handler_input)
    
    def handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        feedback=get_slot_value( 
            handler_input=handler_input, slot_name="feedback")
        global intent
        intent=6
        url="Company_API"    
        headerss = {'Content-Type':'application/json','Accept':'application/json'}
        myobjs ={
                        "survey_id":ids,
                        "platform_id":platform_id,
                        "feedback":feedback
                    }
        
        yo = requests.post(url,headers=headerss,data=json.dumps(myobjs))
        speak_output ="Thank you for Giveing FeedBack. If you want to continue then say Resume,home or say stop to end the survey."

        handler_input.attributes_manager.session_attributes = attr
        return (
            handler_input.response_builder
                        .add_directive(directive = dialog.ElicitSlotDirective(
                        slot_to_elicit = 'feedback'
                        )
                    )

                .speak(speak_output)
                #.ask(speak_output)
                .response
            )

class NextIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.NextIntent")(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return QuestionIntentHandler().handle(handler_input)

class CacheResponseForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the response sent to the user in session.
    The interceptor is used to cache the handler response that is
    being sent to the user. This can be used to repeat the response
    back to the user, in case a RepeatIntent is being used and the
    skill developer wants to repeat the same information back to
    the user.
    """
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["recent_response"] = response

"""
class RepeatInterceptor(AbstractResponseInterceptor):

    def process(self, handler_input, response):
        attr = handler_input.attributes_manager.session_attributes
        attr["repeat_speech_output"] = response.output_speech.ssml.replace("<speak>","").replace("</speak>","")
        try:
            attr["repeat_reprompt"] = response.reprompt.output_speech.ssml.replace("<speak>","").replace("</speak>","")
        except:
            attr["repeat_reprompt"] = response.output_speech.ssml.replace("<speak>","").replace("</speak>","")
"""
class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

# Request and Response Loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Envelope: {}".format(
            handler_input.request_envelope))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Response: {}".format(response))

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again." 

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SurveyIntentHandler())
sb.add_request_handler(QuestionIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(HomeIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(StopIntentHandler())
sb.add_request_handler(PauseIntentHandler())
sb.add_request_handler(ResumeIntentHandler())
sb.add_request_handler(feedbackIntentHandler())
sb.add_request_handler(NextIntentHandler())
sb.add_global_response_interceptor(CacheResponseForRepeatInterceptor())
#sb.add_global_response_interceptor(RepeatInterceptor())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()