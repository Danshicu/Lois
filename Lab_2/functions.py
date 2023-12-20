# Лабораторная работа 2 по предмету "Логические основы интеллектуальных систем"
# Вариант 9: Запрограммировать обратный нечеткий логический вывод на основе операции нечеткой композиции (min({1}∪{max({0}∪{xi+yi-1}|i})
# Выполнили студенты группы 121702: Промчук Д.В, Шакин И.В, Шершень К.А.
# Дата выполнения: 18.12.2023

from re import fullmatch
from itertools import product
import json

def read_file(count):
    count-=1
    with open("input", 'r') as file:
        lines = file.readlines()
    if len(lines) >= count*3+2 and count>=0:
        consequence = lines[count*3]
        relation = lines[count*3+1]
        return consequence, relation
    else:
        if count!=-2:
            raise Exception("Неверный номер следствия")
        else:
            raise Exception("Выход из программы")

def write_file(consequence, relation, result):
    with open("output", 'r') as file:
        lines = file.readlines()

    answer = f"Для следствия {consequence} и отношения {relation} обратный нечёткий логический вывод: {result}\n"
    with open("output", 'a') as file:
        for line in lines:
            if line == answer:
                return
        file.write(answer)

def all_combinations(*arrays):
    return list(product(*arrays))




def text_to_formula(text):
    res = []
    tmp = text.split(",")
    for i in tmp:
        res.append(tuple([i.split(":")[0], float(i.split(":")[1])]))
    return res


def interwal(x):
    return 0 <= x <= 1


def remove_duplicates(list_of_lists):
    unique_lists = set(tuple(tuple(sublist) for sublist in nested_list) for nested_list in list_of_lists)
    return [list(tuple_list) for tuple_list in unique_lists]


def include_each_other(i, point):
    flags = []
    for interval1, interval2 in zip(i, point):
        if interval1[0] == interval2[0] and interval1[1] == interval2[1]:
            flags.append(0)
        elif interval1[0] >= interval2[0] and interval1[1] <= interval2[1]:
            if interval1[0] == interval1[1]:
                return "Добавить"
            flags.append(2)
        elif interval2[0] >= interval1[0] and interval2[1] <= interval1[1]:
            if interval1[0] == interval1[1]:
                return "Добавить"
            flags.append(1)
    if 1 in flags and 2 in flags:
        return "Добавить"
    elif 1 not in flags:
        return "Заменить"
    elif 2 not in flags or (1 not in flags and 2 not in flags):
        return "Не добавлять"


def check_include(res, point):
    for i in range(len(res)):
        status = include_each_other(res[i], point)
        if status == "Не добавлять":
            return res
        elif status == "Заменить":
            res[i] = point
            return res
    res.append(point)
    return res


def merge_answers(answers):
    all_comb_con = all_combinations(*answers)
    res = []
    for comb in all_comb_con:
        # print("combination", comb)
        tmp_point = []
        for i in range(len(comb[0])):
            tmp = [tt[i] for tt in comb]
            left_border = round(max([one[0] for one in tmp]), 1)
            right_border = round(min([two[1] for two in tmp]), 1)

            if left_border <= right_border:
                tmp_point.append(tuple([left_border, right_border]))
        if len(tmp_point) == len(comb[0]):
            res = check_include(res, tmp_point)
    if res:
        return result_to_string(res)
    return None


def result_to_string(result):
    result_answer = []
    for dis_answer in result:
        answer = []
        for i in range(len(dis_answer)):
            if dis_answer[i][0] < dis_answer[i][1]:
                answer.append(f"a{i + 1}=[{dis_answer[i][0]};{dis_answer[i][1]}]")
            elif dis_answer[i][0] == dis_answer[i][1]:
                answer.append(f"a{i + 1}={dis_answer[i][0]}")
        result_answer.append(answer)
    return result_answer


def reverse_fuzzy_logic_inference(consequence, relation_matrix):
    answer = []
    for row in zip(relation_matrix, consequence):
        if row[1] == 1:
            point = []
            for rel in row[0]:
                if interwal(2 - rel):
                    point.append(tuple([2 - rel, 1.0]))
                else:
                    return None
            answer.append([point])
        elif 0 < row[1] < 1:
            dis_points = []
            for index_rel in range(len(row[0])):
                point = []
                for index_rel2 in range(len(row[0])):
                    tmp = row[1] + 1 - row[0][index_rel2]
                    if interwal(tmp):
                        if index_rel == index_rel2:
                            point.append((tmp, tmp))
                        else:
                            point.append((tmp, 1.0))
                    else:
                        point = []
                        break
                if point:
                    dis_points.append(point)
            if dis_points:
                answer.append(remove_duplicates(dis_points))
            else:
                return None
        elif row[1] == 0:
            dis_points = []

            for index_rel in range(len(row[0])):
                point = []
                for index_rel2 in range(len(row[0])):

                    tmp = 1 - row[0][index_rel2]
                    if index_rel == index_rel2:
                        if interwal(tmp):
                            point.append(tuple([0.0, tmp]))
                        else:
                            point = []
                            break
                    else:
                        point.append(tuple([0.0, 1.0]))
                if point:
                    dis_points.append(point)
            if dis_points:
                answer.append(remove_duplicates(dis_points))
            else:
                return None
    return answer

