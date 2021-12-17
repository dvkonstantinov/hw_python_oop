class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = format(duration, '.3f')
        self.distance = format(distance, '.3f')
        self.speed = format(speed, '.3f')
        self.calories = format(calories, '.3f')

    def get_message(self):
        """Вернуть сообщение."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_in_km = self.action * Training.LEN_STEP / Training.M_IN_KM
        return distance_in_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action, duration, weight):
        super(Running, self).__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        training_time_in_min = self.duration * 60
        ratio_calories_1 = 18
        ratio_calories_2 = 20
        calories = ((ratio_calories_1 * self.get_mean_speed()
                     - ratio_calories_2) * self.weight
                    / Training.M_IN_KM * training_time_in_min)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height):
        super(SportsWalking, self).__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        ratio_calories_1 = 0.035
        ratio_calories_2 = 0.029
        training_time_in_min = self.duration * 60
        calories = ((ratio_calories_1 * self.weight
                     + (self.get_mean_speed() ** 2 // self.weight)
                     * ratio_calories_2 * self.weight) * training_time_in_min)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super(Swimming, self).__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_in_km = self.action * self.LEN_STEP / Training.M_IN_KM
        return distance_in_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool * self.count_pool / Training.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        ratio_calories_1 = 1.1
        ratio_calories_2 = 2
        calories = ((self.get_mean_speed() + ratio_calories_1)
                    * ratio_calories_2 * self.weight)
        return calories


def read_package(training_type: str, training_data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict = {'RUN': Running, 'WLK': SportsWalking, 'SWM': Swimming}
    name_of_class = workout_dict[training_type]
    return name_of_class(*training_data)


def main(training_object: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training_object)
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
