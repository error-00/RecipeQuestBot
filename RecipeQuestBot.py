import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import telebot
from telebot import types

TOKEN = 'TOKEN'

RECIPE_SEARCH_URL = 'https://www.allrecipes.com/search?q='

random_ingredients = ['chicken', 'potato', 'cucumber', 'eggs', 'pepper', 'rice', 'tomato', 'onion',
                      'cheese', 'pasta', 'carrot', 'broccoli', 'garlic', 'lemon', 'apple', 'mushrooms', 'cake', 'fish',
                      'meat', 'shrimp']

# Bot initialization
bot = telebot.TeleBot(TOKEN)


# Processing the /start command
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item_random = types.KeyboardButton('Random recipe')
    markup.add(item_random)

    bot.send_message(message.chat.id, 'Hi! Enter the ingredients, separated by commas, and I will tell you the recipes',
                     reply_markup=markup)


# Text message processing
@bot.message_handler(func=lambda message: message.text != 'Random recipe')
def find_recipe(message):
    user_ingredients = message.text
    bot.send_message(message.chat.id, 'Looking for a recipe...')
    recipes = search_recipe(user_ingredients)

    if not recipes:
        bot.send_message(message.chat.id, "Unfortunately, we couldn't find recipes")
    else:
        for recipe in recipes:
            bot.send_message(message.chat.id, recipe)


def search_recipe(ingredients: str) -> str:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    # search recipe
    search_url = RECIPE_SEARCH_URL + ingredients
    driver.get(search_url)
    time.sleep(2)

    recipes = []

    try:
        recipe_elements = driver.find_elements(By.XPATH,
                                               '//a[@class="comp mntl-card-list-items mntl-document-card mntl-card card card--no-image"]')
        for recipe_element in recipe_elements[:5]:
            recipe_name = recipe_element.text
            recipe_link = recipe_element.get_attribute('href')
            recipe = f'Recipe: {recipe_name}\n\nLink: {recipe_link}'
            recipes.append(recipe)
    except:
        pass

    driver.quit()
    return recipes


def search_random_recipe() -> str:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    ingredient = random.choice(random_ingredients)

    random_url = RECIPE_SEARCH_URL + ingredient
    driver.get(random_url)
    time.sleep(2)

    try:
        recipe_element = driver.find_element(By.XPATH,
                                             '//a[@id="mntl-card-list-items_1-0"]')
        recipe_name = recipe_element.text
        recipe_link = recipe_element.get_attribute('href')
        recipe = f'Recipe: {recipe_name}\n\nLink: {recipe_link}'
    except:
        recipe = "Unfortunately, we couldn't find recipes"

    driver.quit()
    return recipe


@bot.message_handler(func=lambda message: message.text == 'Random recipe')
def random_recipe(message):
    bot.send_message(message.chat.id, 'Looking for a recipe...')
    recipe = search_random_recipe()
    bot.send_message(message.chat.id, recipe)


# Bot launch
if __name__ == '__main__':
    bot.polling(none_stop=True)
