from requests import request
from bs4 import BeautifulSoup

class Old_Receipt_Numbers(object):
    def __init__(self):
        self.__base_url = "http://invoice.apmall.tw/{}.htm"
        self.__blacklist = ['貳獎', '參獎', '肆獎', '伍獎', '陸獎']
        self.__years = list(range(92, 102))
        self.__months = [ [1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12] ]
        self.dates = [[y]+m for y in self.__years for m in self.__months]
        self.dates_text = list(map(self.__combine_dates, self.dates))[:-2]
        #self.urls = list(map(self.__base_url.format, self.dates_text))
    
    def __combine_dates(self, dates):
        return "{}/{}-{}".format(*dates) if len(dates) == 3 else None
    
    def process_topics_and_numbers(self, topics, numbers):
        if '增開' in topics and '陸獎' in topics:
            # additional sixth prize
            sixth_prizes = [n for n in numbers if len(n) == 3]
            rest = [n for n in numbers if n not in sixth_prizes]
            return {'special_prize' : [ numbers[0] ],
                    'grand_prize'   : [ numbers[1] ], 
                    'top_prize'     : numbers[2:]   , 
                    'sixth_prize'   : sixth_prizes  ,
                   }
        else:
            return {'special_prize' : [ numbers[0] ],
                    'grand_prize'   : [ numbers[1] ], 
                    'top_prize'     : numbers[2:]   ,
                    'sixth_prize'   : []            ,
                   }
    
    def get_prize_numbers(self, date_text):
        url = self.__base_url.format(date_text)
        print('Requesting from', url)
        resp = request("GET", url)
        
        if not resp.ok:
            print("Unavailable")
            return None
        
        soup = BeautifulSoup(resp.content.decode("utf-8"), 'html.parser')
        prize_numbers = soup.find_all(attrs={"class":"no"})
        prize_numbers = [p.text.replace(" ", "").replace("\n", "") for p in prize_numbers]
        topics = soup.find_all(attrs={"class":"story_reference_topic", "align":"center"})
        topics = [t.text.strip().replace(" ", "") for t in topics]
        topics = [item for item in topics if item not in self.__blacklist]
        return {date_text : self.process_topics_and_numbers(topics, prize_numbers)}
