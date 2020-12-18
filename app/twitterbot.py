from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import os
import time

class TwitterBot:

    hashtags = [
        'beerleaguehockey', 'beerleague', 'cawlidgehawkey', 'nhl', 'hockeytwitter', 'hockeyplayer', 'juniorhockey', 'ahl', 'echl'
    ]

    def __init__(self):
        executable = GeckoDriverManager().install()
        options = Options()
        options.headless = True
        username = os.environ['USERNAME']
        password = os.environ['PASSWORD']
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox(executable_path=executable, options=options)
        
        
    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/')
        time.sleep(10)
        
        email = bot.find_element_by_name('session[username_or_email]')
        password = bot.find_element_by_name('session[password]')
        
        email.clear()
        password.clear()
        
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

    def like_tweet(self):
        bot = self.bot
        time.sleep(6)
        for hashtag in self.hashtags:
            bot.get('https://twitter.com/search?q=%23'+hashtag+'&src=typd')
            print('Working on #'+hashtag+'.')
            time.sleep(12)
            links = set()
            for i in range(1):
                bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(8)
                    
                [links.add(elem.get_attribute('href')) for elem in bot.find_elements_by_xpath("//a[@dir ='auto']") ]    
                condition = lambda link: '/status/' in link and '/media_tags' not in link
                valid_links = list(filter(condition, links))
                for valid_link in valid_links:
                    print(valid_link)
                    bot.get(valid_link)
                    time.sleep(6)
                    try:
                        bot.find_element_by_css_selector(".css-18t94o4[data-testid ='like']").click()
                        print('Liked.')
                        time.sleep(11)
                    except Exception as ex:
                        print ('Nothing to like here, moving on in a minute.')
                        time.sleep(60)

    def close_browser(self):
        bot = self.bot
        bot.quit()

followers = TwitterBot()
 
followers.login()

followers.like_tweet()

followers.close_browser()