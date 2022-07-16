from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from requests import get, Response
from bs4 import BeautifulSoup, Tag


def get_letters(url: str) -> dict[str, list[str]]:
    """
    Return dictionary of available russian letter and empty lists from web page on received url

    Parameters
    —------—
    url : str
    url to start page of search

    Returns
    —---—
    dict[str]
    dictionary of animals russian names by first letter
    """
    response: Response = get(url)
    assert response.status_code == 200, "Response was failed"
    soup = BeautifulSoup(response.text, 'lxml')
    headline: str = soup.select_one(
        '#mw-content-text > div.mw-parser-output > table > tbody > tr').text
    return {letter: [] for letter in headline.split('•')[2]}


def get_animals(letter: str, animals: list[str], url: str) -> tuple[list[str], str | None]:
    """
    Return list of animal names which start by letter and url to next page if it exist.
    If next page doesn't exist, return list of animal names and None

    Parameters
    —------—
    letter : str
    first letter of animals names that we search
    animals : list[str]
    list of finded animals names for letter
    url : str
    url for start page of animal by letter

    Returns
    —---—
    tuple[list[str], str | None]
    List of founded animals name for letter and url to next_page if it exist else None
    """
    response: Response = get(url)
    assert response.status_code == 200, "Response was failed"
    soup = BeautifulSoup(response.text, 'lxml')
    is_ended: bool = False
    for el in soup.select('.mw-category-columns > .mw-category-group'):
        el_letter, _, el_animals = tuple(el.children)
        if el_letter.text == letter:
            animals.extend(el_animals.text.split('\n'))
        else:
            is_ended = True
            break
    next_page: Tag | None = soup.select_one('#mw-pages > a:last-child')
    if is_ended or next_page is None:
        return animals, None
    return animals, f'https://ru.wikipedia.org{next_page.attrs["href"]}'


def thread_func(animals_dict: dict[str, list[str]]) -> Callable[[str], None]:
    """
    Return wrapped for correct thread work function

    Parameters
    —------—
    animals_dict : dict[str,list[str]]
    dictionary of animals russian names by first letter

    Returns
    —---—
    Callable[[str], None]
    wrapped function for getting animals names by letter

    """
    def get_animals_by_letter(letter: str) -> None:
        """
        Modify animals_dict from wrapper function.
        Write to it all animal for choosed letter

        Parameters
        —------—
        letter : str
        first letter of animals names

        Returns
        —---—
        None
        """
        next_page: str | None = f'https://ru.wikipedia.org/w/index.php?title=Категория%3AЖивотные_по_алфавиту&from={letter}'
        while next_page:
            animals_dict[letter], next_page = get_animals(
                letter, animals_dict[letter], next_page)
    return get_animals_by_letter


def main(url: str) -> dict[str, list[str]]:
    """
    Return dictionary of letters and animal names that begins by letters

    Parameters
    —------—
    url: str
    url where should we start parsing

    Returns
    —---—
    dict[str, list[str]]
    dictionary of animals russian names by first letter

    """
    animals_dict: dict[str, list[str]] = get_letters(url)
    task_func: Callable[[str], None] = thread_func(animals_dict)
    with ThreadPoolExecutor(4) as executor:
        executor.map(task_func, animals_dict.keys())
    return animals_dict


if __name__ == "__main__":
    animals = main("https://inlnk.ru/jElywR")
    for letter, animals_names in animals.items():
        print(f'{letter}: {len(animals_names)}')
