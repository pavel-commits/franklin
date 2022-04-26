def _get_result(result):
    A = {2: 1, 3: 2, 5: 3, 7: 4, 11: 5, 13: 6, 17: 8}

    if type(result) == str:
        result = int(result)

    values = [2, 3, 5, 7, 11, 13, 17]
    answer_json = {}
    for value in values:
        answer_json[value] = 0

    index = 0
    while result != 1 and index < len(values):
        if result % values[index] == 0:
            answer_json[values[index]] += 1
            result //= values[index]
        else:
            index += 1
    sum_score = sum(answer_json.values())
    answer_json = {k: v for k, v in sorted(answer_json.items(), key=lambda item: -item[1])}

    ans = {}
    for k, v in answer_json.items():
        ans[A[k]] = v * 100 // sum_score


    return ans


if __name__ == '__main__':
    pass