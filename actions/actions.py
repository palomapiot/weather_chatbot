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

class ActionSearchPodcast(Action):

    def name(self) -> Text:
        return "action_search_podcast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query = tracker.get_slot("search_query")
        result = search_podcast(query)[0]['attributes']
        title = result['title']
        website = result['orig-link']

        dispatcher.utter_message(response="utter_episode_search_result", title=title, website=website)

        return []

class ActionRecommendPodcast(Action):

    def name(self) -> Text:
        return "action_recommend_podcast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = recommend_podcast()[0]['attributes']
        title = result['title']
        website = result['website']
        dispatcher.utter_message(response="utter_podcast_recommendation", title=title, website=website)

        return []

class ActionLastUpdatedPodcast(Action):

    def name(self) -> Text:
        return "action_last_updated_podcast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = last_updated_podcast()[0]['attributes']
        title = result['title']
        website = result['website']
        dispatcher.utter_message(response="utter_last_updated_podcast_response", title=title, website=website)

        return []

class ActionMostSubscribedPodcast(Action):

    def name(self) -> Text:
        return "action_most_subscribed_podcast"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = most_subscribed_podcast()[0]['attributes']
        title = result['title']
        website = result['website']
        count = result['subscriptions-count']
        dispatcher.utter_message(response="utter_subscribed_podcast_response", title=title, website=website, count=count)

        return []

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


    