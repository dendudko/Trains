import pandas

from ontology.objects import *
from ontology.ontology_of_knowledge import OntologyOfKnowledge
from ontology.ontology_of_reality import OntologyOfReality
from ontology.schedule import Schedule
import pickle


def Check(ook: OntologyOfKnowledge, oor: OntologyOfReality):
    # Проверяем область знаний
    check_result = ''
    if len(ook.cities) < 2:
        check_result += f'Ошибка в области знаний! Количество городов: {len(ook.cities)} < 2.\n'
    else:
        for i in range(len(ook.cities) - 1):
            for j in range(i + 1, len(ook.cities)):
                if ook.cities[i] == ook.cities[j]:
                    check_result += f'Ошибка в области знаний! Город {ook.cities[i]} дублируется.\n'

    if len(ook.routes) == 0:
        check_result += f'Ошибка в области знаний! Маршруты не заданы!\n'
    for i in range(len(ook.routes) - 1):
        for j in range(i + 1, len(ook.routes)):
            if ook.routes[i].start_city == ook.routes[j].start_city \
                    and ook.routes[i].end_city == ook.routes[j].end_city \
                    and ook.routes[i].distance == ook.routes[j].distance:
                check_result += f'Ошибка в области знаний! Марушрут {ook.routes[i].start_city} -> ' \
                                f'{ook.routes[i].end_city} {ook.routes[i].distance} дублируется.\n'
    for route in ook.routes:
        if route.start_city not in ook.cities:
            check_result += f'Ошибка в области знаний! Город {route.start_city} не входит в множество городов: {ook.cities} ' \
                            f'(маршрут {route.start_city} -> {route.end_city} {route.distance}).\n'
        if route.end_city not in ook.cities:
            check_result += f'Ошибка в области знаний! Город {route.end_city} не входит в множество городов: {ook.cities} ' \
                            f'(маршрут {route.start_city} -> {route.end_city} {route.distance}).\n'
        if route.start_city == route.end_city:
            check_result += f'Ошибка в области знаний! Начало маршрута = конец маршрута ({route.start_city} = {route.end_city}) ' \
                            f'(маршрут {route.start_city} -> {route.end_city} {route.distance}).\n'
        if route.distance == 0:
            check_result += f'Ошибка в области знаний! Для маршрута {route.start_city} -> {route.end_city} дальность маршрута = 0.\n'

    if len(ook.routes) == 0:
        check_result += f'Ошибка в области знаний! Типы поездов не заданы!\n'
    for i in range(len(ook.train_types) - 1):
        for j in range(i + 1, len(ook.train_types)):
            if ook.train_types[i].train_type_name == ook.train_types[j].train_type_name \
                    or ook.train_types[i].train_distance_min == ook.train_types[j].train_distance_min \
                    and ook.train_types[i].train_distance_max == ook.train_types[j].train_distance_max \
                    and ook.train_types[i].train_speed_min == ook.train_types[j].train_speed_min \
                    and ook.train_types[i].train_speed_max == ook.train_types[j].train_speed_max:
                check_result += f'Ошибка в области знаний! Тип поезда "{ook.train_types[i].train_type_name}" дублируется.\n'
    for train_type in ook.train_types:
        if train_type.train_speed_min > train_type.train_speed_max:
            check_result += f'Ошибка в области знаний! Для типа поезда {train_type}' \
                            f' минимальная скорость движения > максимальной скорости движения:' \
                            f' {train_type.train_speed_min} > {train_type.train_speed_max}.\n'
        if train_type.train_distance_min > train_type.train_distance_max:
            check_result += f'Ошибка в области знаний! Для типа поезда {train_type}' \
                            f' минимальная дальность следования > максимальной дальности следования:' \
                            f' {train_type.train_distance_min} > {train_type.train_distance_max}.\n'

    # Проверяем область действительности
    if len(oor.trains) == 0:
        check_result += f'Ошибка в области действительности! Поезда не заданы.\n'

    if len(oor.routes) == 0:
        check_result += f'Ошибка в области действительности! Маршруты не заданы.\n'
    for i in range(len(oor.routes) - 1):
        for j in range(i + 1, len(oor.routes)):
            if oor.routes[i].start_city == oor.routes[j].start_city \
                    and oor.routes[i].end_city == oor.routes[j].end_city \
                    and oor.routes[i].distance == oor.routes[j].distance:
                check_result += f'Ошибка в области действительности! Марушрут {oor.routes[i].start_city} -> ' \
                                f'{oor.routes[i].end_city} {oor.routes[i].distance} дублируется.\n'

    for i in range(len(oor.trains) - 1):
        for j in range(i + 1, len(oor.trains)):
            if oor.trains[i].train_name == oor.trains[j].train_name:
                check_result += f'Ошибка в области действительности! Поезд {oor.trains[i].train_name} дублируется.\n'

    for train in oor.trains:
        if train.train_distance < train.train_type.train_distance_min:
            check_result += f'Ошибка в области действительности! Для поезда {train.train_name}' \
                            f' дальность следования < минимальной дальности следования для заданного типа ' \
                            f'({train.train_type.train_type_name}): {train.train_distance} < {train.train_type.train_distance_min}.\n'
        if train.train_distance > train.train_type.train_distance_max:
            check_result += f'Ошибка в области действительности! Для поезда {train.train_name}' \
                            f' дальность следования > максимальной дальности следования для заданного типа ' \
                            f'({train.train_type.train_type_name}): {train.train_distance} > {train.train_type.train_distance_max}.\n'
        if train.train_speed < train.train_type.train_speed_min:
            check_result += f'Ошибка в области действительности! Для поезда {train.train_name}' \
                            f' дальность следования < минимальной скорости движения для заданного типа ' \
                            f'({train.train_type.train_type_name}): {train.train_speed} < {train.train_type.train_speed_min}.\n'
        if train.train_speed > train.train_type.train_speed_max:
            check_result += f'Ошибка в области действительности! Для поезда {train.train_name}' \
                            f' скорость движения > максимальной скорости движения для заданного типа ' \
                            f'({train.train_type.train_type_name}): {train.train_speed} > {train.train_type.train_speed_max}.\n'

    # Проверяем связи
    for train in oor.trains:
        if train.train_type.train_type_name not in [train_type.train_type_name for train_type in ook.train_types]:
            check_result += f'Ошибка связи области знаний и области действительности! Неизвестный тип {train.train_type.train_type_name}' \
                            f' для поезда {train.train_name}.\n'

    if check_result:
        return check_result
    else:
        return 0


