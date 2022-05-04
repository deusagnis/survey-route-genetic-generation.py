"""
Структура данных, описывающая параметры обследовательской миссии
"""


class MissionSettings:
    def __init__(self, start_point, end_point):
        """
        :param start_point: Точка начала полётной миссии
        :param end_point: Точка завершения полётной миссии
        """
        self.start_point = start_point
        self.end_point = end_point
