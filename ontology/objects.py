import datetime


class TrainType:
    def __init__(self, train_type_name, train_distance_min, train_distance_max, train_speed_min, train_speed_max):
        self.train_type_name = train_type_name
        self.train_distance_min = train_distance_min
        self.train_distance_max = train_distance_max
        self.train_speed_min = train_speed_min
        self.train_speed_max = train_speed_max


class Train:
    def __init__(self, train_name, train_type: TrainType, train_speed, train_distance):
        self.train_name = train_name
        self.train_type = train_type
        self.train_speed = train_speed
        self.train_distance = train_distance


class Route:
    def __init__(self, start_city, end_city, distance):
        self.start_city = start_city
        self.end_city = end_city
        self.distance = distance


class TrainRoute:
    def __init__(self, train: Train, route: Route, start_time: datetime):
        self.train = train
        self.route = route
        self.start_time = start_time
        self.end_time = self.start_time + datetime.timedelta(hours=self.route.distance / self.train.train_speed)
