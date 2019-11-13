from py2neo import Graph
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionChargingPointInCity(Action):

    def name(self):
        return "action_charging_point_in_city"

    @staticmethod
    def count_charging_point_in_city(graph, city_name):
        return graph.run("MATCH (City {name:{cityName}})<-[:IN*]-(p:ChargingPoint) RETURN count(p)",
                         cityName=city_name).evaluate()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city_name = tracker.get_slot('city')

        if city_name:
            graph = Graph(password='abcd')
            count = self.count_charging_point_in_city(graph, city_name)

            dispatcher.utter_message(f"Il y a {count} bornes de recharge à {city_name}.")
        else:
            dispatcher.utter_message(f"Pour quel ville voulez-vous connaitre les bornes de recharge?")

        return []


class ActionChargingPointNearMetro(Action):

    def name(self):
        return "action_charging_point_near_metro"

    @staticmethod
    def count_charging_point_near_metro(graph, metro_name):
        # Charging parks at less than 500m of Pie-IX metro station
        return graph.run("MATCH (MetroStation {name:{metroName}})-[n:NEARBY]-(p:ChargingPark) WHERE n.distance_km < 0.5 RETURN count(p)",
                         metroName=metro_name).evaluate()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        metro_name = tracker.get_slot('metro')

        if metro_name:
            graph = Graph(password='abcd')
            count = self.count_charging_point_near_metro(graph, metro_name)

            dispatcher.utter_message(f"Il y a {count} endroits à moins de 500m du métro {metro_name}.")
            # dispatcher.utter_message(f"Les bornes pres du metro <{metro_name}> sont:")
        else:
            dispatcher.utter_message(f"Pour quel métro voulez-vous connaitre les bornes de recharge?")

        return []


class ActionChargingPointInQuartier(Action):

    def name(self):
        return "action_charging_point_in_quartier"

    @staticmethod
    def count_charging_point_in_quartier(graph, quartier_name):
        return graph.run("MATCH (QuartierMontreal {name:{quartierName}})<-[:IN*]-(p:ChargingPoint) RETURN count(p)",
                         quartierName=quartier_name).evaluate()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        quartier_name = tracker.get_slot('quartier')

        if quartier_name:
            graph = Graph(password='abcd')
            count = self.count_charging_point_in_quartier(graph, quartier_name)

            dispatcher.utter_message(f"Il y a {count} bornes dans le quartier {quartier_name}.")
        else:
            dispatcher.utter_message(f"Pour quel quartier de Montréal voulez-vous connaitre les bornes de recharge?")

        return []
