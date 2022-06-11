import scrapy
import codecs
import csv
import datetime
from tutorial.items import Manual

class HeathSpider(scrapy.Spider):
    name = 'heath'
    filename = ''
  
    produ_url=''
    product_type=''

    start_urls = ['https://www.allen-heath.com/products/']

    def parse(self, response):
        self.filename = 'product_' + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '.csv'
        header = [
        'brand','product','product_parent', 'file_urls', 'type',"ean", 'url','thumb',"source"
        
        ]

        with open(self.filename, 'wb') as fp:
            fp.write(codecs.BOM_UTF8)

        with open(self.filename, 'a', newline='') as fp:
            csv.writer(fp).writerow(header)

        for quote in response.css('#menu-footer-products-menu li '):

            self.product_parent=quote.css('a::text').get()
            if(quote.css('a[href*="https://www.allen-heath.com"]')):    
                url =  quote.css('a::attr(href)').get()
            else:
                url='https://www.allen-heath.com' + quote.css('a::attr(href)').get()
            yield scrapy.Request(url, self.parse_author, cb_kwargs=dict(product_parent=self.product_parent)) 
    
    
    def parse_author(self, response, product_parent):
 
        for quote in response.css('a[href*="/ahproducts/"]'):
            if(quote.css('a[href*="https://www.allen-heath.com"]')):   
                sub_url=quote.css('a::attr(href)').get()
            else:
                sub_url="https://www.allen-heath.com" + quote.css('a::attr(href)').get()
            
            self.product_parent = product_parent
            yield scrapy.Request(sub_url, self.parse_get_content, cb_kwargs=dict(product_parent=self.product_parent))         

    def parse_get_content(self, response, product_parent):

        manual_url=''
        file_url=''
        fontname=''
        file_urls= response.css('a[href*="pdf"]::attr(href)').getall()
    
        image_url=response.css('div#productcontent p img').attrib['src']

        ean_number=''

        product_url=response.url
        url_array=product_url.split('/')
        product=url_array[4]
        
        file_pdfs=response.css('div.docdetails a[href*=".pdf"]')

       
        for file_pdf in file_pdfs:
            file_pdf_url=file_pdf.attrib['href']
            file_type=file_pdf.css('::text').get()
            product_parent = product_parent
            yield{"file_pdf_url":file_pdf.get()}      
            row = [
                # product_name,
                "Allen & Heath",                   
                product,
                product_parent,
                file_pdf_url,      
                file_type,              
                ean_number ,
                product_url,
                image_url, 
                "allen-heath.com"               

            ]
            manual = Manual()
            
            manual['brand'] = 'Allen & Heath'
            # manual['model'] = product_name
            manual['model_2'] = ''
            manual['product'] =product
            manual['product_parent']=product_parent
            manual['product_lang'] = ''

            manual['file_urls'] = [ file_pdf_url ]
            manual['type'] = file_type
            manual['files'] = []
            manual['eans']=ean_number

            manual['thumb'] = image_url
            manual['url'] = product_url
            manual['source'] = "allen-heath.com"
            with open(self.filename, 'a', newline='', encoding='utf-8') as fp:
                print(row)
                csv.writer(fp).writerow(row)
            yield manual
               
