def task(array: str) -> str:
    """
    Return string with index of first zero symbol in input stringю
    If array doesn't contains zero, return index as -1

    Parameters
    —------—
    array : str
    input string where we should find first zero index

    Returns
    —---—
    str
    string in next format f"OUT: {index of first zero}"
    """
    return f'OUT: {array.find("0")}'


if __name__ == "__main__":
    print(task("111111111110000000000000000"))
