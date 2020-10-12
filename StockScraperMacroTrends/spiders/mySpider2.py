import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class Myspider2Spider(scrapy.Spider): # either scrapy.Spider or SrawlSpider

    name = 'mySpider2'

    allowed_domains = ['macrotrends.net']
    # start_urls = ['https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/pe-ratio', 
    # 'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/price-sales',
    # 'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/price-book',
    # 'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/price-fcf']

    # start_urls = ['https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/revenue',
    # 'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/ebitda',
    # 'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/net-income',
    # 'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/shares-outstanding']

    # start_urls = ['https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/total-assets',
    # 'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/total-liabilities',
    # 'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/long-term-debt',
    # 'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/total-share-holder-equity',
    # 'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/cash-on-hand']

    # start_urls = ['https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/current-ratio',
    #     'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/quick-ratio',
    #     'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/debt-equity-ratio',
    #     'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/roe',
    #     'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/roa',
    #     'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/roi',
    #     'https://www.macrotrends.net/stocks/charts/MSFT/miscrosoft/return-on-tangible-equity']

    with open ('links.txt', 'r') as f:
        start_urls = f.readlines()

    def process_general(self, response, indicator):
        selector = Selector(text=response.body)
        out = response.xpath('//*[@id="style-1"]/div[2]/table/tbody')
        for row in out.css('tr'):
            r = []
            for td in row.css('td'):
                val = ''.join(td.xpath('.//text()').extract())
                if val == '':
                    val = '?'
                r.append(val)
            r.insert(0, (response.url).rsplit('/', 3)[-3])
            r.insert(0, (response.url).rsplit('/', 3)[-1])
            r[-1] = r[-1].replace('$', '')
            r[-1] = r[-1].replace(',', '')
            r = ','.join(r)
            r += "\n"
            with open ('dump.txt', 'a') as f:
                f.writelines(r)

    def process_column(self, response, col_id, indicator):
        selector = Selector(text=response.body)
        out = response.xpath('//*[@id="style-1"]/table/tbody')
        ticker = (response.url).rsplit('/', 3)[-3]
        for row in out.css('tr'):
            r = []
            for td in row.css('td'):
                val = ''.join(td.xpath('.//text()').extract())
                if val == '':
                    val = '?'
                r.append(val)
            # r = row.css('td::text').getall()
            r = [r[0], r[col_id]]
            r.insert(0, ticker)
            r.insert(0, indicator)
            r[-1] = r[-1].replace('$', '')
            r[-1] = r[-1].replace(',', '')
            r = ','.join(r)
            r += "\n"
            with open ('dump.txt', 'a') as f:
                f.writelines(r)

    def parse(self, response):
        print(response.url)
        indicator = (response.url).rsplit('/', 3)[-1]
        if indicator == 'pe-ratio':
            self.process_column(response, 3, 'PE')
            self.process_column(response, 2, 'ttmNetEPS')
            self.process_column(response, 1, 'stockPrice')
        if indicator == 'price-sales':
            self.process_column(response, 3, 'PS')
            self.process_column(response, 2, 'ttmSalesPerShare')
        if indicator == 'price-book':
            self.process_column(response, 3, 'PB')
            self.process_column(response, 2, 'BVPS')
        if indicator == 'price-fcf':
            self.process_column(response, 3, 'PriceFCF')
            self.process_column(response, 2, 'ttmFCFps')
        if indicator == 'current-ratio':
            self.process_column(response, 3, 'CurrentRatio')
            self.process_column(response, 2, 'CurrentLiabilities')
            self.process_column(response, 1, 'CurrentAssets')
        if indicator == 'quick-ratio':
            self.process_column(response, 3, 'QuickRatio')
            self.process_column(response, 1, 'CurrentAssetsInventory')
        if indicator == 'debt-equity-ratio':
            self.process_column(response, 3, 'DE')
        if indicator == 'roe':
            self.process_column(response, 3, 'ROE')
            self.process_column(response, 1, 'ttmNetIncome')
        if indicator == 'roa':
            self.process_column(response, 3, 'ROA')
        if indicator == 'roi':
            self.process_column(response, 3, 'ROI')
            self.process_column(response, 2, 'LTinvestAndDebt')
        if indicator == 'return-on-tangible-equity':
            self.process_column(response, 3, 'RoTangibleEquity')
            self.process_column(response, 2, 'TangibleEquity')
        if indicator in ['revenue',
                        'ebitda',
                        'net-income',
                        'shares-outstanding',
                        'operating-income',
                        'total-assets',
                        'total-liabilities',
                        'long-term-debt',
                        'total-share-holder-equity',
                        'cash-on-hand']:
            self.process_general(response, indicator)