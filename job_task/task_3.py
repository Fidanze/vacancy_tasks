def easy_appearance(intervals: dict[str, list[int]]) -> int:
    """
    Return time of the total presence of pupil and tutor in the lesson (in seconds)

    Parameters
    —------—
    intervals : dict[str, list[int]]
    Contains 3 items:
        1) intervals['letter'] is pair of int, start and end of lesson
        2) intervals['pupil'] is list of int, where int mean like this [start1,end1,...startN, endN]
        3) intervals['tutor'] is list of int, where int mean like this [start1,end1,...startN, endN]
    Returns
    —---—
    int
    Time of the total presence of pupil and tutor in the lesson (in seconds)
    """
    # init input data as sets{start, start+1, start+2, ..., end-1, end}
    lesson: set[int] = set(range(*intervals['lesson']))
    pupil: list[set[int]] = [set(range(v, intervals['pupil'][2*k+1]))
                             for k, v in enumerate(intervals['pupil'][::2])]
    tutor: list[set[int]] = [set(range(v, intervals['tutor'][2*k+1]))
                             for k, v in enumerate(intervals['tutor'][::2])]

    # get union sets of tutor and pupil times
    tutor_union: set[int] = set()
    pupil_union: set[int] = set()

    for t_interval in tutor:
        tutor_union = tutor_union.union(t_interval)
    for p_interval in pupil:
        pupil_union = pupil_union.union(p_interval)

    # get intersection of tutor and pupil times unions
    t_p_intersection: set[int] = tutor_union.intersection(pupil_union)

    # return intersection of all three groups
    return len(t_p_intersection.intersection(lesson))


def areIntersect(start1: int, end1: int, start2: int, end2: int) -> bool:
    """
    Check if intervals intersect

    Parameters
    —------—
    start1: int
    start time of first interval
    end1: int
    end time of first interval
    start2: int
    start time of second interval
    end2: int
    end time of second interval
    Returns
    —---—
    bool 
        True if intervals intersect else False 
    """
    return start2 <= start1 <= end2 or start2 <= end1 <= end2


def get_intersection(start1: int, end1: int, start2: int, end2: int) -> tuple[int, int] | None:
    """
    Compute intersection of two intervals if it's exist

    Parameters
    —------—
    start1: int
    start time of first interval
    end1: int
    end time of first interval
    start2: int
    start time of second interval
    end2: int
    end time of second interval
    Returns
    —---—
    bool 
        True if intervals intersect else False 
    """
    new_start: int = max(start1, start2)
    new_end: int = min(end1, end2)
    if new_start <= new_end:
        return new_start, new_end
    else:
        return None


def optimize_appearance(intervals: dict[str, list[int]]) -> int:
    """
    Return time of the total presence of pupil and tutor in the lesson (in seconds)

    Parameters
    —------—
    intervals : dict[str, list[int]]
    Contains 3 items:
        1) intervals['letter'] is pair of int, start and end of lesson
        2) intervals['pupil'] is list of int, where int mean like this [start1,end1,...startN, endN]
        3) intervals['tutor'] is list of int, where int mean like this [start1,end1,...startN, endN]
    Returns
    —---—
    int
    Time of the total presence of pupil and tutor in the lesson (in seconds)
    """

    # check if any input data is empty list
    if not (intervals['lesson'] or intervals['pupil'] or intervals['tutor']):
        return 0

    # init input data as tuples(start, end)
    lesson: tuple[int, int] = (intervals['lesson'][0], intervals['lesson'][1])
    pupils: list[tuple[int, int]] = [(v, intervals['pupil'][2*k+1])
                                     for k, v in enumerate(intervals['pupil'][::2])]
    tutors: list[tuple[int, int]] = [(v, intervals['tutor'][2*k+1])
                                     for k, v in enumerate(intervals['tutor'][::2])]

    # search intersections of lesson and pupil
    temp: list[tuple[int, int]] = []
    for pupil in pupils:
        pupil_lesson = get_intersection(*lesson, *pupil)
        if pupil_lesson:
            temp.append(pupil_lesson)

    # check if lessons and pupil doesn't have intersections
    if not temp:
        return 0

    # search tutors intersection with result of previous step
    pl_tutors: list[tuple[int, int]] = []
    for pupil_lesson in temp:
        for tutor in tutors:
            pupil_lesson_tutor = get_intersection(*pupil_lesson, *tutor)
            if pupil_lesson_tutor:
                pl_tutors.append(pupil_lesson_tutor)

    # clear results from repeated intersections
    while True:
        temp = pl_tutors[:]
        isChanged = False
        for key, plt in enumerate(pl_tutors[:-1]):
            for key1, plt1 in enumerate(pl_tutors[key+1:]):
                if areIntersect(*plt, *plt1):
                    temp.pop(key)
                    temp.pop(key1)
                    temp.append(
                        (min(plt[0], plt1[0]), max(plt[1], plt1[1])))
                    isChanged = True
                    break
            if isChanged:
                break
        else:
            break
        pl_tutors = temp[:]

    # return sum of all results lengths
    return sum([plt[1]-plt[0] for plt in pl_tutors])


tests = [
    {'data': {'lesson': [1594663200, 1594666800],
              'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
              'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'data': {'lesson': [1594702800, 1594706400],
              'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
              'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'data': {'lesson': [1594692000, 1594695600],
              'pupil': [1594692033, 1594696347],
              'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = optimize_appearance(test['data'])
        assert test_answer == test[
            'answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
