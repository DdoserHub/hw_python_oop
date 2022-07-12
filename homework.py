from dataclasses import dataclass
from typing import List


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Информационное сообщение о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    SECONDS: int = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод класса не переопределен')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    MULTIPLIER: int = 18
    SUBTRAHEND: int = 20

    def get_spent_calories(self) -> float:
        return ((self.MULTIPLIER * self.get_mean_speed()
                - self.SUBTRAHEND) * self.weight
                / self.M_IN_KM * self.duration * self.SECONDS)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    MULTIPLIER_FOR_WEIGHT: float = 0.035
    MULTIPLIER_FOR_QUOTIENT: float = 0.029

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        return ((self.MULTIPLIER_FOR_WEIGHT * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.MULTIPLIER_FOR_QUOTIENT * self.weight)
                * self.duration * self.SECONDS)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SUMMAND: float = 1.1

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.SUMMAND) * 2 * self.weight


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts: [str, Training] = {'SWM': Swimming,
                                 'RUN': Running,
                                 'WLK': SportsWalking}
    if workout_type in workouts:
        return workouts[workout_type](*data)
    raise ValueError('Значение переменной workout_type неизвестно')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:

        training = read_package(workout_type, data)
        main(training)
