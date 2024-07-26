from selenium import webdriver
import time
import csv
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_integer(value):
    try:
        return int(''.join(filter(str.isdigit, value)))
    except ValueError:
        return 0

def convert_time_to_minutes(time_str):
    try:
        if 'hrs' in time_str and 'mins' in time_str:
            hours, minutes = time_str.split(' ')
            return int(hours.replace('hrs', '')) * 60 + int(minutes.replace('m', ''))
        elif 'hrs' in time_str:
            return int(time_str.replace('hrs', '')) * 60
        elif 'mins' in time_str:
            return int(time_str.replace('mins', ''))
    except ValueError:
        return 0
    return 0

driver = webdriver.Chrome()
info = []
url = [
    "https://www.allrecipes.com/recipes/650/meat-and-poultry/chicken/fried-chicken/",
    "https://www.allrecipes.com/recipes/661/meat-and-poultry/chicken/chicken-thighs/",
    "https://www.allrecipes.com/recipes/201/meat-and-poultry/chicken/",
    "https://www.allrecipes.com/recipes/662/meat-and-poultry/chicken/whole-chicken/",
    "https://www.allrecipes.com/recipes/17022/meat-and-poultry/chicken/ground-chicken/",
    "https://www.allrecipes.com/recipes/17127/meat-and-poultry/chicken/chicken-sausage/",
    "https://www.allrecipes.com/recipes/17372/meat-and-poultry/chicken/chicken-tenders/",
    "https://www.allrecipes.com/recipes/649/meat-and-poultry/chicken/chicken-salad/",
    "https://www.allrecipes.com/recipes/660/meat-and-poultry/chicken/chicken-legs/",
    "https://www.allrecipes.com/recipes/663/meat-and-poultry/chicken/chicken-wings/",
    "https://www.allrecipes.com/recipes/664/meat-and-poultry/chicken/baked-and-roasted/",
    "https://www.allrecipes.com/recipes/14908/meat-and-poultry/chicken/cornish-hens/",
    "https://www.allrecipes.com/recipes/1234/appetizers-and-snacks/meat-and-poultry/chicken/",
    "https://www.allrecipes.com/recipes/124/bbq-grilling/chicken/",
    "https://www.allrecipes.com/recipes/2264/everyday-cooking/gourmet/main-dishes/chicken/",
    "https://www.allrecipes.com/recipes/1203/everyday-cooking/slow-cooker/main-dishes/chicken/",
    "https://www.allrecipes.com/recipes/14485/healthy-recipes/main-dishes/chicken/",
    "https://www.allrecipes.com/recipes/16954/main-dish/chicken/",
    "https://www.allrecipes.com/recipes/1032/main-dish/sandwiches/chicken/",
    "https://www.allrecipes.com/recipes/2254/main-dish/savory-pies/chicken-pie/",
    "https://www.allrecipes.com/recipes/2035/main-dish/stir-fry/chicken/",
    "https://www.allrecipes.com/recipes/14725/soups-stews-and-chili/chili/chicken-chili/",
    "https://www.allrecipes.com/recipes/1246/soups-stews-and-chili/soup/chicken-soup/",
    "https://www.allrecipes.com/recipes/657/soups-stews-and-chili/stews/chicken/"
]

driver.get("https://www.allrecipes.com/recipes/201/meat-and-poultry/chicken/")

# Wait until the list of items is present
categories = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "/html/body/main/section/div[1]/div[2]/div[2]/ul/li"))
)

# Iterate through the categories
for k in range(1, (len(categories) // 6)):
    # Click on the category to view the recipes
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, f"/html/body/main/section/div[1]/div[2]/div[2]/ul/li[{k}]"))
    ).click()

    # Fetch all recipes in the category
    recipe_titles = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[@class='card__title']"))
    )
    s = len(recipe_titles)

    # Iterate through the recipes and extract information
    for l in range(1, s):
        recipe = driver.find_element(by=By.XPATH, value=f"(//span[@class='card__title'])[{l}]")
        driver.execute_script("arguments[0].click()", recipe)
        time.sleep(5)
        try:
            name = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='article-header--recipe_1-0']/h1"))).text
        except TimeoutException:
            name = "NULL"
        try:
            rating = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mntl-recipe-review-bar__rating_1-0']"))).text
        except TimeoutException:
            rating = "NULL"
        try:
            reviews = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mntl-recipe-review-bar__comment-count_1-0']"))).text
        except TimeoutException:
            reviews = "NULL"
        try:
            total_time = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mntl-recipe-details_1-0']/div[1]/div[3]/div[2]"))).text
            total_time = convert_time_to_minutes(total_time)
        except TimeoutException:
            total_time = 0
        try:
            servings = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mntl-recipe-details_1-0']/div[1]/div[4]/div[2]"))).text
        except TimeoutException:
            servings = "NULL"
        try:
            calories = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mntl-nutrition-facts-summary_1-0']/table/tbody/tr[1]/td[1]"))).text
        except TimeoutException:
            calories = "NULL"
        try:
            fat = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mntl-nutrition-facts-summary_1-0']/table/tbody/tr[2]/td[1]"))).text
        except TimeoutException:
            fat = "NULL"
        try:
            carbs = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mntl-nutrition-facts-summary_1-0']/table/tbody/tr[3]/td[1]"))).text
        except TimeoutException:
            carbs = "NULL"
        try:
            protein = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mntl-nutrition-facts-summary_1-0']/table/tbody/tr[4]/td[1]"))).text
        except TimeoutException:
            protein = "NULL"

        # Convert values to integers where applicable
        try:
            rating = float(rating) if rating != "NULL" else 0.0
        except ValueError:
            rating = 0.0
        try:
            reviews = int(reviews.replace(' REVIEWS', '').replace(' REVIEW', '').replace(',', '')) if reviews != "NULL" else 0
        except ValueError:
            reviews = 0
        try:
            servings = int(servings.replace(' servings', '').replace(' serving', '')) if servings != "NULL" else 0
        except ValueError:
            servings = 0
        try:
            calories = int(calories.replace(' calories', '')) if calories != "NULL" else 0
        except ValueError:
            calories = 0
        try:
            fat = int(fat.replace('g', '')) if fat != "NULL" else 0
        except ValueError:
            fat = 0
        try:
            carbs = int(carbs.replace('g', '')) if carbs != "NULL" else 0
        except ValueError:
            carbs = 0
        try:
            protein = int(protein.replace('g', '')) if protein != "NULL" else 0
        except ValueError:
            protein = 0

        popularity = rating * reviews

        info.append([name, rating, reviews, total_time, servings, calories, fat, carbs, protein, popularity])
        print(name)
        driver.get(url[k - 1])
        time.sleep(3)
    driver.get("https://www.allrecipes.com/recipes/201/meat-and-poultry/chicken/")
    WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@id='mntl-taxonomy-nodes__chop-text_1-0']"))
    ).click()

# Write the information to CSV
with open("extracted_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Recipe Name", "Ratings", "No. of Reviews", "Total time (minutes)", "Servings", "Calories", "Fat", "Carbs", "Protein", "Popularity"])
    csvwriter.writerows(info)

driver.quit()