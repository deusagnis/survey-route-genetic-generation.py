"""
Структура данных, описывающая используемые параметры БПЛА
"""


class VehicleData:
    def __init__(self, vision_width):
        """
        :param vision_width: Ширина приборного "зрения"
        """
        self.vision_width = vision_width
