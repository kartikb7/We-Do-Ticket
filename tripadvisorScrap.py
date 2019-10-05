#reference code:https://www.scrapehero.com/how-to-scrape-tripadvisor/

def hotel_scrap(MatchCity):
    locality=MatchCity
    userInputCheckin=input("Please enter checkin data as YYYY/MM/DD:")
    userInputCheckout=input("Please enter checkout data as YYYY/MM/DD:")
    checkin_date = datetime.strptime(userInputCheckin,"%Y/%m/%d")
    checkout_date = datetime.strptime(userInputCheckout,"%Y/%m/%d")
    checkIn = checkin_date.strftime("%Y/%m/%d")
    checkOut = checkout_date.strftime("%Y/%m/%d")
    sort="popularity"
    
    checkIn = checkin_date.strftime("%Y/%m/%d")
    checkOut = checkout_date.strftime("%Y/%m/%d")
    print ("Scraper Inititated for Locality:%s"%locality)
    # TA rendering the autocomplete list using this API
    print ("Finding search result page URL")
    geo_url = 'https://www.tripadvisor.com/TypeAheadJson?action=API&startTime='+str(int(time()))+'&uiOrigin=GEOSCOPE&source=GEOSCOPE&interleaved=true&types=geo,theme_park&neighborhood_geos=true&link_type=hotel&details=true&max=12&injectNeighborhoods=true&query='+locality
    api_response  = requests.get(geo_url, verify=False).json()
    #getting the TA url for th equery from the autocomplete response
    url_from_autocomplete = "http://www.tripadvisor.com"+api_response['results'][0]['url']
    print ('URL found %s'%url_from_autocomplete)
    geo = api_response['results'][0]['value']   
    #Formating date for writing to file 
    
    date = checkin_date.strftime("%Y_%m_%d")+"_"+checkout_date.strftime("%Y_%m_%d")
    #form data to get the hotels list from TA for the selected date
    form_data = {'changeSet': 'TRAVEL_INFO',
            'showSnippets': 'false',
            'staydates':date,
            'uguests': '2',
            'sortOrder':sort
    }
        #Referrer is necessary to get the correct response from TA if not provided they will redirect to home page
    headers = {
                            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
                            'Accept-Encoding': 'gzip,deflate',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Cache-Control': 'no-cache',
                            'Connection': 'keep-alive',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                            'Host': 'www.tripadvisor.com',
                            'Pragma': 'no-cache',
                            'Referer': url_from_autocomplete,
                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0',
                            'X-Requested-With': 'XMLHttpRequest'
                        }
    cookies=  {"SetCurrency":"USD"}
    print ("Downloading search results page")
    page_response  = requests.post(url = url_from_autocomplete,data=form_data,headers = headers, cookies = cookies, verify=False)
    print ("Parsing results ")
    parser = html.fromstring(page_response.text)
    hotel_lists = parser.xpath('//div[contains(@class,"listItem")]//div[contains(@class,"listing collapsed")]')
    hotel_data = []
    if not hotel_lists:
        hotel_lists = parser.xpath('//div[contains(@class,"listItem")]//div[@class="listing "]')
    
    for hotel in hotel_lists:
        XPATH_HOTEL_LINK = './/a[contains(@class,"property_title")]/@href'
        XPATH_REVIEWS  = './/a[@class="review_count"]//text()'
        XPATH_RANK = './/div[@class="popRanking"]//text()'
        XPATH_RATING = './/a[contains(@class,"rating")]/@alt'
        XPATH_HOTEL_NAME = './/a[contains(@class,"property_title")]//text()'
        XPATH_HOTEL_FEATURES = './/div[contains(@class,"common_hotel_icons_list")]//li//text()'
        XPATH_HOTEL_PRICE = './/div[contains(@data-sizegroup,"mini-meta-price")]/text()'
        XPATH_VIEW_DEALS = './/div[contains(@data-ajax-preserve,"viewDeals")]//text()' 
        XPATH_BOOKING_PROVIDER = './/div[contains(@data-sizegroup,"mini-meta-provider")]//text()'
    
        raw_booking_provider = hotel.xpath(XPATH_BOOKING_PROVIDER)
        raw_no_of_deals =  hotel.xpath(XPATH_VIEW_DEALS)
        raw_hotel_link = hotel.xpath(XPATH_HOTEL_LINK)
        raw_no_of_reviews = hotel.xpath(XPATH_REVIEWS)
        raw_rank = hotel.xpath(XPATH_RANK)
        raw_rating = hotel.xpath(XPATH_RATING)
        raw_hotel_name = hotel.xpath(XPATH_HOTEL_NAME)
        raw_hotel_features = hotel.xpath(XPATH_HOTEL_FEATURES)
        raw_hotel_price_per_night  = hotel.xpath(XPATH_HOTEL_PRICE)
    
        url = 'http://www.tripadvisor.com'+raw_hotel_link[0] if raw_hotel_link else  None
        reviews = ''.join(raw_no_of_reviews).replace("reviews","").replace(",","") if raw_no_of_reviews else 0 
        rank = ''.join(raw_rank) if raw_rank else None
        rating = ''.join(raw_rating).replace('of 5 bubbles','').strip() if raw_rating else None
        name = ''.join(raw_hotel_name).replace(',','-').strip() if raw_hotel_name else None
        hotel_features = ','.join(raw_hotel_features).replace(',',';')
    #         price_per_night = ''.join(raw_hotel_price_per_night).encode('utf-8').replace('\n','') if raw_hotel_price_per_night else None
        price_per_night = ''.join(raw_hotel_price_per_night).replace('\n','') if raw_hotel_price_per_night else None
        no_of_deals = re.findall("all\s+?(\d+)\s+?",''.join(raw_no_of_deals))
        booking_provider = ''.join(raw_booking_provider).strip() if raw_booking_provider else None
    
        if no_of_deals:
            no_of_deals = no_of_deals[0]
        else:
            no_of_deals = 0
            
        data = {
                    'hotel_name':name,
                    'url':url,
                    'locality':locality,
                    'reviews':reviews,
                    'tripadvisor_rating':rating,
                    'checkOut':checkOut,
                    'checkIn':checkIn,
                    'hotel_features':hotel_features,
                    'price_per_night':price_per_night,
                    'no_of_deals':no_of_deals,
                    'booking_provider':booking_provider
    
        }
        hotel_data.append(data)
    # data = parse(locality,checkin_date,checkout_date,sort)
    print(hotel_data)
    print ("Writing to output file tripadvisor_data.csv")
    with open('tripadvisor_data.csv','wb')as csvfile:
        fieldnames = ['hotel_name','url','locality','reviews','tripadvisor_rating','checkIn','checkOut','price_per_night','booking_provider','no_of_deals','hotel_features']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in  hotel_data:
            writer.writerow(row)