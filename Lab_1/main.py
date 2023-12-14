"""
Лабораторная работа №4 по дисциплине "Логические основы интеллектуальных систем"
Выполнена студентами группы №121702  Шакиным И.В., Шершенем К.А., Промчуком Д.В.
Файл содержит пример реализации алгоритма импликации Лукасевича
Дата: 25.09.2023
"""
from test import *

def main ():
    parcel_to_rule_list = []
    used_rules = []
    external_counter = 0
    input_information_dict, input_values_dict = input_transformation()
    #print(input_information_dict)
    #print(input_values_dict)
    parcel_information_dict, parcel_values_dict = parcel_transformation(external_counter)
    #print(parcel_information_dict)
    #print(parcel_values_dict)
    array_of_operations = operation_reader()
    #print(array_of_operations)
    matrix_dict = lukasiewicz_matrix_formation(input_information_dict, array_of_operations)
    #print(matrix_dict)

    new_matrix_dict, parcel_to_rule_list = t_norm(input_information_dict, input_values_dict, matrix_dict, parcel_information_dict, parcel_values_dict, used_rules, parcel_to_rule_list)

    result = strait_output(new_matrix_dict, input_information_dict, input_values_dict, parcel_information_dict, external_counter, parcel_to_rule_list)

    while result>0:
        external_counter+=1
        parcel_information_dict, parcel_values_dict = parcel_transformation(external_counter)
        new_matrix_dict, parcel_to_rule_list = t_norm(input_information_dict, input_values_dict, matrix_dict,
                                                      parcel_information_dict, parcel_values_dict, used_rules,
                                                      parcel_to_rule_list)
        result = strait_output(new_matrix_dict, input_information_dict, input_values_dict, parcel_information_dict, external_counter, parcel_to_rule_list)


if __name__ == "__main__":
    main()
