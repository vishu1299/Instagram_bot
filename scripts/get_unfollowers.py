import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

engine = webdriver.Chrome()
engine.get('https://www.instagram.com/')
sleep(10)

user_name = ""
passwd = ""

uid = engine.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input').send_keys(user_name)
passwd = engine.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input').send_keys(passwd)
btn = engine.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button').click()
sleep(5)
engine.get('https://www.instagram.com/{}'.format(user_name))
main_win = engine.current_window_handle

def get_followers():
    follower = engine.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
    sleep(5)

    scroll_box = engine.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
    engine.execute_script('arguments[0].scrollIntoView()',scroll_box)
    last_ht = 0
    ht = 1
    while last_ht != ht: 
        last_ht = ht
        sleep(5)
        ht = engine.execute_script("""
        arguments[0].scrollTo(0, arguments[0].scrollHeight);
        return arguments[0].scrollHeight;
        """,scroll_box)
    
    fList  = scroll_box.find_elements_by_tag_name('a')
    follower_names = [names.text for names in fList if names.text != '']
    finish = engine.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')\
        .click()
    return follower_names
	
def get_following():
    following = engine.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
    sleep(5)

    scroll_bar = engine.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
    engine.execute_script('arguments[0].scrollIntoView()', scroll_bar)
    last_ht = 0
    ht = 1
    while last_ht != ht: 
        last_ht = ht
        sleep(2)
        ht = engine.execute_script("""
        arguments[0].scrollTo(0, arguments[0].scrollHeight);
        return arguments[0].scrollHeight;
        """,scroll_bar)

    fList  = scroll_bar.find_elements_by_tag_name('a')
    following_names = [names.text for names in fList if names.text != '']
    finish = engine.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')\
        .click()
    return following_names

sleep(5)

follower = get_followers()
print('got the followers')
following = get_following()
print('got the following')

not_following = []
not_following = [user for user in following if user not in follower]
with open("unfollowers.txt", "w") as f:
    for line in not_following:
        f.write('%s\n' % line)

print("Operation Completed")
engine.close()
