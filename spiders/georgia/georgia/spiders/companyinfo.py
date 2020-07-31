import scrapy, requests

class CompanySpider(scrapy.Spider):
    name = "companyinfo"

    def start_requests(self):
        urls = [
            f"https://www.companyinfo.ge/en/corporations/{i}" for i in range(1, 50)
        ]
        
        # send requests before starting
        url_1 = "https://www.companyinfo.ge/en/corporations/1"

        resp_ = requests.get(url_1, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"})
        cookie_ = dict(resp_.cookies)

        for url in urls:
            yield scrapy.Request(url=url, cookies=cookie_, callback=self.parse)

    def parse(self, response):

        url = response.request.url

        if response.css('#corporation-attributes > tbody > tr:nth-child(1) > td:nth-child(2)::text') is None:
            yield response.follow(url, self.parse)

        _id = url.split("/")[-1]

        data = {
            'name': response.css('#corporation-attributes > tbody > tr:nth-child(1) > td:nth-child(2)::text').get(),
            'id_number': response.css('#corporation-attributes > tbody > tr:nth-child(2) > td:nth-child(2)::text').get(),
            'legal_form': response.css('#corporation-attributes > tbody > tr:nth-child(3) > td:nth-child(2)::text').get(),
            'registration_number': response.css('#corporation-attributes > tbody > tr:nth-child(4) > td:nth-child(2)::text').get(),
            'source_information': response.css('#corporation-attributes > tbody > tr:nth-child(5) > td:nth-child(2)::text').get().strip(),
            'address': response.css('#corporation-attributes > tbody > tr:nth-child(6) > td:nth-child(2)::text').get(),
            'email': response.css('#corporation-attributes > tbody > tr:nth-child(7) > td:nth-child(2)::text').get(),
            'web_id' : _id
        }

        g_link = url.replace("/en/", "/ka/")

        request = scrapy.Request(g_link, callback=self.parse_georgian)

        request.meta['item'] = data
        
        yield request

    def parse_georgian(slef, response):
        name_ka = response.css('#corporation-attributes > tbody > tr:nth-child(1) > td:nth-child(2)::text').get()

        data = response.meta['item']

        yield {
            'name_en': data["name"],
            'name_ka' : name_ka,
            'id_number': data["id_number"],
            'legal_form': data["legal_form"],
            'registration_number': data["registration_number"],
            'source_information': data["source_information"],
            'address': data["address"],
            'email': data["email"],
            'web_id' : data["web_id"]
        }