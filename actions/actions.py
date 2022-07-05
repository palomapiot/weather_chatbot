# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        temp = int(weather(city)['temp'] - 273)

        dispatcher.utter_message(response="utter_weather", temp=temp)

        return []

class ActionSearchPodcast(Action):

    def name(self) -> Text:
        return "action_search_podcast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query = tracker.get_slot("search_query")
        result = search_podcast(query)[0]['attributes']['title']

        dispatcher.utter_message(response="utter_episode_search_result", episode_title=result)

        return []

class ActionRecommendPodcast(Action):

    def name(self) -> Text:
        return "action_recommend_podcast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = recommend_podcast()[0]['attributes']['title']
        dispatcher.utter_message(response="utter_podcast_recommendation", podcast_title=result)

        return []

class ActionLastUpdatedPodcast(Action):

    def name(self) -> Text:
        return "action_last_updated_podcast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = last_updated_podcast()[0]['attributes']['title']
        dispatcher.utter_message(response="utter_last_updated_podcast_response", podcast_title=result)

        return []

class ActionMostSubscribedPodcast(Action):

    def name(self) -> Text:
        return "action_most_subscribed_podcast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = most_subscribed_podcast()[0]['attributes']['title']
        dispatcher.utter_message(response="utter_subscribed_podcast_response", podcast_title=result)

        return []

def weather(city):
    api_adress = 'http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
    url = api_adress + city
    json_data = requests.get(url).json()

    format_weather = json_data['main']

    return format_weather

def load_json_data(url):
    return requests.get(url).json()['data']

def search_podcast(query: Text):
    url = 'https://panoptikum.io/jsonapi/episodes/search?filter={}'.format(query)
    return load_json_data(url)

def recommend_podcast():
    url = 'https://panoptikum.io/jsonapi/recommendations/random'
    return load_json_data(url)

def last_updated_podcast():
    url = 'https://panoptikum.io/jsonapi/podcasts/last_updated'
    return load_json_data(url)

def most_subscribed_podcast():
    url = 'https://panoptikum.io/jsonapi/podcasts/most_subscribed'
    return load_json_data(url)


    