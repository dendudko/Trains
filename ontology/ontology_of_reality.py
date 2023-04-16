from ontology.objects import *


class OntologyOfReality:
    def __init__(self):
        self.trains = []
        self.routes = []

    def add_train(self, train: Train):
        self.trains.append(train)

    def add_route(self, route: Route):
        self.routes.append(route)
