from ontology.objects import *


class OntologyOfKnowledge:
    def __init__(self):
        self.train_types = []
        self.cities = []
        self.routes = []

    def add_city(self, city):
        self.cities.append(city)

    def add_route(self, route: Route):
        self.routes.append(route)

    def add_train_type(self, train_type: TrainType):
        self.train_types.append(train_type)
