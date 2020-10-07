import pickle
from artDefs import Piece
import csv

# pickle_in = open("pieces.pickle","rb")
# pieces = pickle.load(pickle_in)

pickle_in = open("pieces2.pickle","rb")
pieces2 = pickle.load(pickle_in)

# hist = {}
# for piece in pieces:
#     act_lgth = len(piece.auctions)
#     if act_lgth in hist:
#         hist[act_lgth] += 1
#     else:
#         hist[act_lgth] = 1

# print(hist)

hist2 = {}
for piece in pieces2:
    act_lgth = len(piece.auctions)
    if act_lgth in hist2:
        hist2[act_lgth] += 1
    else:
        hist2[act_lgth] = 1

print(hist2)

# s = 0
# for k, v in hist.items():
#     s += v*k


s2 = 0
k_max = 0
for k, v in hist2.items():
    s2 += v*k
    # TODO zrobić to bardziej pytonowo, jakaś lambda?
    if k > k_max:
        k_max = k

# print(s)
print(s2)


with open('pieces.csv', mode='w') as pieces_file:
    p_writer = csv.writer(pieces_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header = ["Tytuł", "Artysta", "Informacje dodatkowe"]
    
    
    for hist_bin in range(k): # max(hist2, key=int)
        cur_date = "data aukcji nr " + str(hist_bin+1)
        header.append(cur_date)
        cur_price = "cena aukcji nr " + str(hist_bin+1)
        header.append(cur_price)
    p_writer.writerow(header)

    for piece in pieces2:
        act_row = []
        act_row.append(piece.name)
        act_row.append(piece.artist)
        act_row.append(piece.technique)
        for auction in piece.auctions:
            act_row.append(auction[0])
            act_row.append(auction[1])
        p_writer.writerow(act_row)