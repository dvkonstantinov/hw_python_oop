from dataclasses import dataclass
from typing import Dict, Union, Type


@dataclass()
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вернуть сообщение."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {format(self.duration, ".3f")} ч.; '
                f'Дистанция: {format(self.distance, ".3f")} км; '
                f'Ср. скорость: {format(self.speed, ".3f")} км/ч; '
                f'Потрачено ккал: {format(self.calories, ".3f")}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

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
        raise NotImplementedError('Невозможно посчитать калории. Неверный '
                                  'тип тренировки')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    ratio_calories_1: float = 18
    ratio_calories_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        training_time_in_min = self.duration * Training.MIN_IN_HOUR
        calories = ((Running.ratio_calories_1 * self.get_mean_speed()
                     - Running.ratio_calories_2) * self.weight
                    / Training.M_IN_KM * training_time_in_min)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    ratio_calories_1: float = 0.035
    ratio_calories_2: float = 0.029

    def __init__(self, action, duration, weight, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        training_time_in_min = self.duration * Training.MIN_IN_HOUR
        calories = ((SportsWalking.ratio_calories_1 * self.weight
                     + (self.get_mean_speed() ** 2 // self.weight)
                     * SportsWalking.ratio_calories_2 * self.weight)
                    * training_time_in_min)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self, action, duration, weight,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
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
        ratio_calories_1: float = 1.1
        ratio_calories_2: float = 2
        calories = ((self.get_mean_speed() + ratio_calories_1)
                    * ratio_calories_2 * self.weight)
        return calories


def read_package(training_type: str, training_data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    # Проверка правильности введенного типа тренировки
    if training_type not in ['RUN', 'WLK', 'SWM']:
        raise TypeError("Введен неверный тип тренировки")
    workout_dict: Dict[str, Type[Union[Running,
                                       Swimming,
                                       SportsWalking]]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming}
    name_of_class = workout_dict[training_type]
    return name_of_class(*training_data)


def main(training_object: Training) -> None:
    """Главная функция."""
    info: InfoMessage = Training.show_training_info(training_object)
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
