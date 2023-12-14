import re
import random



def input_transformation():
    input_information_dict = {}
    values_dict = {}
    with open("./Inputs/input.txt", 'r') as file:
        lines = file.readlines()

    for line in lines:
        letter = line.split('=')[0]
        array_of_variable_numbers = []
        equation = line.split('=')[1]
        pattern = re.compile(r'<[a-z]\d+?,\d.\d>')
        matches = pattern.findall(equation)
        values_array = []

        for match in matches:
            variable = match[1]
            string = match.split(',')[0][1:]
            values_array.append(string)
            number = float(match.split(',')[1][:-1])
            if variable not in array_of_variable_numbers:
                array_of_variable_numbers.append(variable)
            array_of_variable_numbers.append(number)
        input_information_dict[letter] = array_of_variable_numbers
        values_dict[letter] = values_array

    return input_information_dict, values_dict


def operation_reader():

    with open("./Inputs/operation.txt", 'r') as file:

        array_of_operations = file.readlines()
        for index, value in enumerate(array_of_operations):
            if '\n' in value:
                array_of_operations[index] = value.strip().split('~>')

    return array_of_operations


def parcel_transformation(level):
    parcel_information_dict = {}
    values_dict = {}
    with open("./Inputs/parcel.txt", 'r') as file:
        lines = file.readlines()

    for line in lines:
        if get_spaces_count(line) != level:
            continue
        letter = line.split('=')[0]
        array_of_variable_numbers = []

        equation = line.split('=')[1]
        pattern = re.compile(r'<[a-z]\d+?,\d.\d>')
        matches = pattern.findall(equation)
        values_array = []

        for match in matches:
            variable = match[1]
            string = match.split(',')[0][1:]
            values_array.append(string)
            number = float(match.split(',')[1][:-1])
            if variable not in array_of_variable_numbers:
                array_of_variable_numbers.append(variable)
            array_of_variable_numbers.append(number)
        parcel_information_dict[letter] = array_of_variable_numbers
        values_dict[letter] = values_array

    return parcel_information_dict, values_dict


def get_spaces_count(input):
    count = 0
    for char in input:
        if char.isspace():
            count += 1
        elif char.isalpha():
            break  # Прерывает цикл при обнаружении первой буквы
    return count

def lukasiewicz_matrix_formation(input_information_dict, array_of_operations):

    matrix_dict = {}

    #Выбираем в цикле операцию
    for operation in array_of_operations:

        matrix = []

        #Получаем массивы из словаря для импликации Лукасевича
        first_param = operation[0]
        second_param = operation[1]
        first_array = input_information_dict[operation[0]][1:]
        second_array = input_information_dict[operation[1]][1:]

        for external_element in first_array:
            row_elements = []

            for internal_element in second_array:

                result = min(1, 1 - external_element + internal_element)
                result = round(float(result), 1)
                row_elements.append(result)

            matrix.append(row_elements)

        matrix_dict[f"{first_param}{second_param}"] = matrix

    return matrix_dict


def t_norm(input_information_dict, input_values_dict, matrix_dict, parcel_information_dict, parcel_values_dict, used_rules, parcel_to_rule_list):

    matrix_keys = list(matrix_dict.keys())
    parcel_keys = list(parcel_information_dict.keys())
    #print(matrix_keys)
    #print(parcel_keys)
    new_matrix_dict = {}

    for matrix_key in matrix_keys:
        if matrix_key in used_rules:
            continue
        pattern = re.compile(r'[A-Z]\d+|[A-Z]')
        matches = pattern.findall(matrix_key)
        first_param = matches[0]
        current_matrix = matrix_dict[matrix_key]

        param_info = input_information_dict[first_param]
        necessary_variable = param_info[0]

        necessary_parcels = []

        for parcel_key in parcel_keys:
            parcel_info = parcel_information_dict[parcel_key]
            necessary_parcel_variable = parcel_info[0]

            if necessary_variable == necessary_parcel_variable:
                if input_values_dict[first_param] == parcel_values_dict[parcel_key]:
                    necessary_parcels.append(parcel_info[1:])
                    parcel_to_rule_list.append(f"{parcel_key}+{matrix_key}")


        #Пробегаемся по всем подходящим посылкам
        for parcel in necessary_parcels:
            new_matrix = []

            for parcel_element_id, parcel_element in enumerate(parcel):

                current_row = current_matrix[parcel_element_id]

                new_row = []

                for matrix_element in current_row:
                    result = max(0, parcel_element + matrix_element - 1)
                    result = round(float(result), 1)
                    new_row.append(result)

                new_matrix.append(new_row)

            used_rules.append(matrix_key)
            new_matrix_dict[matrix_key] = new_matrix

    return new_matrix_dict, parcel_to_rule_list


def strait_output(new_matrix_dict, input_information_dict, input_values_dict, parcel_information_dict, external_counter, parcel_to_rule_list):

    parcel_to_rule_counter=0
    new_parcels_count =0
    alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    matrix_keys = list(new_matrix_dict.keys())
    parcel_keys = list(parcel_information_dict.keys())
    checked_keys = list(parcel_keys)
    #print(matrix_keys)

    #Пробегаемся по всем матрицам
    for matrix_key in matrix_keys:
        try:
            current_matrix = new_matrix_dict[matrix_key]
            columns = [[row[i] for row in current_matrix] for i in range(len(current_matrix[0]))]

            direct_conclusive = []
            for column in columns:
                direct_conclusive.append(max(column))

            pattern = re.compile(r'[A-Z]\d+|[A-Z]')
            matches = pattern.findall(matrix_key)
            second_param = matches[1]
            param_info = input_information_dict[second_param]
            necessary_variable = param_info[0]

            letter = parcel_to_rule_list[parcel_to_rule_counter].split('+')[0]
            subletter = random.choice(alphabet)
            while subletter in checked_keys:
                subletter = random.choice(alphabet)
            checked_keys.append(subletter)

            amount_of_elements = len(new_matrix_dict[matrix_key])
            counter = 0

            array_of_elements = []
            for counter in range(0, amount_of_elements):
                #print(new_matrix_dict[matrix_key][counter])
                element = f"<{input_values_dict[second_param][counter]},{direct_conclusive[counter]}>"
                array_of_elements.append(element)

            equation = '{' + ','.join(array_of_elements) + '}'
            result = f"{subletter}{external_counter+1}={equation}"
            line = f"\n{' '*(external_counter+1)}{result}"
            pattern = re.compile(r'[A-Z]\d+|[A-Z]')
            matches = pattern.findall(parcel_to_rule_list[parcel_to_rule_counter].split('+')[1])
            print(f"{letter} : {matches[0]}~>{matches[1]} |- {result}")
            parcel_to_rule_counter+=1
            with open('./Inputs/parcel.txt', 'a') as file:

                file.write(line)
                new_parcels_count+=1

        except:
            return 0
        #finally:
            #return new_parcels_count
    parcel_to_rule_list.clear()
    return new_parcels_count




'''
input_information_dict = input_transformation()
parcel_information_dict = parcel_transformation()
array_of_operations = operation_reader()



matrix_dict = lukasiewicz_matrix_formation(input_information_dict, array_of_operations)
print(matrix_dict)
new_matrix_dict = t_norm(input_information_dict, matrix_dict, parcel_information_dict)
strait_output(new_matrix_dict, input_information_dict, parcel_information_dict, 1)'''