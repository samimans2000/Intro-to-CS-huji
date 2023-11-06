
def input_list():
    """
    asks the user for numbers, and adds them to a list. than the user inputs an
    empty input, the function takes all the numbers, sums them up them up and
    adds them to the end of the list.
    :return: a list of the numbers and their sum
    """
    numbers = []
    final_lst = []
    total = 0
    num = input()
    while num:
        numbers.append(num)
        num = input()
    else:
        for i in numbers:
            final_lst.append(float(i))
            total += float(i)
        final_lst.append(total)
    return final_lst


def inner_product(vec_1, vec_2):
    """
    gets two lists(vectors), Multiplies the first in the first list by the
    first in the second list and so on.
    :param vec_1: the first list(vector)
    :param vec_2: the second list(vector)
    :return: the total of the multiplication
    """
    if len(vec_1) != len(vec_2):
        return None
    total = 0
    for i in range(len(vec_1)):
        local_total = vec_1[i] * vec_2[i]
        total += local_total
    return total


def sequence_monotonicity(sequence):
    """
    the function gets a list of numbers and checks what kind of sequence
    they make and returns and answer.
    :param sequence: the list of numbers.
    :return: a list of True or False according to the numbers checked
    """
    ans = [True, True, True, True]
    for i in range(1, len(sequence)):
        if sequence[i] > sequence[i - 1]:
            if sequence[i] == sequence[i - 1]:
                ans[0:2] = True, False
            else:
                ans[2:4] = False, False
        elif sequence[i] < sequence[i - 1]:
            if sequence[i] == sequence[i - 1]:
                ans[2:4] = True, False
            else:
                ans[0:2] = False, False
        else:
            if sequence[i] == sequence[i - 1]:
                ans[1] = False
                ans[3] = False
    return ans


def monotonicity_inverse(def_bool):
    """
    the function gets a list of requirements
    :param def_bool: the requirements
    :return: a list of numbers
    """
    if def_bool == [True, True, False, False]:
        return [1, 2, 3, 4]
    elif def_bool == [True, False, False, False]:
        return [1, 2, 2, 4]
    elif def_bool == [False, False, True, True]:
        return [7.5, 4.3, 1.411, 0.111]
    elif def_bool == [False, False, True, False]:
        return [7.5, 4, 4, 0.111]
    elif def_bool == [True, False, True, False]:
        return [1, 1, 1, 1]
    elif def_bool == [False, False, False, False]:
        return [5, -5, 5, -5]
    else:
        return None


def is_prime(num):
    """
    the function checks if a number is a prime number.
    :return: True if the number is prime, else false
    """
    div = 2
    while div <= num ** 0.5:
        if num % div == 0:
            return False
        div += 1
    return True


def primes_for_asafi(n):
    """
    the function is told how many prime numbers to return and returns them
    by order from the smallest to the largest.
    :param n: how many prime numbers to return
    :return: list of n prime numbers
    """
    ans = []
    num = 2
    counter = 0
    while counter < n:
        if is_prime(num):
            ans.append(num)
            counter += 1
        num += 1
    return ans


def sum_of_vectors(vec_list):
    """
    the function receives a list of vectors (list of lists) and returns .
    :param vec_list: list of lists(list of vectors)
    :return: the vector sum
    """
    if not vec_list:
        return None
    counter = 0
    ans = []
    while counter < len(vec_list[0]):
        vectors_sum = 0
        for i in range(len(vec_list)):
            vectors_sum += vec_list[i][counter]
        ans.append(vectors_sum)
        counter += 1
    return ans


def num_of_orthogonal(vectors):
    """
    the function receives a list of vectors (list of lists) and returns the
    number of pairs in The lists that orthogonal to each other :param
    vectors: list of lists(list of vectors)
    :return: number of orthogonal vectors
    """
    counter = 0
    for i in range(len(vectors)):
        for j in range(i, len(vectors)):
            if i != j:
                c = inner_product(vectors[i], vectors[j])
                if c == 0:
                    counter += 1
    return counter

