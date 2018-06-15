import datetime
from requests import request
from bs4 import BeautifulSoup

class Prize_History(object):
    def __init__(self):
        self.base_url = "http://service.etax.nat.gov.tw/etw-main/web/ETW183W2_{}/"
        self.current_year = datetime.datetime.now().year
        self._date_list = self._get_lottery_dates(self.current_year)
        self.urls = list(map(self.base_url.format, self._date_list))
        self.maps = {
            'specialPrize' : 'special_prize',
            'grandPrize' : 'grand_prize',
            'firstPrize' : 'top_prize',   
            'addSixPrize' : 'sixth_prize',
           }
        
    @staticmethod
    def year_converter(year):
        return year - 1911
    
    def _extract_date_from_url(self, url):
        date = url.split('_')[1].replace('/', '')
        month = int(date[len(date)-2:])
        year = date[:len(date)-2]
        return '{}/{:02d}-{:02d}'.format(year, month, month+1)

    def _get_dates_in_a_year(self, converted_year):
        months = range(5,12,2) if converted_year <= 101 else range(1,12,2)
        year = str(converted_year) if converted_year > 101 else '101'
        return [year + '{:02d}'.format(m) for m in months]

    def _get_lottery_dates(self, current_year):
        year = Prize_History.year_converter(current_year)
        years = range(101, year+1)
        date_list = list(map(self._get_dates_in_a_year, years))
        date_list = [item for sublist in date_list for item in sublist]
        return date_list
    
    def get_prize_numbers(self, url):
        resp = request("GET", url)
        if not resp.ok:
            return None
        soup = BeautifulSoup(str(resp.content), 'html.parser')
        table = soup.find(attrs={'id':'tablet01'})
        numbers = table.find_all(attrs={'class':'number'})
        prize_numbers = {self.maps[ t.attrs['headers'][0] ]: str(t.contents[0]).strip().split("\\xe3\\x80\\x81") for t in numbers}
        dates = self._extract_date_from_url(url)
        return {dates : prize_numbers}
    
    def get_prize_dict(self):
        prize_dict = list(map(self.get_prize_numbers, self.urls))
        prize_dict = [p for p in prize_dict if p]
        return prize_dict