def refill():
    ontology_of_knowledge = OntologyOfKnowledge()
    ontology_of_reality = OntologyOfReality()

    ontology_of_knowledge.add_train_type(TrainType('скоростной поезд дальнего следования', 700, 20000, 91, 300))
    ontology_of_knowledge.add_train_type(TrainType('скоростной поезд местного сообщения', 150, 700, 91, 300))
    ontology_of_knowledge.add_train_type(TrainType('скоростной поезд пригородного сообщения', 0, 150, 91, 300))
    ontology_of_knowledge.add_train_type(TrainType('скорый поезд дальнего следования', 700, 20000, 50, 91))
    ontology_of_knowledge.add_train_type(TrainType('скорый поезд местного сообщения', 150, 700, 50, 91))
    ontology_of_knowledge.add_train_type(TrainType('скорый поезд пригородного  сообщения', 0, 150, 50, 91))
    ontology_of_knowledge.add_train_type(TrainType('обычный пассажирский поезд дальнего следования', 700, 20000, 0, 50))
    ontology_of_knowledge.add_train_type(TrainType('обычный пассажирский поезд местного сообщения', 150, 700, 0, 50))
    ontology_of_knowledge.add_train_type(TrainType('обычный пассажирский поезд пригородного сообщения', 0, 150, 0, 50))

    ontology_of_knowledge.add_city('Владивосток')
    ontology_of_knowledge.add_city('Находка')
    ontology_of_knowledge.add_city('Хабаровск')
    ontology_of_knowledge.add_city('Москва')
    ontology_of_knowledge.add_city('Артем')

    ontology_of_knowledge.add_route(Route('Находка', 'Владивосток', 200))
    ontology_of_knowledge.add_route(Route('Находка', 'Хабаровск', 900))
    ontology_of_knowledge.add_route(Route('Владивосток', 'Москва', 7000))
    ontology_of_knowledge.add_route(Route('Владивосток', 'Хабаровск', 730))
    ontology_of_knowledge.add_route(Route('Владивосток', 'Артем', 40))
    ontology_of_knowledge.add_route(Route('Хабаровск', 'Москва', 6300))

    ontology_of_knowledge.add_route(Route('Владивосток', 'Находка', 200))
    ontology_of_knowledge.add_route(Route('Хабаровск', 'Находка', 900))
    ontology_of_knowledge.add_route(Route('Москва', 'Владивосток', 7000))
    ontology_of_knowledge.add_route(Route('Хабаровск', 'Владивосток', 730))
    ontology_of_knowledge.add_route(Route('Артем', 'Владивосток', 40))
    ontology_of_knowledge.add_route(Route('Москва', 'Хабаровск', 6300))

    ontology_of_reality.routes = ontology_of_knowledge.routes

    ontology_of_reality.add_train(Train('t000', ontology_of_knowledge.train_types[0], 300, 8000))
    ontology_of_reality.add_train(Train('t001', ontology_of_knowledge.train_types[0], 200, 6400))
    ontology_of_reality.add_train(Train('t002', ontology_of_knowledge.train_types[1], 200, 500))
    ontology_of_reality.add_train(Train('t003', ontology_of_knowledge.train_types[2], 200, 130))
    ontology_of_reality.add_train(Train('t004', ontology_of_knowledge.train_types[2], 250, 130))
    ontology_of_reality.add_train(Train('t005', ontology_of_knowledge.train_types[3], 85, 740))
    ontology_of_reality.add_train(Train('t006', ontology_of_knowledge.train_types[4], 89, 200))
    ontology_of_reality.add_train(Train('t007', ontology_of_knowledge.train_types[5], 90, 130))
    ontology_of_reality.add_train(Train('t008', ontology_of_knowledge.train_types[6], 50, 9000))
    ontology_of_reality.add_train(Train('t009', ontology_of_knowledge.train_types[7], 45, 250))
    ontology_of_reality.add_train(Train('t010', ontology_of_knowledge.train_types[8], 45, 130))

    dump(ontology_of_knowledge, ontology_of_reality)


