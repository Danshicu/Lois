"""
Лабораторная работа №4 по дисциплине "Логические основы интеллектуальных систем"
Выполнена студентами группы №121702  Шакиным И.В., Шершенем К.А., Промчуком Д.В.
Файл содержит пример реализации алгоритма импликации Лукасевича
Дата: 25.09.2023
"""
from test import *

def main ():
    input_information_dict = input_transformation()
    parcel_information_dict = parcel_transformation(0)
    array_of_operations = operation_reader()

    matrix_dict = lukasiewicz_matrix_formation(input_information_dict, array_of_operations)
    print(matrix_dict)
    new_matrix_dict = t_norm(input_information_dict, matrix_dict, parcel_information_dict)
    print(new_matrix_dict)

    external_counter = 0

    result = strait_output(new_matrix_dict, input_information_dict, parcel_information_dict, external_counter)

    while result>0:
        external_counter+=1
        parcel_information_dict = parcel_transformation(external_counter)
        print(parcel_information_dict)
        new_matrix_dict = t_norm(input_information_dict, matrix_dict, parcel_information_dict)
        print(new_matrix_dict)
        result = strait_output(new_matrix_dict, input_information_dict, parcel_information_dict, external_counter)
        print(result)


if __name__ == "__main__":
    main()
