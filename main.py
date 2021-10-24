from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time, threading
import random
from selenium.common.exceptions import NoSuchElementException
import requests
import os
import json
import schedule
from schedule import every, repeat, run_pending
from timeloop import Timeloop
from datetime import timedelta

class InstaBot():

    #инициализация данных аккаунта и браузера
    def __init__(self, username, password):
        self.username = username 
        self.password = password
        self.browser = webdriver.Chrome("chromedriver/chromedriver")
        # self.browser = webdriver.Firefox(executable_path=(r'geckodriver/geckodriver'))

    #метод закрывает браузер
    def close_browser(self):
        self.browser.close()
        self.browser.quit()
    
    #метод логинится на аккаунт
    def login(self):

        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(1, 5))

            #find username in html code and input your auth_data
        
        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)
        

        time.sleep(random.randrange(0, 5)) #pausing btw user actions

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        time.sleep(random.randrange(4, 36))
        password_input.send_keys(Keys.ENTER) #imitate pressing Enter key by user

        time.sleep(15)

    #метод лайкает фотки по хэштегу
    def like_photo_by_hashtag(self, hashtag):

        browser =  self.browser

        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(random.randrange(0, 4))

        for i in range(1, 5):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(0,5))

        hrefs = browser.find_elements_by_tag_name('a')

        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:
            try:
                browser.get(url)
                time.sleep(3)
                like_button = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(2, 30))
            except Exception as ex:
                print(ex)
                self.close_browser()


        #check if xpath exists on the page
    
    #метод проверяет существует ли xpath
    def xpath_exists(self, url):
        browser =  self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

        #put like on the post with direct ref
    
    #метод ставит лайки на конкретные посты пользователя
    def put_exactly_like(self, userpost):

        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("That post doesn't exist! Check URL")
            self.close_browser()
        else:
            print("Post successfully found, like it!")
            time.sleep(2)

            like_button = "/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button"
            browser.find_element_by_xpath(like_button).click()
            time.sleep(4)

            print(f"Post: {userpost} Liked!")
            self.close_browser()


    #метод собирает ссылки на все посты пользователя:
    def get_all_posts_urls(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/div/h2"

        if self.xpath_exists(wrong_userpage):
            print("That user doesn't exist! Check URL")
            self.close_browser()
        else:
            print("User successfully found, like it!")
            time.sleep(2)

            posts_count = int(browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)

            loops_count = int(posts_count /12)

            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)
                
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3,5))
                print(f"Iteration #{i+1}")

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")
            
            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)
            
            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n') 

    #метод ставит лайки  по ссылкам на аккаунте пользователя:
    def put_many_likes(self, userpage):
        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(random.randrange(1,4))
        browser.get(userpage)
        time.sleep(4)     

        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()
            
            for post_url in urls_list[0:6]:
                try:
                    browser.get(post_url)
                    time.sleep(random.randrange(1, 3))
                
                    like_button = "/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button"
                    browser.find_element_by_xpath(like_button).click()
                    # time.sleep(random.randrange(80, 100))
                    time.sleep(2)
                    print(f"Post: {post_url} Liked!")
                
                except Exception as ex:
                    print(ex)
                    self.close_browser()
        
        self.close_browser()
    
    

    #метод подписки на всех подписчиков переданного аккаунта:
    def get_all_followers(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split("/")[-2]

         # создаём папку с именем пользователя для чистоты проекта
        if os.path.exists(f"{file_name}"):
            print(f"Папка {file_name} уже существует!")
        else:
            print(f"Создаем папку пользователя {file_name}")
            os.mkdir(file_name)


        wrong_userpage = "/html/body/div[1]/section/main/div/div/h2"

        if self.xpath_exists(wrong_userpage):
            print(f"Пользователя {file_name} не существует, проверьте URL!")
            self.close_browser()
        else:
            print(f"Пользователь {file_name} найден! скачиваем ссылки для подписки!")
            time.sleep(2)

        followers_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
        followers_count = followers_button.text
        followers_count = 1000*(int(followers_count.split(' ')[0].replace("k", "")))
        
        print(f"Количество подписчиков: {followers_count}")
        time.sleep(2)

        loops_count = int(followers_count / 12)
        print(f"Число итераций: {loops_count}")
        time.sleep(random.randrange(1, 3))

        followers_button.click()
        time.sleep(random.randrange(1, 3))

        followers_ul = browser.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/ul")

        try:
            followers_urls = []
            for i in range(1, loops_count +1):
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                time.sleep(random.randrange(2, 4))
                print(f"Итерация №{i}")
            all_urls_div = followers_ul.find_elements_by_tag_name("li")

            for url in all_urls_div:
                url = url.find_element_by_tag_name("a").get_attribute("href")
                followers_urls.append(url)

            #сохраняем список всех подписчиков в файл:
            with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                for link in followers_urls:
                    text_file.write(link + "\n")
            
            with open(f"{file_name}/{file_name}.txt") as text_file:
                users_urls = text_file.readlines()

                for user in users_urls:
                    try:
                        try:
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        print(f'Мы уже подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                        except Exception as ex:
                            print('Файл со ссылками ещё не создан!')
                            # print(ex)

                        browser = self.browser
                        browser.get(user)
                        page_owner = user.split("/")[-2]

                        if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div/a"):

                            print("Это наш профиль, уже подписан, пропускаем итерацию!")
                        elif self.xpath_exists(
                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button/div/span"):
                            print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                        else:
                            time.sleep(random.randrange(4, 8))

                            if self.xpath_exists(
                                    "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                try:
                                    follow_button = browser.find_element_by_xpath(
                                        "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button").click()
                                    print(f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                                except Exception as ex:
                                    print(ex)
                            else:
                                try:
                                    if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button"):
                                        follow_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                        print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                    else:
                                        follow_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button").click()
                                        print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                except Exception as ex:
                                    print(ex)

                            # записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем
                            with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                        'a') as subscribe_list_file:
                                subscribe_list_file.write(user)

                            time.sleep(random.randrange(120, 180))
                    
                    except Exception as ex:
                        print(ex)
                        self.close_browser()
                         
        except Exception as ex:
            print(ex)
            self.close_browser()

    #метод отписки от всех пользователей
    def unfollow_all(self, userpage):
       
        browser =  self.browser
        browser.get(f"https://instagram.com/{username}/")
        time.sleep(random.randrange(2, 6))

        following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_count =  following_button.find_element_by_tag_name("span").text

        #если кол-во больше 999, убираем запятые
        if ',' in following_count:
            followers_count = int(''.join(following_count.split(',')))
        else:
            followers_count = int(following_count)
        print(f"Количество подписок: {following_count}")
        
        time.sleep(random.randrange(2, 8))
        
        loops_count = int(followers_count / 10) +1
        print(f"Количество перезагрузок страницы: {loops_count}")

        following_users_dict = {}

        for loop in range(1, loops_count + 1):

            count = 10

            browser.get(f"https://instagram.com/{username}/")
            time.sleep(random.randrange(3, 6))

            #кликаем и вызываем меню подписок
            following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
            
            following_button.click()
            time.sleep(random.randrange(3, 10))

            #забираем все li из ul, в них хранятся кнопка отписки и ссылки на подписки
            following_div_block = browser.find_element_by_xpath("/html/body/div[6]/div/div/div[3]/ul/div")
            following_users = following_div_block.find_elements_by_tag_name("li")
            time.sleep(random.randrange(2, 6))

            for user in following_users:

                if not count:
                    break

                user_url = user.find_element_by_tag_name("a").get_attribute("href")
                user_name = user_url.split("/")[-2]

                #добавляем в словарь имя пользователя и ссылку(на всякий случай)
                following_users_dict[username] = user_url



                following_button = user.find_element_by_tag_name("button").click()
                time.sleep(random.randrange(2, 10))
                unfollow_button =  browser.find_element_by_xpath("/html/body/div[7]/div/div/div/div[3]/button[1]").click()

                print(f"Итерация № {count} >>> Отписался от пользователя {user_name}")

                count -= 1
                
                time.sleep(random.randrange(10, 60))
                browser =  self.browser



        

# метод отписки, отписываемся от всех кто не подписан на нас
    def smart_unsubscribe(self, username):

        browser = self.browser
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        followers_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
        followers_count = followers_button.get_attribute("title")

        following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_count = following_button.find_element_by_tag_name("span").text

        time.sleep(random.randrange(3, 6))

        # если количество подписчиков больше 999, убираем из числа запятые
        if ',' in followers_count or following_count:
            followers_count, following_count = int(''.join(followers_count.split(','))), int(''.join(following_count.split(',')))
        else:
            followers_count, following_count = int(followers_count), int(following_count)

        print(f"Количество подписчиков: {followers_count}")
        followers_loops_count = int(followers_count / 12) + 1
        print(f"Число итераций для сбора подписчиков: {followers_loops_count}")

        print(f"Количество подписок: {following_count}")
        following_loops_count = int(following_count / 12) + 1
        print(f"Число итераций для сбора подписок: {following_loops_count}")

        # собираем список подписчиков
        followers_button.click()
        time.sleep(4)

        followers_ul = browser.find_element_by_xpath("/html/body/div[6]/div/div/div[2]")

        try:
            followers_urls = []
            print("Запускаем сбор подписчиков...")
            for i in range(1, followers_loops_count + 1):
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            all_urls_div = followers_ul.find_elements_by_tag_name("li")

            for url in all_urls_div:
                url = url.find_element_by_tag_name("a").get_attribute("href")
                followers_urls.append(url)

            # сохраняем всех подписчиков пользователя в файл
            with open(f"{username}_followers_list.txt", "a") as followers_file:
                for link in followers_urls:
                    followers_file.write(link + "\n")
        except Exception as ex:
            print(ex)
            self.close_browser()

        time.sleep(random.randrange(4, 6))
        browser.get(f"https://www.instagram.com/{username}/")
        

        # собираем список подписок
        following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_button.click()
        time.sleep(random.randrange(3, 5))

        following_ul = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

        try:
            following_urls = []
            print("Запускаем сбор подписок")

            for i in range(1, following_loops_count + 1):
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_ul)
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            all_urls_div = following_ul.find_elements_by_tag_name("li")

            for url in all_urls_div:
                url = url.find_element_by_tag_name("a").get_attribute("href")
                following_urls.append(url)

            # сохраняем всех подписок пользователя в файл
            with open(f"{username}_following_list.txt", "a") as following_file:
                for link in following_urls:
                    following_file.write(link + "\n")

            """Сравниваем два списка, если пользователь есть в подписках, но его нет в подписчиках,
            заносим его в отдельный список"""

            count = 0
            unfollow_list = []
            for user in following_urls:
                if user not in followers_urls:
                    count += 1
                    unfollow_list.append(user)
            print(f"Нужно отписаться от {count} пользователей")

            # сохраняем всех от кого нужно отписаться в файл
            with open(f"{username}_unfollow_list.txt", "a") as unfollow_file:
                for user in unfollow_list:
                    unfollow_file.write(user + "\n")

            print("Запускаем отписку...")
            time.sleep(2)

            # заходим к каждому пользователю на страницу и отписываемся
            with open(f"{username}_unfollow_list.txt") as unfollow_file:
                unfollow_users_list = unfollow_file.readlines()
                unfollow_users_list = [row.strip() for row in unfollow_users_list]

            try:
                count = len(unfollow_users_list)
                for user_url in unfollow_users_list:
                    browser.get(user_url)
                    time.sleep(random.randrange(4, 6))

                    # кнопка отписки
                    unfollow_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
                    unfollow_button.click()

                    time.sleep(random.randrange(4, 6))

                    # подтверждение отписки
                    unfollow_button_confirm = browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[1]")
                    unfollow_button_confirm.click()

                    print(f"Отписались от {user_url}")
                    count -= 1
                    print(f"Осталось отписаться от: {count} пользователей")

                    # time.sleep(random.randrange(120, 130))
                    time.sleep(random.randrange(4, 6))

            except Exception as ex:
                print(ex)
                self.close_browser()

        except Exception as ex:
            print(ex)
            self.close_browser()

        time.sleep(random.randrange(4, 6))
        self.close_browser()


#     for user, user_data in users_settings_dict.items():
#         username = user_data['login']
#         password = user_data['password']
# # window_size = user_data['window_size']

   
   
    



my_bot = InstaBot(username, password)
my_bot.login()

schedule.every(1).to(6).minutes.do(my_bot.unfollow_all("mommy_kg"))






# my_bot.smart_unsubscribe("mommy_kg")



#my_bot.like_photo_by_hashtag("bishkek")
#my_bot.get_all_followers('https://www.instagram.com/fashion_shop_kg/')
# my_bot.download_userpage_content("https://www.instagram.com/meder.myrzaev/")
        