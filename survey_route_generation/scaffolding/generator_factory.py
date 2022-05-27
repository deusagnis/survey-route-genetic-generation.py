from config import settings


def tune_generator_factory(generator_factory):
    """
    Настроить фабрику генераторов маршрута из файла настроек.
    """
    # Размер начальной популяции
    generator_factory.population_size = settings.population_size
    # Доля выживших особей при отборе
    generator_factory.selection_rate = settings.selection_rate
    # Количество генотипов при размножении
    generator_factory.parents_count = settings.parents_count
    # Доля мутированных особей
    generator_factory.mutants_rate = settings.mutants_rate
    # Максимальное число циклов смены популяции
    generator_factory.max_lifecycles = settings.max_lifecycles
    # Тип выбора родительских генотипов при скрещивании: panmixia, inbreeding, outbreeding
    generator_factory.parents_choice_type = settings.parents_choice_type
    # Тип сравнения генотипов при группировке родителей методами аутбридинга и инбридинга: fitness, combination
    generator_factory.parents_similarity_type = settings.parents_similarity_type
    # Число мутаций в генотипе: доля или конкретное число
    generator_factory.mutation_swap_value = settings.mutation_swap_value
    # Тип числа мутаций: rate, value
    generator_factory.mutation_swap_type = settings.mutation_swap_type
    # Значимость сокращения длины маршрута при оценке приспособленности
    generator_factory.route_distance_weight = settings.route_distance_weight
    # Значимость увеличения плавности движения при оценке приспособленности
    generator_factory.route_turns_angle_weight = settings.route_turns_angle_weight
    # Значимость количества самопересечений маршрута при оценке приспособленности
    generator_factory.route_self_intersection_weight = settings.route_self_intersection_weight
    # Применять ли к генотипам правило "ближайших точек"
    generator_factory.repair_route_genotypes = settings.repair_route_genotypes
