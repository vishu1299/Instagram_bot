import selenium
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys


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

def blue_tick():
    try:
        bluetick = engine.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span')
        return True
    except Exception as e:
        return False
		
not_following = []
with open('unfollowers.txt', 'r') as filehandle:
    for line in filehandle:
        # remove linebreak which is the last character of the string
        currentPlace = line[:-1]

        # add item to the list
        not_following.append(currentPlace)
print(not_following)

engine.switch_to_window(main_win)
i = 0 
for name in not_following:
    i = i + 1 
    if( i % 10 == 0):
        print('sleeping')
        sleep(120)
    search = engine.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input').send_keys(name)
    sleep(10)

    popup = engine.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]')
    engine.execute_script('arguments[0].scrollIntoView()', popup)

    unfollower = popup.find_element_by_tag_name('a').click()
    sleep(5)

    verification = blue_tick()
    if not verification:
        unfollow_btn = engine.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button').click()
        sleep(5)
        unfollow_popup = engine.find_element_by_xpath('/html/body/div[4]/div/div/div')
        engine.execute_script('arguments[0].scrollIntoView()', unfollow_popup)
        unfollow = unfollow_popup.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]').click()
        print("Successfuly Unfollowed:" + name)
        sleep(10)   

engine.close()
