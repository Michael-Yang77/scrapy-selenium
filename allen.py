import scrapy
import codecs
import csv
import datetime
from tutorial.items import Manual

class AllenSpider(scrapy.Spider):
    name = 'allen'
    filename = ''
    product_name=''
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

        for quote in response.css('.seriesop'):

            product = quote.css('a img::attr(alt)').get()

            url=quote.css('a::attr(href)').get()
            if(url == "/dlive-home/"):
                yield {'url': url}
                # yield scrapy.Request('https://www.allen-heath.com'+url, self.parse_sub_1, cb_kwargs=dict(product=product))
            elif(url == "/avantis/"):
                yield {'url': url}
                # yield scrapy.Request('https://www.allen-heath.com'+url, self.parse_sub_2, cb_kwargs=dict(product=product))
            elif(url == "/sq-series/"):
                yield {'url': url}
                # yield scrapy.Request('https://www.allen-heath.com'+url, self.parse_sub_3, cb_kwargs=dict(product=product))
            elif(url == "/key-series/qu-series/"):
                yield {'url': url}
                # yield scrapy.Request('https://www.allen-heath.com'+url, self.parse_sub_4, cb_kwargs=dict(product=product))
            elif(url == "/ahm-64/"):
                yield {'url': url}
                # yield scrapy.Request('https://www.allen-heath.com'+url, self.parse_sub_5, cb_kwargs=dict(product=product))
            elif(url == "https://www.allen-heath.com/everything-io/"):
                yield {'product': product}
                # yield scrapy.Request(url, self.parse_sub_6, cb_kwargs=dict(product=product))
            elif(url == "https://www.allen-heath.com/key-series/me/"):
                # yield {'product': product}
                yield scrapy.Request(url, self.parse_sub_7, cb_kwargs=dict(product=product))
            # elif(url == "https://www.allen-heath.com/key-series/zed-series/"):
            #     # yield {'product': product}
            #     yield scrapy.Request(url, self.parse_sub_2, cb_kwargs=dict(product=product))
            # elif(url == "https://www.allen-heath.com/dj-products/"):
            #     # yield {'product': product}
            #     yield scrapy.Request(url, self.parse_sub_2, cb_kwargs=dict(product=product))
            # elif(url == "https://www.allen-heath.com/product_series/gr-series/"):
            #     # yield {'product': product}
            #     yield scrapy.Request(url, self.parse_sub_2, cb_kwargs=dict(product=product))
            # elif(url == "https://www.allen-heath.com/series/xb/"):
            #     # yield {'product': product}
            #     yield scrapy.Request(url, self.parse_sub_2, cb_kwargs=dict(product=product))
            # elif(url == "https://www.allen-heath.com/series/discontinued/"):
            #     # yield {'product': product}
            #     yield scrapy.Request(url, self.parse_sub_2, cb_kwargs=dict(product=product))
            
            

    def parse_sub_1(self, response, product):

        for quote in response.css('.mega-menu-item-object-ahproducts'):

            sub_url=quote.css('a::attr(href)').get()
            product_name = quote.css('a::text').get()
            product = product
                
            yield scrapy.Request(sub_url, self.parse_get_content_1,  cb_kwargs=dict(product_name=product_name, product=product)) 
    def parse_get_content_1(self, response, product_name, product):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def sliceindex(x):
            i = 0
            for c in x:
                if c.isalpha():
                    i = i + 1
                    return i
                i = i + 1

        def upperfirst(x):
            i = sliceindex(x)
            return x[:i].upper() + x[i:]
        manual_url=''
        file_url=''
        fontname=''
        file_urls= response.css('div.prodocs div.docdetails h5 a[href*="pdf"]::attr(href)').getall()

        image_url=response.css('div#productcontent:nth-child(1) div.row p img').attrib['src']
        yield{ "image_url":image_url}
        
        product_name = product_name
        product = product
        ean_number=''

        product_url=response.url
        url_array=product_url.split('/')
        array_len=len(url_array)
        product_str=url_array[array_len-3]
        product_array=product_str.split('-')
       
        product_parent = ""
        file_pdfs=response.css('h5 a[href*=".pdf"]')
                  
        for file_pdf in file_pdfs:
            file_pdf_url=file_pdf.attrib['href']
            file_type=file_pdf.css('::text').get()
            
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
            manual['product_lang'] = 'en'

            manual['file_urls'] =  file_pdf_url 
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

    def parse_sub_2(self, response, product):
       
        manual_url=''
        file_url=''
        fontname=''
        file_urls= response.css('div.fl-module-button div.fl-node-content div.fl-button-has-icon a.fl-button::attr(href)').getall()

        image_url=response.css('div.fl-photo-img-jpg img').attrib['src']
        yield{ "image_url":image_url}
        product_name = response.css('ul#menu-footer-products-menu li.active a::text').get()
        yield {'name': product_name}
        product = product

        ean_number=''

        product_url=response.url
        url_array=product_url.split('/')
        array_len=len(url_array)
        product_str=url_array[array_len-3]
        product_array=product_str.split('-')

        product_parent = ""
        file_pdfs=response.css('div#docs div.fl-col-content div.fl-col-group div.fl-col-small')
       
        for file_pdf in file_pdfs:

            if(file_pdf.css('div.fl-module div.fl-module-content div.fl-button-wrap a').get() is not None):
                file_pdf_url=file_pdf.css('div.fl-module div.fl-module-content div.fl-button-wrap a').attrib['href']
                file_type=file_pdf.css('div.fl-module-content div.fl-rich-text span::text').get()
    
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
                manual['product_lang'] = 'en'

                manual['file_urls'] =  file_pdf_url 
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
        
    def parse_sub_3(self, response, product):

        for quote in response.css('div.fl-col-group-equal-height div.fl-col-small div.fl-col-content '):
            yield {'subtilte': quote.css('div.fl-module:nth-child(2) div.fl-module-content div.fl-rich-text p a::attr(href)').get()}
            if(quote.css('div.fl-module:nth-child(2) div.fl-module-content div.fl-rich-text p a span::text').get() == "SQ Dante" or quote.css('div.fl-module:nth-child(2) div.fl-module-content div.fl-rich-text p a span::text').get() == "SQ SLink" or quote.css('div.fl-module:nth-child(2) div.fl-module-content div.fl-rich-text p a span::text').get() == "SQ Waves" or quote.css('div.fl-module:nth-child(2) div.fl-module-content div.fl-rich-text p a span::text').get() == "SQ MADI"):
                sub_url=quote.css('div.fl-module:nth-child(2) div.fl-module-content div.fl-rich-text p a::attr(href)').get()
            else:
                sub_url='https://www.allen-heath.com' + quote.css('div.fl-module:nth-child(1) div.fl-photo-content a::attr(href)').get()

            product_name = quote.css('div.fl-module:nth-child(2) div.fl-module-content div.fl-rich-text p a span::text').get()
            product = product
            # yield{'sub_url':sub_url, 'product_name':product_name, 'product':product}                
            yield scrapy.Request(sub_url, self.parse_get_content_3,  cb_kwargs=dict(product_name=product_name, product=product)) 
    def parse_get_content_3(self, response, product_name, product):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def sliceindex(x):
            i = 0
            for c in x:
                if c.isalpha():
                    i = i + 1
                    return i
                i = i + 1

        def upperfirst(x):
            i = sliceindex(x)
            return x[:i].upper() + x[i:]
        manual_url=''
        file_url=''
        fontname=''

        file_urls= response.css('div.fl-module-content div.fl-button-has-icon a[href*="pdf"]::attr(href)').getall()

        image_url=response.css('div.fl-fade-left div.fl-photo-content img').attrib['src']
        yield{ "image_url":image_url}

        product_name = product_name
        product = product
        ean_number=''

        product_url=response.url
        url_array=product_url.split('/')
        array_len=len(url_array)
        product_str=url_array[array_len-3]
        product_array=product_str.split('-')

        product_parent = ""
        file_pdfs=response.css('div.fl-node-60892fc15cb50 div.fl-col-small')
        
        for file_pdf in file_pdfs:

            file_pdf_url=file_pdf.css('div.fl-module-button div.fl-button-has-icon a').attrib['href']
            file_type=file_pdf.css('div.fl-module-rich-text div.fl-rich-text h3::text').get()
           
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
            manual['product_lang'] = 'en'

            manual['file_urls'] =  file_pdf_url 
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
    def parse_sub_4(self, response, product):

        for quote in response.css('div.fl-col-group-equal-height div.fl-col-small div.fl-col-content div.fl-module:nth-child(2) div.fl-rich-text a'):
            # yield {'subtilte': quote.getall()}
            if( quote.css('a::attr(href)').get() != "/everything-io/"):
                sub_url='https://www.allen-heath.com' + quote.css('a::attr(href)').get()

            product_name = quote.css('a span::text').get()
            product = product
            # yield{'sub_urles':sub_url, 'product_name':product_name, 'product':product}                
            yield scrapy.Request(sub_url, self.parse_get_content_4,  cb_kwargs=dict(product_name=product_name, product=product)) 

    def parse_get_content_4(self, response, product_name, product):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def sliceindex(x):
            i = 0
            for c in x:
                if c.isalpha():
                    i = i + 1
                    return i
                i = i + 1

        def upperfirst(x):
            i = sliceindex(x)
            return x[:i].upper() + x[i:]
        manual_url=''
        file_url=''
        fontname=''

        file_urls= response.css('div.fl-module-content div.fl-button-has-icon a[href*="pdf"]::attr(href)').getall()

        image_url=response.css('div.fl-fade-left div.fl-photo-content img').attrib['src']
        yield{ "image_url":image_url}

        product_name = product_name
        product = product
        ean_number=''

        product_url=response.url
        url_array=product_url.split('/')
        array_len=len(url_array)
        product_str=url_array[array_len-3]
        product_array=product_str.split('-')

        product_parent = ""
        file_pdfs=response.css('div.fl-builder-content div.fl-row:nth-child(20)  div.fl-col-small')
        # yield{'lll':file_pdfs.getall()}
        for file_pdf in file_pdfs:

            file_pdf_url=file_pdf.css('div.fl-module-button div.fl-button-has-icon a').attrib['href']
            file_type=file_pdf.css('div.fl-module-rich-text div.fl-rich-text h3::text').get()
           
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
            manual['product_lang'] = 'en'

            manual['file_urls'] =  file_pdf_url 
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

    def parse_sub_5(self, response, product):
       
        manual_url=''
        file_url=''
        fontname=''
        # file_urls= response.css('div.fl-module-button div.fl-node-content div.fl-button-has-icon a.fl-button::attr(href)').getall()

        image_url=response.css('div.fl-photo-img-jpg img').attrib['src']
        yield{ "image_url":image_url}
        product_name = response.css('ul#menu-footer-products-menu li.active a::text').get()
        yield {'name': product_name}
        product = product

        ean_number=''

        product_url=response.url
        url_array=product_url.split('/')
        array_len=len(url_array)
        product_str=url_array[array_len-3]
        product_array=product_str.split('-')

        product_parent = ""
        file_pdfs=response.css('div#docs div.fl-row-content div.fl-col-group div.fl-col-small')
        yield{'sss':file_pdfs}
        for file_pdf in file_pdfs:

            
            file_pdf_url=file_pdf.css('div.fl-module div.fl-module-content div.fl-rich-text a').attrib['href']
            file_type=file_pdf.css('div.fl-module-content div.fl-rich-text p::text').get()

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
            manual['product_lang'] = 'en'

            manual['file_urls'] =  file_pdf_url 
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

    def parse_sub_6(self, response, product):

        for quote in response.css('.pp-gallery-item'):

            sub_url=quote.css('.pp-photo-gallery-content a::attr(href)').get()
            product_name = quote.css('.pp-photo-gallery-caption h3::text').get()
            product = product
                
            yield scrapy.Request(sub_url, self.parse_get_content_6,  cb_kwargs=dict(product_name=product_name, product=product))
    def parse_get_content_6(self, response, product_name, product):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def sliceindex(x):
            i = 0
            for c in x:
                if c.isalpha():
                    i = i + 1
                    return i
                i = i + 1

        def upperfirst(x):
            i = sliceindex(x)
            return x[:i].upper() + x[i:]
        manual_url=''
        file_url=''
        fontname=''

        # file_urls= response.css('div.prodocs div.docdetails h5 a[href*="pdf"]::attr(href)').getall()

        image_url=response.css('div#productcontent p img').attrib['src']
        yield{ "image_url":image_url}

        product_name = product_name
        product = product
        ean_number=''

        product_url=response.url
        url_array=product_url.split('/')
        array_len=len(url_array)
        product_str=url_array[array_len-3]
        product_array=product_str.split('-')

        product_parent = ""
        file_pdfs=response.css('div.proddocs div.docdetails ')
        # yield{'lll':file_pdfs.getall()}
        for file_pdf in file_pdfs:

            file_pdf_url=file_pdf.css('a').attrib['href']
            file_type=file_pdf.css('a::text').get()
           
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
            manual['product_lang'] = 'en'

            manual['file_urls'] =  file_pdf_url 
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

    def parse_sub_7(self, response, product):

        for quote in response.css('.hosect div.product_image '):

            sub_url=quote.css('p a::attr(href)').get()
            product_name = quote.css(' h3::text').get()
            product = product
            yield{'ssss'}
            yield scrapy.Request(sub_url, self.parse_get_content_7,  cb_kwargs=dict(product_name=product_name, product=product))
    def parse_get_content_7(self, response, product_name, product):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def sliceindex(x):
            i = 0
            for c in x:
                if c.isalpha():
                    i = i + 1
                    return i
                i = i + 1

        def upperfirst(x):
            i = sliceindex(x)
            return x[:i].upper() + x[i:]
        manual_url=''
        file_url=''
        fontname=''

        # file_urls= response.css('div.prodocs div.docdetails h5 a[href*="pdf"]::attr(href)').getall()

        image_url=response.css('div#productcontent div.col-sm-6 p img').attrib['src']
        yield{ "image_url":image_url}

        product_name = product_name
        product = product
        ean_number=''

        product_url=response.url
        url_array=product_url.split('/')
        array_len=len(url_array)
        product_str=url_array[array_len-3]
        product_array=product_str.split('-')

        product_parent = ""
        file_pdfs=response.css('div.proddocs div.docdetails ')
        # yield{'lll':file_pdfs.getall()}
        for file_pdf in file_pdfs:

            file_pdf_url=file_pdf.css('a').attrib['href']
            file_type=file_pdf.css('a::text').get()
           
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
            manual['product_lang'] = 'en'

            manual['file_urls'] =  file_pdf_url 
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



        
    
            
