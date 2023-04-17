import random
import pandas
import xlsxwriter
from ontology.objects import *


class Schedule:
    def __init__(self, trains: [Train], routes: [Route], cities):
        self.trains = trains
        self.routes = routes
        self.cities = cities

        self.train_routes = []
        self.df = pandas.DataFrame

        self.time_list = []
        start_date = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + datetime.timedelta(weeks=1)
        while start_date < end_date:
            self.time_list.append(start_date)
            start_date += datetime.timedelta(minutes=30)

        self.cities_times = {}
        for city in self.cities:
            self.cities_times[city] = self.time_list

    def generate_schedule(self):
        for train in self.trains:
            # Выбираем допустимые по дальности маршруты
            routes = [route_i for route_i in self.routes if
                      train.train_type.train_distance_min <= route_i.distance <= train.train_distance]

            if len(routes) == 0:
                return f'Ошибка связи области знаний и области действительности!\n' \
                       f'Для поезда {train.train_name} нет ни одного допустимого маршрута!'
            local_cities_times = {}
            for city in set(route.start_city for route in routes).union(set(route.end_city for route in routes)):
                local_cities_times[city] = self.time_list

            for i in range(len(local_cities_times)):
                for city, city_times in local_cities_times.items():
                    if len(self.train_routes) != 0 and self.train_routes[-1].train.train_name == train.train_name:
                        start_city = self.train_routes[-1].route.end_city
                        routes = [route_i for route_i in self.routes if
                                  train.train_type.train_distance_min <= route_i.distance <= train.train_distance and
                                  route_i.start_city == start_city]
                    potential_routes = []
                    for city_time in city_times:
                        if len(routes) == 0:
                            break
                        route_index = random.randint(0, len(routes) - 1)
                        potential_routes.append(TrainRoute(train, routes[route_index], city_time))

                    if len(self.train_routes) == 0:
                        self.train_routes.append(potential_routes[0])
                        try:
                            self.cities_times[potential_routes[0].route.start_city].remove(potential_routes[0].start_time)
                            self.cities_times[potential_routes[0].route.end_city].remove(potential_routes[0].end_time)
                        except:
                            pass
                    else:
                        can_append = True
                        for potential_route in potential_routes:
                            for train_route in self.train_routes:
                                if train_route.train == train and train_route.end_time < potential_route.start_time and train_route.route.end_city == potential_route.route.start_city:
                                    can_append = True
                                elif train not in [train_route.train for train_route in self.train_routes]:
                                    can_append = True
                                else:
                                    can_append = False
                            if can_append:
                                self.train_routes.append(potential_route)
                                try:
                                    self.cities_times[potential_route.route.start_city].remove(potential_route.start_time)
                                    self.cities_times[potential_route.route.end_city].remove(potential_route.end_time)
                                except:
                                    pass

        self.df = pandas.DataFrame(
            columns=['Город отправления', 'Город прибытия', 'Время отправления', 'Время прибытия', 'Поезд',
                     'Тип поезда', 'Дальность следования', 'Дальность маршрута', 'Скорость'])
        for train_route in self.train_routes:
            self.df.loc[len(self.df)] = [train_route.route.start_city, train_route.route.end_city,
                                         train_route.start_time.strftime("%m-%d %H:%M"),
                                         train_route.end_time.strftime("%m-%d %H:%M"),
                                         train_route.train.train_name, train_route.train.train_type.train_type_name,
                                         str(train_route.train.train_type.train_distance_min) + '-' + str(
                                             train_route.train.train_distance),
                                         train_route.route.distance, train_route.train.train_speed]
        with pandas.ExcelWriter('schedule.xlsx', engine='xlsxwriter') as writer:
            self.df.to_excel(writer, sheet_name='Расписание 1', index=False)
            # Получаем объект workbook и worksheet
            worksheet = writer.sheets['Расписание 1']
            # Установка максимальной ширины колонки
            for i, col in enumerate(self.df.columns):
                # Для каждой колонки устанавливаем ширину, которая соответствует максимальной длине в строке
                max_width = max(self.df[col].astype(str).map(len).max(), len(col)) + 1
                worksheet.set_column(i, i, max_width)

            self.df = self.df.sort_values(by=['Город отправления', 'Время отправления'])
            self.df.to_excel(writer, sheet_name='Расписание 2', index=False)
            # Получаем объект workbook и worksheet
            worksheet = writer.sheets['Расписание 2']
            # Установка максимальной ширины колонки
            for i, col in enumerate(self.df.columns):
                # Для каждой колонки устанавливаем ширину, которая соответствует максимальной длине в строке
                max_width = max(self.df[col].astype(str).map(len).max(), len(col)) + 1
                worksheet.set_column(i, i, max_width)

        return self.df
