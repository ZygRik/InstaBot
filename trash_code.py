 # метод скачивает контент со страницы пользователя
    def download_userpage_content(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        # создаём папку с именем пользователя для чистоты проекта
        if os.path.exists(f"{file_name}"):
            print("Папка уже существует!")
        else:
            os.mkdir(file_name)

        img_and_video_src_urls = []
        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list[0:3]:
                try:
                    browser.get(post_url)
                    time.sleep(4)

                    img_src = "/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img"
                    video_src = "/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div/div[1]/div/div/video"
                    post_id = post_url.split("/")[-2]

                    if self.xpath_exists(img_src):
                        img_src_url = browser.find_element_by_xpath(img_src).get_attribute("src")
                        img_and_video_src_urls.append(img_src_url)

                        # сохраняем изображение
                        get_img = requests.get(img_src_url)
                        with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)

                    elif self.xpath_exists(video_src):
                        video_src_url = browser.find_element_by_xpath(video_src).get_attribute("src")
                        img_and_video_src_urls.append(video_src_url)

                        # сохраняем видео
                        get_video = requests.get(video_src_url, stream=True)
                        with open(f"{file_name}/{file_name}_{post_id}_video.mp4", "wb") as video_file:
                            for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    video_file.write(chunk)
                    else:
                        # print("Упс! Что-то пошло не так!")
                        img_and_video_src_urls.append(f"{post_url}, нет ссылки!")
                    print(f"Контент из поста {post_url} успешно скачан!")

                except Exception as ex:
                    print(ex)
                    self.close_browser()

            self.close_browser()

        with open(f'{file_name}/{file_name}_img_and_video_src_urls.txt', 'a') as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")











# def login(username, password):
#     browser = webdriver.Chrome('chromedriver/chromedriver')

#     try:
#         browser.get('https://www.instagram.com')
#         time.sleep(random.randrange(3, 5))

#         #find username in html code and input your auth_data
#         username_input = browser.find_element_by_name('username')
#         username_input.clear()
#         username_input.send_keys(username)

        
#         time.sleep(2) #pausing btw user actions

#         password_input = browser.find_element_by_name('password')
#         password_input.clear()
#         password_input.send_keys(password)

#         password_input.send_keys(Keys.ENTER) #imitate pressing Enter key by user

#         time.sleep(15)


#         browser.close()
#         browser.quit()

#     except Exception as ex:
#         print(ex)
#         browser.close()
#         browser.quit

# login(username, password)


# def hashtag_search(username, password, hashtag):
#     browser = webdriver.Chrome('chromedriver/chromedriver')

#     try:
#         browser.get('https://www.instagram.com')
#         time.sleep(random.randrange(3, 5))

#             #find username in html code and input your auth_data
#         username_input = browser.find_element_by_name('username')
#         username_input.clear()
#         username_input.send_keys(username)

            
#         time.sleep(2) #pausing btw user actions

#         password_input = browser.find_element_by_name('password')
#         password_input.clear()
#         password_input.send_keys(password)

#         password_input.send_keys(Keys.ENTER) #imitate pressing Enter key by user

#         time.sleep(15)    

#         try:
#             browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
#             time.sleep(5)

#             for i in range(1, 5):
#                 browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 time.sleep(random.randrange(3,5))

#             hrefs = browser.find_elements_by_tag_name('a')

#             posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
#             print(posts_urls)
            
#             #old code below, oneline code above
#             # posts_urls = []
#             # for item in hrefs:
#             #     href = item.get_attribute('href')

#             #     if "/p/" in href:
#             #         posts_urls.append(href)
#             #         print(href)

#             for url in posts_urls:
#                 try:
#                     browser.get(url)
#                     time.sleep(3)
#                     like_button = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
#                     time.sleep(random.randrange(88, 100))
#                 except Exception as ex:
#                     print(ex)


#             browser.close()
#             browser.quit()

#         except Exception as ex:
#             print(ex)
#             browser.close()
#             browser.quit()

#     except Exception as ex:
#         print(ex)
#         browser.close()
#         browser.quit()

# hashtag_search(username, password, 'bishkek')



