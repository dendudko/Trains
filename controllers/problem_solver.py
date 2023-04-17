import flask
from flask import render_template

from app import app
from ontology.main import *


@app.route('/problem_solver', methods=['get'])
def problem_solver():
    # refill()
    with open('ontology_of_knowledge.pickle', 'rb') as load_file:
        ontology_of_knowledge = pickle.load(load_file)
    with open('ontology_of_reality.pickle', 'rb') as load_file:
        ontology_of_reality = pickle.load(load_file)

    result = call_gen_schedule(ontology_of_knowledge, ontology_of_reality)

    # Строка ошибок (если пустая, отдаст таблицу, иначе выведет ошибки)
    errors = ''
    if type(result) == str:
        errors = result
        errors = flask.Markup(errors.replace('\n', '<br>'))
        result = pandas.DataFrame()
        result1 = pandas.DataFrame()
    else:
        result1 = result.copy()
        result1 = result1.sort_values(by=['Город отправления', 'Время отправления'])
        result1 = result1.reset_index(drop=True)

    html = render_template(
        'problem_solver.html',
        errors=errors,
        df=result,
        df1=result1,
        len=len,
        int=int)
    return html