def dump(ontology_of_knowledge=None, ontology_of_reality=None, schedule=None):
    if ontology_of_knowledge is not None:
        with open('ontology_of_knowledge.pickle', 'wb') as dump_file:
            pickle.dump(ontology_of_knowledge, dump_file, protocol=pickle.HIGHEST_PROTOCOL)
    if ontology_of_reality is not None:
        with open('ontology_of_reality.pickle', 'wb') as dump_file:
            pickle.dump(ontology_of_reality, dump_file, protocol=pickle.HIGHEST_PROTOCOL)
    if schedule is not None:
        with open('schedule.pickle', 'wb') as dump_file:
            pickle.dump(schedule, dump_file, protocol=pickle.HIGHEST_PROTOCOL)


def call_gen_schedule(ontology_of_knowledge: OntologyOfKnowledge, ontology_of_reality: OntologyOfReality):
    check = Check(ontology_of_knowledge, ontology_of_reality)
    if check == 0:
        schedule = Schedule(ontology_of_reality.trains, ontology_of_reality.routes, ontology_of_knowledge.cities)
        schedule_result = schedule.generate_schedule()
        # if type(schedule_result) != pandas.DataFrame:
        #     return schedule_result
        # with open('schedule.pickle', 'wb') as dump_file:
        #     pickle.dump(schedule, dump_file, protocol=pickle.HIGHEST_PROTOCOL)
        return schedule_result
    else:
        return check
