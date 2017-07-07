from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver.exe')
browser.get('http://twitter.com')
top_bar = browser.find_element_by_css_selector(".StreamsTopBar.StreamsTopBar--fixed.js-variableHeightTopBar")
tall = top_bar.find_element_by_css_selector('.StreamsHero.StreamsHero--tall')
bc = tall.find_element_by_css_selector('.StreamsHero-buttonContainer')
bc.find_element_by_css_selector('.Button.StreamsLogin.js-login').click()
browser.find_element_by_xpath("//input[contains(@name,'username')]").send_keys('michellewoo567@yahoo.com')
browser.find_element_by_xpath("//input[contains(@name,'password')]").send_keys('wmq531,,.')
browser.find_element_by_xpath("//input[contains(@name,'password')]").send_keys(Keys.RETURN)

pr = browser.find_element_by_class_name('pull-right')
si = pr.find_element_by_class_name('search-input')
si.send_keys('#bonnaroo')
si.send_keys(Keys.RETURN)
time.sleep(5)

tweetList = []
scroll = 0

while len(tweetList) <= 1000:
    WEtweetList = browser.find_elements_by_css_selector('.TweetTextSize.js-tweet-text.tweet-text')
    for t in WEtweetList:
        if t.text not in tweetList:
            tweetList.append(t.text)
        
    send = WEtweetList[-1]
    
    actions = webdriver.ActionChains(browser)
    actions.move_to_element(send)
    #actions.click()
    actions.send_keys(Keys.PAGE_DOWN)
    actions.perform()
    scroll += 1
    
    print 'Tweets collected so far: ' + str(len(tweetList))
    print 'Number of page scrolls: ' + str(scroll)
    print '***********************'
    
    time.sleep(5)