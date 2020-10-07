# -*- coding: utf-8 -*-

from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup, NavigableString
import pickle
from artDefs import Piece
import csv
import page_data

def check_exists_by_link_text(driver, text):
    try:
        driver.find_element_by_link_text(text)
    except NoSuchElementException:
        return False
    return True

def write_to_csv(csv_file, pieces):
    with open(csv_file, mode='a') as pieces_file:
        p_writer = csv.writer(pieces_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for piece in pieces:
            act_row = []
            act_row.append(piece.name)
            act_row.append(piece.artist)
            act_row.append(piece.technique)
            for auction in piece.auctions:
                act_row.append(auction[0])
                act_row.append(auction[1])
            p_writer.writerow(act_row)


with open('pieces.csv', mode='w') as pieces_file:
        p_writer = csv.writer(pieces_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ["Tytuł", "Artysta", "Informacje dodatkowe"]
        
        for i in range(0,100): # max(hist2, key=int)
            cur_date = "data aukcji nr " + str(i+1)
            header.append(cur_date)
            cur_price = "cena aukcji nr " + str(i+1)
            header.append(cur_price)
        p_writer.writerow(header)


driver = webdriver.Firefox()
driver.get("http://www.artinfo.pl/pl/uzytkownicy/")
time.sleep(1)
# Extract lists of "buyers" and "prices" based on xpath.
username = driver.find_element_by_xpath("//*[@name='email']")
password = driver.find_element_by_xpath("//*[@name='pass1']")

# username.send_keys(page_data.my_login)
# password.send_keys(page_data.my_passw)
username.send_keys(page_data.login)
password.send_keys(page_data.passw)
time.sleep(2)
login_attempt = driver.find_element_by_xpath("//*[@value='Zaloguj']").click()
# login_attempt.submit()
print("submitted")
time.sleep(1)

driver.get(page_data.wizy)
last_visited_artsts_page = page_data.wizy
sleep_count = 0
pages_no = 0
while check_exists_by_link_text(driver, "następna"):
    pieces =[]
    soup = BeautifulSoup(driver.page_source, 'lxml')

    list_of_artists = soup.find('div', class_='artistList')
    for artist_line in list_of_artists.findAll('div',attrs={'class': None}):
        if sleep_count >= 20:
            time.sleep(40)
            sleep_count = 0
        else:
            sleep_count += 1
        artist_a = artist_line.find('a')
        if artist_a['href'] != page_data.artysta:
            cur_artist = artist_a.contents[0]
            driver.get(artist_a['href'])
            mid_page = BeautifulSoup(driver.page_source, 'lxml')
            for option in mid_page.findAll('a', class_='bigText auctionObjectsHeader'):
                if option.contents[0] == page_data.archiwum_str or option.contents[0] == page_data.archiwum_str_short:
                    driver.get(option['href']+';category:0;sale_condition:1;product_category:27')
                    while check_exists_by_link_text(driver, "następna"):
                        # links_obj = driver.find_elements_by_xpath("//*[@class='auctionObjectOverlayLink']")
                        # for link in links_obj:
                        #     links.append(link.get_attribute('href'))
                        auction_page = BeautifulSoup(driver.page_source, 'lxml')

                        for auction in auction_page.find_all('div', class_='auctionSingleObject'):
                            leftSide = auction.find('span', {"class":"leftSide"})
                            inner_text = [element for element in leftSide if isinstance(element, NavigableString)]
                            # cur_artist = inner_text[0].replace("\t", "")
                            # cur_artist = cur_artist.replace("\n", "")
                            cur_price = auction.find('p', {"class":"soldPrice"})
                            if cur_price != None: 
                            # TODO: sformatowac cene na inta i cur_date sensownie
                                cur_piece_name = auction.find('p', {"class":"auctionObjectName mediumText"}).text
                                cur_technique = auction.find('p', {"class":"auctionObjectShort mediumText"}).text#next_element.strip()
                                
                                cur_price = cur_price.text# .contents[0].strip() # TODO: to na razie wskazuje na element "cena wywoławcza", trzeba dać do kolejenego elementu
                                cur_price = ''.join(i for i in cur_price if i.isdigit())
                                date_wrapper = auction.find('div', {"class":"mediumDownText"})
                                if date_wrapper != None:
                                    cur_date = date_wrapper.find('b').text
                                else:
                                    cur_date = 'brak daty'
                                is_in_pieces = False
                                for piece in pieces:
                                    if piece.name == cur_piece_name and piece.artist == cur_artist:
                                        piece.append_auctions(cur_date, cur_price)
                                        is_in_pieces = True
                                        print("dzielo {} juz jest na liscie".format(cur_piece_name))
                                        break
                                if not is_in_pieces:
                                    new_piece = Piece(cur_piece_name, cur_artist, cur_technique)
                                    new_piece.append_auctions(cur_date, cur_price)
                                    pieces.append(new_piece)


                        next_page_button = driver.find_element_by_link_text("następna")
                        driver.get(next_page_button.get_attribute('href'))
                    
                    auction_page = BeautifulSoup(driver.page_source, 'lxml')
                    for auction in auction_page.find_all('div', class_='auctionSingleObject'):
                        leftSide = auction.find('span', {"class":"leftSide"})
                        inner_text = [element for element in leftSide if isinstance(element, NavigableString)]
                        # cur_artist = inner_text[0].replace("\t", "")
                        # cur_artist = cur_artist.replace("\n", "")
                        cur_price = auction.find('p', {"class":"soldPrice"})
                        if cur_price != None: 
                            # TODO: sformatowac cene na inta i cur_date sensownie
                            cur_piece_name = auction.find('p', {"class":"auctionObjectName mediumText"}).text
                            cur_technique = auction.find('p', {"class":"auctionObjectShort mediumText"}).text#next_element.strip()
                            cur_price = cur_price.text # contents[0].strip() # TODO: to na razie wskazuje na element "cena wywoławcza", trzeba dać do kolejenego elementu
                            cur_price = ''.join(i for i in cur_price if i.isdigit())
                            
                            date_wrapper = auction.find('div', {"class":"mediumDownText"})
                            if date_wrapper != None:
                                cur_date = date_wrapper.find('b').text
                            else:
                                cur_date = 'brak daty'
                            is_in_pieces = False
                            for piece in pieces:
                                if piece.name == cur_piece_name and piece.artist == cur_artist:
                                    piece.append_auctions(cur_date, cur_price)
                                    is_in_pieces = True
                                    print("dzielo {} juz jest na liscie".format(cur_piece_name))
                                    break
                            if not is_in_pieces:
                                new_piece = Piece(cur_piece_name, cur_artist, cur_technique)
                                new_piece.append_auctions(cur_date, cur_price)
                                pieces.append(new_piece)
    write_to_csv('pieces.csv', pieces)
    pages_no += 1
    if pages_no >= 5:
        break             
    driver.get(last_visited_artsts_page)
    next_page_button = driver.find_element_by_link_text("następna")
    link_to_next_page = next_page_button.get_attribute('href')
    driver.get(link_to_next_page)
    last_visited_artsts_page = link_to_next_page



pickle_out = open("pieces2.pickle","wb")
pickle.dump(pieces, pickle_out)
pickle_out.close()
  


# TODO: przeleciec po wszytskich stronach [1][2][3][4] 


# for link in links:
#     scrap_content(driver, link)

#     auction_name = driver.find_element_by_xpath("//*[@class='auctionName mediumBig']")
#     image_description = driver.find_element_by_xpath("//*[@class='productShort']")
#     print(image_description.text)
#     print(auction_name.text)


# title = driver.find_elements_by_xpath('//div[@class="loginPageTitle"]')
# print(title[0].text)
driver.close()
