class VehicleData:
    def __init__(self, turn_rate, average_speed, vision_width):
        """
        :param turn_rate: На сколько градусов БПЛА может повернуть на 1 скорости в м/с
        :param average_speed: Средняя предполагаемая скорость БПЛА (Крейсерская?)
        :param vision_width: Ширина приборного "зрения"
        """
        self.turn_rate = turn_rate
        self.average_speed = average_speed
        self.vision_width = vision_width
