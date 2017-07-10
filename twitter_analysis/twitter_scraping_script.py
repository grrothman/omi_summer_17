from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import local_config
import json

def write_file(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def scrape(browser, limit = 100):
    # Collect tweets
    tweetList = []
    scroll = 0
    prior_length = 0
    print('Collecting approx. {LIMIT} tweets'.format(LIMIT = limit))

    while len(tweetList) <= limit:
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

        if len(tweetList) - prior_length < 1:
            print('No new tweets found, ending search.')
            break

        prior_length = len(tweetList)

        time.sleep(5)

    return tweetList

def search(browser):
    # Find search bar
    si = browser.find_element_by_class_name('search-input')

    # Longer way to find search bar
    # tb = browser.find_element_by_css_selector(".topbar.js-topbar")
    # nav = tb.find_element_by_css_selector(".global-nav")
    # nav_in = nav.find_element_by_css_selector(".global-nav-inner")
    # con = nav_in.find_element_by_css_selector(".container")
    # pull = con.find_element_by_css_selector(".pull-right.nav-extras")
    # # search = pull.find_element_by_css_selector(".search")
    # form = pull.find_element_by_css_selector(".t1-form.form-search.js-search-form")
    # si = form.find_element_by_css_selector(".search-input")

    # Find Advanced Search
    si.send_keys('dummy')
    si.send_keys(Keys.RETURN)
    time.sleep(2)
    browser.find_element_by_class_name('SidebarFilterModule-toggle').click()
    browser.find_element_by_class_name('SidebarFilterModule-advanced').click()

    # Fill Advanced Search form - here is where critical terms are inputted!
    form = browser.find_element_by_css_selector('#doc').find_element_by_css_selector('#page-outer').find_element_by_css_selector('#page-container').find_element_by_css_selector('.search.advanced-search')
    ands = form.find_element_by_css_selector('[name=ands]')
    ands.send_keys('same drugs')
    # phrase = form.find_element_by_css_selector('[name=phrase]')
    # phrase.send_keys('same drugs')
    ors = form.find_element_by_css_selector('[name=ors]')
    ors.send_keys("#samedrugs #chancetherapper #coloringbook")
    # nots = form.find_element_by_css_selector('[name=nots]')
    # tag = form.find_element_by_css_selector('[name=tag]')

    # from_acct = form.find_element_by_css_selector('[name=from]')
    # from_acct.send_keys('@chancetherapper')

    since = form.find_element_by_css_selector('[name=since]')
    since.send_keys('2016-05-13')
    until = form.find_element_by_css_selector('[name=until]')
    until.click()
    until.send_keys('2016-06-13')

    # Make your search happen!
    sb = form.find_element_by_class_name('submit')
    sb.click()

    time.sleep(5)

    return browser

def login(browser, username, password):
    # Find and click on login button
    top_bar = browser.find_element_by_css_selector('.StreamsTopBar.StreamsTopBar--fixed.js-variableHeightTopBar')
    tall = top_bar.find_element_by_css_selector('.StreamsHero.StreamsHero--tall')
    bc = tall.find_element_by_css_selector('.StreamsHero-buttonContainer')
    bc.find_element_by_css_selector('.EdgeButton.EdgeButton--transparent.EdgeButton--medium.StreamsLogin.js-login').click()
    #bc.find_element_by_css_selector('.Button.StreamsLogin.js-login').click()

    # Enter login information
    browser.find_element_by_xpath("//input[contains(@name,'username')]").send_keys(username)
    browser.find_element_by_xpath("//input[contains(@name,'password')]").send_keys(password)
    browser.find_element_by_xpath("//input[contains(@name,'password')]").send_keys(Keys.RETURN)

    return browser

def open_main_browser(url):
    # Open Browser
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver.exe')
    # Navigate to main url
    browser.get(url)

    return browser

def main(main_url, username, password, limit):
    browser = open_main_browser(main_url)
    browser = login(browser, username, password)
    browser = search(browser)
    tweet_list = scrape(browser, limit = limit)
    write_file(tweet_list, 'chance_tweet_100.txt')

if __name__ == '__main__':
    main_url = 'http://twitter.com'
    username = local_config.username
    password = local_config.password
    limit = 1000
    main(main_url, username, password, limit)