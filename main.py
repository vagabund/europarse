import asyncio
import parser as prs
import os

counter = 1
for key in prs.leagues.keys():
    print(key + " -> " + str(counter))
    counter += 1
selector_league = int(input("Выберите лигу: "))
chosen_league = prs.leagues_select[selector_league]
for club in chosen_league:
    print(club.name + " -> " + str(chosen_league.index(club) + 1))
selector_club = int(input("Выберите клуб: "))
chosen_club = chosen_league[selector_club - 1]
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
print(chosen_club.name)
asyncio.run(chosen_club.scrape())
chosen_club.data_frame()
os.system('pause')