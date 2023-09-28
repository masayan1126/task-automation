import random


def get_random_element_from_list(input_list: list, num_of_elem: int):
    if len(input_list) < num_of_elem:
        raise Exception(
            f"要素数は全要素数以上の数を指定することはできません。要素数={num_of_elem}, 全要素数={len(input_list)}"
        )  # リストの要素数が2未満の場合、Noneを返すか、エラーメッセージを出力するなど適切な処理を行う

    random_elements = random.sample(input_list, num_of_elem)
    return random_elements
