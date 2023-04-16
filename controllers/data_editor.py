import flask
from flask import render_template, request

from app import app
from ontology.main import *


@app.route('/data_editor', methods=['get'])
def data_editor():
    # refill()
    with open('ontology_of_knowledge.pickle', 'rb') as load_file:
        ontology_of_knowledge = pickle.load(load_file)
    with open('ontology_of_reality.pickle', 'rb') as load_file:
        ontology_of_reality = pickle.load(load_file)

    all_routes = ontology_of_knowledge.routes
    train_types = ontology_of_knowledge.train_types
    trains = ontology_of_reality.trains
    current_routes = ontology_of_reality.routes

    if request.values.get('addTravelTrip'):
        ontology_of_reality.add_route(ontology_of_knowledge.routes[int(request.values.get('route'))])
        dump(ontology_of_reality=ontology_of_reality)
        return flask.redirect(flask.url_for('data_editor'))

    if request.values.get('delTravelTrip'):
        del_route = ontology_of_knowledge.routes[int(request.values.get('route'))]
        ontology_of_reality.routes = [route for route in ontology_of_reality.routes
                                      if not (route.start_city == del_route.start_city and
                                              route.end_city == del_route.end_city and
                                              route.distance == del_route.distance)]
        dump(ontology_of_reality=ontology_of_reality)
        return flask.redirect(flask.url_for('data_editor'))

    if request.values.get('addTrain'):
        ontology_of_reality.add_train(Train(request.values.get('train-number'),
                                            ontology_of_knowledge.train_types[int(request.values.get('train-type'))],
                                            int(request.values.get('speed')),
                                            int(request.values.get('distance'))))
        dump(ontology_of_reality=ontology_of_reality)
        return flask.redirect(flask.url_for('data_editor'))

    if request.values.get('delTrain'):
        ontology_of_reality.trains = [train for train in ontology_of_reality.trains
                                      if not (train.train_name == request.values.get('train-number') and
                                              train.train_type.train_type_name == ontology_of_knowledge.train_types[
                                                  int(request.values.get('train-type'))].train_type_name and
                                              train.train_distance == int(request.values.get('distance')) and
                                              train.train_speed == int(request.values.get('speed')))]
        dump(ontology_of_reality=ontology_of_reality)
        return flask.redirect(flask.url_for('data_editor'))

    html = render_template(
        'data_editor.html',
        len=len,
        int=int,
        train_types=train_types,
        all_routes=all_routes,
        trains=trains,
        current_routes=current_routes
    )

    return html
