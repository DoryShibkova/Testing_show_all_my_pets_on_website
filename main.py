import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    yield
    pytest.driver.quit()


def testing_show_all_my_pets():
    pytest.driver.find_element(By.ID, 'email').send_keys('dasha.shibkova03@mail.ru')
    pytest.driver.find_element(By.ID, 'pass').send_keys('Dashuta03')
    time.sleep(2)
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    pytest.driver.find_element(By.CLASS_NAME, "nav-item").click()
    pets_number = int(pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text
                    .split('\n')[1].split(":")[1])
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))
    print('Number of pets:', pets_number)

    pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')))
    print(len(pets))

    assert pets_number == len(pets)

    pytest.driver.implicitly_wait(10)
    photos = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    pets_names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')
    types_of_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[2]')
    pets_ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[3]')

    count = 0
    for img in photos:
        if img.size != {'height': 0, 'width': 0}:
            count = count + 1

    assert count > len(pets) / 2

    names = []
    for pet in pets_names:
        names.append(pet.text.split(' '))
    for i in names:
        assert i != " "
    for k in range(len(names) - 1):
        for m in range(k+1, len(names)):
            assert names[k] != names[m]

    print(names)

    ages = []
    for pet in pets_ages:
        ages.append(pet.text.split(' '))
    for i in ages:
        assert i != " "
    print(ages)

    types = []
    for pet in types_of_pets:
        types.append(pet.text.split(' '))
    for i in types:
        assert i != " "
    print(types)

    new_count = 0
    for i in range(len(pets) - 1):
        for j in range(i+1, len(pets)):
            if types[i] == types[j] and names[i] == names[j] and ages[i] == ages[j]:
                new_count = new_count + 1

    assert new_count == 0
