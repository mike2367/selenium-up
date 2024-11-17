## Examples 

### Work Flow
```python
from Workflow import Workflow
from SaveToolKit import SaveToolKit
from ParseToolKit import ParseToolKit

url = "https://accounts.douban.com/passport/login"


class Spider(Workflow):
    def main_driver_flow(self):
        return 0
    def parse_flow(self, p_input:any):
        return ParseToolKit.table_print(p_input, log=False)

    def save_flow(self, s_input:any):
        return SaveToolKit().csv_save(s_input)
    
# uses the default chrome driver with XPATH
spider = Spider(url)
spider.run()
```


### Slider Movement
```python
def main_driver_flow(self):
        """
        slide 
        """
        self.driver.get("https://accounts.douban.com/passport/login") # douban login page
        action = self.driver_action
        action.click_element('//*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]', "密码登录")
        # input username and password
        action.input_keys('//*[@id="username"]', "11111111111")
        action.input_keys('//*[@id="password"]', "11")
        # click login
        action.click_element('//*[@id="account"]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a', "登录")
        # switch to slider iframe and move the slider right for 200 pixels
        action.frame_switch(['//div[@id="tcaptcha_transform_dy"]/iframe', 
                                         (self.driver_action.slide_horizontal,
                                          ('/html/body/div/div[3]/div[2]/div[6]', 200))])
```


### Page Scroll Down
```python
def main_driver_flow(self):
        """
        scroll 
        """
        self.driver.get("https://www.baidu.com")
        # input search keys and click search
        self.driver_action.input_keys('//*[@id="kw"]', 'test')
        self.driver_action.click_element('//*[@id="su"]', 'Search Button')
        # scroll down to the bottom slowly
        self.driver_action.scroll_down()
```

### Window switch
```python
def main_driver_flow(self):
        """
        window switch 
        """
        # Condition Setting, two pages in different tabs
        self.driver.get("https://accounts.douban.com/passport/login")
        self.driver.switch_to.new_window('window')
        self.driver.get("https://www.baidu.com")
        
        # search than fast scroll in the second tab
        self.driver_action.input_keys('//*[@id="kw"]', 'test')
        self.driver_action.click_element('//*[@id="su"]', 'Search Button')
        self.driver_action.scroll_down(slowly=False)
        
        # switch back to the first page(index 0) then input username
        self.driver_action.window_switch([0, 
        (self.driver_action.click_element, ('//*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]', "密码登录")),
        (self.driver_action.input_keys, ('//*[@id="username"]', "11111111111")),
        ])
```