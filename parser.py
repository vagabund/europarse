import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup


club_links = {
    'Chelsea': 'https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats',
    'Manchester City': 'https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats',
    'West Ham': 'https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats',
    'Liverpool': 'https://fbref.com/en/squads/822bd0ba/Liverpool-Stats',
    'Arsenal': 'https://fbref.com/en/squads/18bb7c10/Arsenal-Stats',
    'Manchester United': 'https://fbref.com/en/squads/19538871/Manchester-United-Stats',
    'Brighton': 'https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats',
    'Wolverhampton Wanderers': 'https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats',
    'Tottenham': 'https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats',
    'Crystal Palace': 'https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats',
    'Everton': 'https://fbref.com/en/squads/d3fd31cc/Everton-Stats',
    'Leicester': 'https://fbref.com/en/squads/a2d435b3/Leicester-City-Stats',
    'Southampton': 'https://fbref.com/en/squads/33c895d4/Southampton-Stats',
    'Brentford': 'https://fbref.com/en/squads/cd051869/Brentford-Stats',
    'Leeds': 'https://fbref.com/en/squads/5bfb9659/Leeds-United-Stats',
    'Aston Villa': 'https://fbref.com/en/squads/8602292d/Aston-Villa-Stats',
    'Watford': 'https://fbref.com/en/squads/2abfe087/Watford-Stats',
    'Burnley': 'https://fbref.com/en/squads/943e8050/Burnley-Stats',
    'Newcastle United': 'https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats',
    'Norwich': 'https://fbref.com/en/squads/1c781004/Norwich-City-Stats',

    'Napoli': 'https://fbref.com/en/squads/d48ad4ff/Napoli-Stats',
    'AC Milan': 'https://fbref.com/en/squads/dc56fe14/Milan-Stats',
    'Inter': 'https://fbref.com/en/squads/d609edc0/Internazionale-Stats',
    'Atalanta': 'https://fbref.com/en/squads/922493f3/Atalanta-Stats',
    'Roma': 'https://fbref.com/en/squads/cf74a709/Roma-Stats',
    'Juventus': 'https://fbref.com/en/squads/e0652b02/Juventus-Stats',
    'Bologna': 'https://fbref.com/en/squads/1d8099f8/Bologna-Stats',
    'Fiorentina': 'https://fbref.com/en/squads/421387cf/Fiorentina-Stats',
    'Lazio': 'https://fbref.com/en/squads/7213da33/Lazio-Stats',
    'Verona': 'https://fbref.com/en/squads/0e72edf2/Hellas-Verona-Stats',
    'Empoli': 'https://fbref.com/en/squads/a3d88bd8/Empoli-Stats',
    'Sassuolo': 'https://fbref.com/en/squads/e2befd26/Sassuolo-Stats',
    'Torino': 'https://fbref.com/en/squads/105360fe/Torino-Stats',
    'Udinese': 'https://fbref.com/en/squads/04eea015/Udinese-Stats',
    'Sampdoria': 'https://fbref.com/en/squads/8ff9e3b3/Sampdoria-Stats',
    'Venezia': 'https://fbref.com/en/squads/af5d5982/Venezia-Stats',
    'Spezia': 'https://fbref.com/en/squads/68449f6d/Spezia-Stats',
    'Genoa': 'https://fbref.com/en/squads/658bf2de/Genoa-Stats',
    'Cagliari': 'https://fbref.com/en/squads/c4260e09/Cagliari-Stats',
    'Salernitana': 'https://fbref.com/en/squads/c5577084/Salernitana-Stats',

    'Real Madrid': 'https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats',
    'Atletico Madrid': 'https://fbref.com/en/squads/db3b9613/Atletico-Madrid-Stats',
    'Real Sociedad': 'https://fbref.com/en/squads/e31d1cd9/Real-Sociedad-Stats',
    'Sevilla': 'https://fbref.com/en/squads/ad2be733/Sevilla-Stats',
    'Real Betis': 'https://fbref.com/en/squads/fc536746/Real-Betis-Stats',
    'Rayo Vallecano': 'https://fbref.com/en/squads/98e8af82/Rayo-Vallecano-Stats',
    'Barcelona': 'https://fbref.com/en/squads/206d90db/Barcelona-Stats',
    'Athletic Club': 'https://fbref.com/en/squads/2b390eca/Athletic-Club-Stats',
    'Espanyol': 'https://fbref.com/en/squads/a8661628/Espanyol-Stats',
    'Osasuna': 'https://fbref.com/en/squads/03c57e2b/Osasuna-Stats',
    'Valencia': 'https://fbref.com/en/squads/dcc91a7b/Valencia-Stats',
    'Villarreal': 'https://fbref.com/en/squads/2a8183b3/Villarreal-Stats',
    'Celta Vigo': 'https://fbref.com/en/squads/f25da7fb/Celta-Vigo-Stats',
    'Mallorca': 'https://fbref.com/en/squads/2aa12281/Mallorca-Stats',
    'Granada': 'https://fbref.com/en/squads/a0435291/Granada-Stats',
    'Alaves': 'https://fbref.com/en/squads/8d6fd021/Alaves-Stats',
    'Elche': 'https://fbref.com/en/squads/6c8b07df/Elche-Stats',
    'Cadiz': 'https://fbref.com/en/squads/ee7c297c/Cadiz-Stats',
    'Getafe': 'https://fbref.com/en/squads/7848bd64/Getafe-Stats',
    'Levante': 'https://fbref.com/en/squads/9800b6a1/Levante-Stats',

    'Bayern Munich': 'https://fbref.com/en/squads/054efa67/Bayern-Munich-Stats',
    'Borussia Dortmund': 'https://fbref.com/en/squads/add600ae/Dortmund-Stats',
    'Bayer Leverkusen': 'https://fbref.com/en/squads/c7a9f859/Bayer-Leverkusen-Stats',
    'Union Berlin': 'https://fbref.com/en/squads/7a41008f/Union-Berlin-Stats',
    'Freiburg': 'https://fbref.com/en/squads/a486e511/Freiburg-Stats',
    'Hoffenheim': 'https://fbref.com/en/squads/033ea6b8/Hoffenheim-Stats',
    'Wolfsburg': 'https://fbref.com/en/squads/4eaa11d7/Wolfsburg-Stats',
    'RasenBallsport Leipzig': 'https://fbref.com/en/squads/acbb6a5b/RB-Leipzig-Stats',
    'Mainz 05': 'https://fbref.com/en/squads/a224b06a/Mainz-05-Stats',
    'FC Cologne': 'https://fbref.com/en/squads/bc357bf7/Koln-Stats',
    'Borussia M.Gladbach': 'https://fbref.com/en/squads/32f3ee20/Monchengladbach-Stats',
    'Eintracht Frankfurt': 'https://fbref.com/en/squads/f0ac8ee6/Eintracht-Frankfurt-Stats',
    'Bochum': 'https://fbref.com/en/squads/b42c6323/Bochum-Stats',
    'Hertha Berlin': 'https://fbref.com/en/squads/2818f8bc/Hertha-BSC-Stats',
    'VfB Stuttgart': 'https://fbref.com/en/squads/598bc722/Stuttgart-Stats',
    'Augsburg': 'https://fbref.com/en/squads/0cdc4311/Augsburg-Stats',
    'Arminia Bielefeld': 'https://fbref.com/en/squads/247c4b67/Arminia-Stats',
    'Greuther Fuerth': 'https://fbref.com/en/squads/12192a4c/Greuther-Furth-Stats',

    'Paris Saint Germain': 'https://fbref.com/en/squads/e2d8892c/Paris-Saint-Germain-Stats',
    'Marseille': 'https://fbref.com/en/squads/5725cc7b/Marseille-Stats',
    'Rennes': 'https://fbref.com/en/squads/b3072e00/Rennes-Stats',
    'Nice': 'https://fbref.com/en/squads/132ebc33/Nice-Stats',
    'Lens': 'https://fbref.com/en/squads/fd4e0f7d/Lens-Stats',
    'Strasbourg': 'https://fbref.com/en/squads/c0d3eab4/Strasbourg-Stats',
    'Monaco': 'https://fbref.com/en/squads/fd6114db/Monaco-Stats',
    'Angers': 'https://fbref.com/en/squads/69236f98/Angers-Stats',
    'Montpellier': 'https://fbref.com/en/squads/281b0e73/Montpellier-Stats',
    'Lyon': 'https://fbref.com/en/squads/d53c0b06/Lyon-Stats',
    'Brest': 'https://fbref.com/en/squads/fb08dbb3/Brest-Stats',
    'Lille': 'https://fbref.com/en/squads/cb188c0c/Lille-Stats',
    'Nantes': 'https://fbref.com/en/squads/d7a486cd/Nantes-Stats',
    'Reims': 'https://fbref.com/en/squads/7fdd64e0/Reims-Stats',
    'Troyes': 'https://fbref.com/en/squads/54195385/Troyes-Stats',
    'Lorient': 'https://fbref.com/en/squads/d2c87802/Lorient-Stats',
    'Clermont Foot': 'https://fbref.com/en/squads/d9676424/Clermont-Foot-Stats',
    'Bordeaux': 'https://fbref.com/en/squads/123f3efe/Bordeaux-Stats',
    'Metz': 'https://fbref.com/en/squads/f83960ae/Metz-Stats',
    'Saint-Etienne': 'https://fbref.com/en/squads/d298ef2c/Saint-Etienne-Stats',

    'Zenit St. Petersburg': 'https://fbref.com/en/squads/98ce363d/Zenit-Stats',
    'Dinamo Moscow': 'https://fbref.com/en/squads/541a280b/Dynamo-Moscow-Stats',
    'PFC Sochi': 'https://fbref.com/en/squads/011c18c5/Sochi-Stats',
    'CSKA Moscow': 'https://fbref.com/en/squads/f0c0c2c2/CSKA-Moscow-Stats',
    'FC Krasnodar': 'https://fbref.com/en/squads/fa11a9cc/Krasnodar-Stats',
    'Lokomotiv Moscow': 'https://fbref.com/en/squads/5a8dc328/Lokomotiv-Moscow-Stats',
    'FK Akhmat': 'https://fbref.com/en/squads/8aa1135c/Akhmat-Grozny-Stats',
    'Krylya Sovetov Samara': 'https://fbref.com/en/squads/483ffd93/Samara-Stats',
    'Spartak Moscow': 'https://fbref.com/en/squads/8c635914/Spartak-Moscow-Stats',
    'Rubin Kazan': 'https://fbref.com/en/squads/5625a7da/Rubin-Kazan-Stats',
    'Ural': 'https://fbref.com/en/squads/1920cf18/Ural-Yekaterinburg-Stats',
    'Arsenal Tula': 'https://fbref.com/en/squads/0bca3a9e/Arsenal-Tula-Stats',
    'Nizhny Novgorod': 'https://fbref.com/en/squads/c28444cc/Nizhny-Novgorod-Stats',
    'FC Rostov': 'https://fbref.com/en/squads/d60423ef/Rostov-Stats',
    'FC Ufa': 'https://fbref.com/en/squads/ec7fdeb7/Ufa-Stats',
    'Khimki': 'https://fbref.com/en/squads/224b0274/FC-Khimki-Stats'
}

HEADERS = {'Accept-Language': 'en-US,en;q=0.5', "User-Agent": "Mozilla/5.0 (X11; "
                                                              "Linux x86_64) "
                                                              "AppleWebKit/537"
                                                              ".36 (KHTML, "
                                                              "like Gecko) "
                                                              "Chrome/51.0.2704"
                                                              ".103 "
                                                              "Safari/537.36"}

class Club:
    def __init__(self, name, fbref_name, league="EPL"):
        self.name = name
        self.fbref_name = fbref_name
        self.league = league
        self.logo = None
        self.dates = []
        self.competitions = []
        self.venues = []
        self.results = []
        self.opponents = []
        self.goals_for = []
        self.goals_against = []
        self.goals_overall = []
        self.goal_minutes_for = []
        self.goal_minutes_against = []
        self.xg_for = []
        self.xg_against = []
        self.yellows = []
        self.subs = []
        self.subs_time = []
        self.variants = []
        self.goal_scorers = []
        self.yellows_for = []
        self.yellows_against = []
        self.link_fbref = club_links.get(self.name) + '#all_matchlogs'
    
    async def get_html_fbref(self):
        global HEADERS
        async with aiohttp.ClientSession() as session:
            async with session.get(self.link_fbref) as resp:
                assert resp.status == 200, "Connection fault"
                return await resp.text(errors='replace')

    async def get_reports_fbref(self):
        response = await self.get_html_fbref()
        links = []
        soup = BeautifulSoup(response, 'lxml')
        table = soup.find('table', {'id': 'matchlogs_for'})
        rows = table.find_all('tr')
        for row in rows:
            comp = row.find('td', {'data-stat': 'comp'})
            if comp is not None:
                a = comp.find('a')
                if a.text == 'Conf Lg' or a.text == 'Europa Lg' or a.text == 'Champions Lg':
                    report = row.find('td', {'data-stat': 'match_report'})
                    new_a = report.find('a')
                    if new_a is not None and new_a.text == "Match Report":
                        links.append(new_a['href'])
        return links

    async def parse_report_fbref(self, link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers=HEADERS) as resp:

                def extract_time(text):
                    temp_time = []
                    temp_list = list(text)
                    for element in temp_list:
                        if element.isnumeric():
                            temp_time.append(element)
                    new_string = ''.join(temp_time)
                    if len(new_string) > 2:
                        new_string = new_string[:2]
                    return int(new_string)

                def extract_date(text):
                    months = {
                        "January": "01",
                        "February": "02",
                        "March": "03",
                        "April": "04",
                        "May": "05",
                        "June": "06",
                        "July": "07",
                        "August": "08",
                        "September": "09",
                        "October": "10",
                        "November": "11",
                        "December": "12"
                    }
                    begin_index = text.index('–')
                    datespace = text[begin_index + 2:]
                    day = 0
                    if len(datespace[1]) == 2:
                        day = '0' + datespace[1][:1]
                    elif len(datespace[1]) == 3:
                        day = datespace[1][:2]
                    date = day + '.' + months.get(datespace[0]) + '.' + datespace[2][:4]
                    return date

                result = await resp.text(errors='replace')
                soup = BeautifulSoup(result, 'lxml')
                content = soup.find('div', {'id': 'content'})
                comp = content.find('h1')
                comp = comp.text.split()

                date = extract_date(comp)

                first_div = content.find('div')
                href = first_div.find('a')
                competition = href.text

                goals_for = 0
                goals_away = 0
                goal_scorers_for = []
                goal_scorers_away = []
                goal_minutes_for = []
                goal_minutes_away = []
                subs_in_home = []
                subs_in_away = []
                subs_minutes_home = []
                subs_minutes_away = []
                xg = []
                yellows = 0
                reds = 0
                subs = 0
                penalty = 0
                own_goals = 0
                yellows_for = 0
                yellows_away = 0
                subs_owns = 0

                variants = []

                if comp[:len(self.fbref_name.split(" "))] == self.fbref_name.split(" "):
                    venue = "Home"
                    vs_index = comp.index('vs.')
                    end_index = comp.index('Match')
                    opponent = " ".join(comp[vs_index + 1:end_index])
                else:
                    venue = "Away"
                    vs_index = comp.index('vs.')
                    opponent = " ".join(comp[:vs_index])

                scorebox = content.find('div', {'class': 'scorebox'})
                eventbox_for = scorebox.find('div', {'id': 'a'})
                for event in eventbox_for:
                    if event != "\n":
                        if event.find('div', {'class': 'event_icon goal'}):
                            goal_scorer = event.find('a')
                            goal_scorers_for.append(goal_scorer.text)
                            goal_minutes_for.append(extract_time(event.text))
                            goals_for += 1
                        if event.find('div', {'class': 'event_icon own_goal'}):
                            goal_scorer = event.find('a')
                            goal_scorers_for.append(goal_scorer.text)
                            goal_minutes_for.append(extract_time(event.text))
                            goals_for += 1
                        if event.find('div', {'class': 'event_icon penalty_goal'}):
                            goal_scorer = event.find('a')
                            goal_scorers_for.append(goal_scorer.text)
                            goal_minutes_for.append(extract_time(event.text))
                            goals_for += 1

                eventbox_away = scorebox.find('div', {'id': 'b'})
                for event in eventbox_away:
                    if event != "\n":
                        if event.find('div', {'class': 'event_icon goal'}):
                            goal_scorer = event.find('a')
                            goal_scorers_away.append(goal_scorer.text)
                            goal_minutes_away.append(extract_time(event.text))
                            goals_away += 1
                        if event.find('div', {'class': 'event_icon own_goal'}):
                            goal_scorer = event.find('a')
                            goal_scorers_away.append(goal_scorer.text)
                            goal_minutes_away.append(extract_time(event.text))
                            goals_away += 1
                        if event.find('div', {'class': 'event_icon penalty_goal'}):
                            goal_scorer = event.find('a')
                            goal_scorers_away.append(goal_scorer.text)
                            goal_minutes_away.append(extract_time(event.text))
                            goals_away += 1

                goals_for_first = []
                goals_for_second = []
                goals_away_first = []
                goals_away_second = []

                for i in goal_minutes_for:
                    if i <= 45:
                        goals_for_first.append(i)
                    else:
                        goals_for_second.append(i)

                for i in goal_minutes_away:
                    if i <= 45:
                        goals_away_first.append(i)
                    else:
                        goals_away_second.append(i)

                if goals_for > goals_away:
                    variants.append(1)
                elif goals_for < goals_away:
                    variants.append(2)
                else:
                    variants.append(3)

                if len(goals_for_first) > len(goals_away_first):
                    variants.append(4)
                elif len(goals_for_first) < len(goals_away_first):
                    variants.append(5)
                else:
                    variants.append(6)

                if len(goals_for_second) > len(goals_away_second):
                    variants.append(7)
                elif len(goals_for_second) < len(goals_away_second):
                    variants.append(8)
                else:
                    variants.append(9)

                if len(goals_for_first) + len(goals_away_first) > len(goals_for_second) + len(goals_away_second):
                    variants.append(10)
                elif len(goals_for_first) + len(goals_away_first) < len(goals_for_second) + len(goals_away_second):
                    variants.append(11)
                else:
                    variants.append(12)

                if goals_for + goals_away == 0:
                    variants.append(13)
                elif goals_for + goals_away == 1 or goals_for + goals_away == 2:
                    variants.append(14)
                elif goals_for + goals_away == 3 or goals_for + goals_away == 4:
                    variants.append(15)
                else:
                    variants.append(16)

                if goals_away == 0:
                    variants.append(17)

                if goals_for == 0:
                    variants.append(18)

                if goals_for > goals_away:
                    for i in range(len(goal_minutes_away)):
                        if goal_minutes_for[i] > goal_minutes_away[i]:
                            variants.append(19)
                            break
                elif goals_away > goals_for:
                    for i in range(len(goal_minutes_for)):
                        if goal_minutes_away[i] > goal_minutes_for[i]:
                            variants.append(20)
                            break
                else:
                    for i in range(len(goal_minutes_for)):
                        if goal_minutes_for[i] > goal_minutes_away[i]:
                            variants.append(19)
                            break
                        elif goal_minutes_away[i] > goal_minutes_for[i]:
                            variants.append(20)
                            break

                try:
                    if 1 <= min(goal_minutes_for) <= 45 and 1 <= min(goal_minutes_away) <= 45:
                        variants.append(21)
                except ValueError:
                    pass

                try:
                    if 46 <= max(goal_minutes_for) <= 90 and 46 <= max(goal_minutes_away) <= 90:
                        variants.append(22)
                except ValueError:
                    pass

                if len(goal_minutes_for) > 0 and len(goal_minutes_away) > 0:
                    if min(goal_minutes_for) < min(goal_minutes_away):
                        if 1 <= min(goal_minutes_for) <= 20:
                            variants.append(23)
                        elif 21 <= min(goal_minutes_for) <= 45:
                            variants.append(24)
                        else:
                            variants.append(25)
                    else:
                        if 1 <= min(goal_minutes_away) <= 20:
                            variants.append(23)
                        elif 21 <= min(goal_minutes_away) <= 45:
                            variants.append(24)
                        else:
                            variants.append(25)
                elif len(goal_minutes_away) == 0 and len(goal_minutes_for) > 0:
                    if 1 <= min(goal_minutes_for) <= 20:
                        variants.append(23)
                    elif 21 <= min(goal_minutes_for) <= 45:
                        variants.append(24)
                    else:
                        variants.append(25)
                elif len(goal_minutes_for) == 0 and len(goal_minutes_away) > 0:
                    if 1 <= min(goal_minutes_away) <= 20:
                        variants.append(23)
                    elif 21 <= min(goal_minutes_away) <= 45:
                        variants.append(24)
                    else:
                        variants.append(25)
                else:
                    pass

                if goals_for > goals_away:
                    winning_goal = goal_minutes_for[goals_away]
                    if 1 <= winning_goal <= 45:
                        variants.append(26)
                    elif 46 <= winning_goal <= 70:
                        variants.append(27)
                    elif 71 <= winning_goal <= 90:
                        variants.append(28)
                elif goals_away > goals_for:
                    winning_goal = goal_minutes_away[goals_for]
                    if 1 <= winning_goal <= 45:
                        variants.append(26)
                    elif 46 <= winning_goal <= 70:
                        variants.append(27)
                    elif 71 <= winning_goal <= 90:
                        variants.append(28)

                if goals_for > goals_away:
                    temp = goals_for - goals_away
                    if temp == 1:
                        variants.append(29)
                    elif temp == 2:
                        variants.append(30)
                    elif temp >= 3:
                        variants.append(31)
                else:
                    temp = goals_away - goals_for
                    if temp == 1:
                        variants.append(29)
                    elif temp == 2:
                        variants.append(30)
                    elif temp >= 3:
                        variants.append(31)

                for scorer in goal_scorers_for:
                    if goal_scorers_for.count(scorer) > 1:
                        variants.append(32)
                        break

                for scorer in goal_scorers_away:
                    if goal_scorers_away.count(scorer) > 1:
                        variants.append(32)
                        break

                events_home = soup.find_all('div', {'class': 'event a'})
                for event in events_home:
                    z = event.find_all('div')
                    for div in z:
                        if div.find('div', {'class': 'event_icon yellow_card'}):
                            yellows += 1
                            yellows_for += 1
                        if div.find('div', {'class': 'event_icon yellow_red_card'}) or div.find('div', {
                            'class': 'event_icon red_card'}):
                            reds += 1
                        if div.find('div', {'class': 'event_icon substitute_in'}):
                            subs_minutes_home.append(extract_time(event.text))
                            subs_in_home.append(div.a.text)
                            subs += 1
                            if venue == "Home":
                                subs_owns += 1
                        if div.find('div', {'class': 'event_icon penalty_goal'}):
                            penalty += 1
                        if div.find('div', {'class': 'event_icon own_goal'}):
                            own_goals += 1

                events_away = soup.find_all('div', {'class': 'event b'})
                for event in events_away:
                    z = event.find_all('div')
                    for div in z:
                        if div.find('div', {'class': 'event_icon yellow_card'}):
                            yellows += 1
                            yellows_away += 1
                        if div.find('div', {'class': 'event_icon yellow_red_card'}) or div.find('div', {
                            'class': 'event_icon red_card'}):
                            reds += 1
                        if div.find('div', {'class': 'event_icon substitute_in'}):
                            subs_minutes_away.append(extract_time(event.text))
                            subs_in_away.append(div.a.text)
                            subs += 1
                            if venue == "Away":
                                subs_owns += 1
                        if div.find('div', {'class': 'event_icon penalty_goal'}):
                            penalty += 1
                        if div.find('div', {'class': 'event_icon own_goal'}):
                            own_goals += 1

                if yellows <= 3:
                    variants.append(33)
                elif 4 <= yellows <= 5:
                    variants.append(34)
                else:
                    variants.append(35)

                if reds > 0 or own_goals > 0:
                    variants.append(36)

                if penalty > 0:
                    variants.append(37)

                if subs <= 5:
                    variants.append(38)

                try:
                    if 1 <= min(subs_minutes_home) <= 46 or 1 <= min(subs_minutes_away) <= 46:
                        variants.append(39)
                except ValueError:
                    pass

                for sub in subs_in_home:
                    if sub in goal_scorers_for:
                        variants.append(40)
                        break

                for sub in subs_in_away:
                    if sub in goal_scorers_away:
                        if variants.count(40) > 0:
                            pass
                        else:
                            variants.append(40)

                xg_div = content.find_all('div', {'class': 'score_xg'})
                if len(xg_div) != 0:
                    for element in xg_div:
                        xg.append(element.text)
                else:
                    xg.append("")
                    xg.append("")

                if venue == "Home":
                    scores_for = goals_for
                    scores_against = goals_away
                    scores_minutes_for = goal_minutes_for
                    scores_minutes_against = goal_minutes_away
                    score = str(scores_for) + ":" + str(scores_against)
                    goal_scorers = ';'.join(goal_scorers_for)
                    if scores_for > scores_against:
                        result = 'W'
                    elif scores_for == scores_against:
                        result = 'D'
                    else:
                        result = 'L'
                    xg_for = xg[0]
                    xg_against = xg[1]
                    subs_minutes = subs_minutes_home
                    yellows_club_for = yellows_for
                    yellows_club_against = yellows_away
                else:
                    scores_for = goals_away
                    scores_against = goals_for
                    scores_minutes_for = goal_minutes_away
                    scores_minutes_against = goal_minutes_for
                    score = str(scores_for) + ":" + str(scores_against)
                    goal_scorers = ';'.join(goal_scorers_away)
                    if scores_against > scores_for:
                        result = 'L'
                    elif scores_against == scores_for:
                        result = 'D'
                    else:
                        result = 'W'
                    xg_for = xg[1]
                    xg_against = xg[0]
                    subs_minutes = subs_minutes_away
                    yellows_club_for = yellows_away
                    yellows_club_against = yellows_for

                temp_minutes_for = map(str, scores_minutes_for)
                scores_minutes_for_final = " ".join(temp_minutes_for)

                temp_minutes_against = map(str, scores_minutes_against)
                scores_minutes_against_final = " ".join(temp_minutes_against)

                temp_subs_minutes = map(str, subs_minutes)
                subs_minutes_final = " ".join(temp_subs_minutes)

                temp_variants = map(str, variants)
                variants_final = "-".join(temp_variants)

                if yellows == 0 and reds == 0 and subs == 0 and own_goals == 0 and penalty == 0:
                    pass
                else:
                    return [date, competition, venue, result, opponent, scores_for, scores_against, score,
                            scores_minutes_for_final, scores_minutes_against_final, xg_for, xg_against, yellows,
                            subs_owns, subs_minutes_final, variants_final, goal_scorers, yellows_club_for,
                            yellows_club_against]
    async def scrape(self):
        tasks = []
        fbref_reports = await self.get_reports_fbref()
        for report in fbref_reports:
            new_link = 'https://fbref.com' + report
            task = asyncio.create_task(self.parse_report_fbref(new_link))
            tasks.append(task)
        data = await asyncio.gather(*tasks)
        for element in data:
            if element is not None:
                self.dates.append(element[0])
                self.competitions.append(element[1])
                self.venues.append(element[2])
                self.results.append(element[3])
                self.opponents.append(element[4])
                self.goals_for.append(element[5])
                self.goals_against.append(element[6])
                self.goals_overall.append(element[7])
                self.goal_minutes_for.append(element[8])
                self.goal_minutes_against.append(element[9])
                self.xg_for.append(element[10])
                self.xg_against.append(element[11])
                self.yellows.append(element[12])
                self.subs.append(element[13])
                self.subs_time.append(element[14])
                self.variants.append(element[15])
                self.goal_scorers.append(element[16])
                self.yellows_for.append(element[17])
                self.yellows_against.append(element[18])

    def data_frame(self):
        dates = pd.Series(self.dates)
        comps = pd.Series(self.competitions)
        venues = pd.Series(self.venues)
        results = pd.Series(self.results)
        opponents = pd.Series(self.opponents)
        scores = pd.Series(self.goals_overall)
        xg = pd.Series(self.xg_for)
        xg_a = pd.Series(self.xg_against)
        variants = pd.Series(self.variants)
        frame = {'дата': dates, 'турнир': comps, 'дом':venues, 'результат': results, 'противник': opponents,
                 'счёт': scores, 'xg': xg, 'xg_A': xg_a, 'варианты': variants}
        df = pd.DataFrame(frame)
        print(df.to_string())

chelsea = Club("Chelsea", "Chelsea", "EPL")
manchester_city = Club("Manchester City", "Manchester City", "EPL")
west_ham = Club("West Ham", "West Ham United", "EPL")
liverpool = Club("Liverpool", "Liverpool", "EPL")
arsenal = Club("Arsenal", "Arsenal", "EPL")
manchester_united = Club("Manchester United", "Manchester United", "EPL")
brighton = Club("Brighton", "Brighton & Hove Albion", "EPL")
wolverhampton = Club("Wolverhampton Wanderers", "Wolverhampton Wanderers", "EPL")
tottenham = Club("Tottenham", "Tottenham Hotspur", "EPL")
crystal_palace = Club("Crystal Palace", "Crystal Palace", "EPL")
everton = Club("Everton", "Everton", "EPL")
leicester = Club("Leicester", "Leicester City", "EPL")
southampton = Club("Southampton", "Southampton", "EPL")
brentford = Club("Brentford", "Brentford", "EPL")
leeds = Club("Leeds", "Leeds United", "EPL")
aston_villa = Club("Aston Villa", "Aston Villa", "EPL")
watford = Club("Watford", "Watford", "EPL")
burnley = Club("Burnley", "Burnley", "EPL")
newcastle = Club("Newcastle United", "Newcastle United", "EPL")
norwich = Club("Norwich", "Norwich City", "EPL")

napoli = Club("Napoli", "Napoli", "Serie A")
milan = Club("AC Milan", "Milan", "Serie A")
inter = Club("Inter", "Internazionale", "Serie A")
atalanta = Club("Atalanta", "Atalanta", "Serie A")
roma = Club("Roma", "Roma", "Serie A")
juventus = Club("Juventus", "Juventus", "Serie A")
bologna = Club("Bologna", "Bologna", "Serie A")
fiorentina = Club("Fiorentina", "Fiorentina", "Serie A")
lazio = Club("Lazio", "Lazio", "Serie A")
h_verona = Club("Verona", "Hellas Verona", "Serie A")
empoli = Club("Empoli", "Empoli", "Serie A")
sassuolo = Club("Sassuolo", "Sassuolo", "Serie A")
torino = Club("Torino", "Torino", "Serie A")
udinese = Club("Udinese", "Udinese", "Serie A")
sampdoria = Club("Sampdoria", "Sampdoria", "Serie A")
venezia = Club("Venezia", "Venezia", "Serie A")
spezia = Club("Spezia", "Spezia", "Serie A")
genoa = Club("Genoa", "Genoa", "Serie A")
cagliari = Club("Cagliari", "Cagliari", "Serie A")
salernitana = Club("Salernitana", "Salernitana", "Serie A")

real = Club("Real Madrid", "Real Madrid", "La Liga")
atletico = Club("Atletico Madrid", "Atlético Madrid", "La Liga")
real_sociedad = Club("Real Sociedad", "Real Sociedad", "La Liga")
sevilla = Club("Sevilla", "Sevilla", "La Liga")
betis = Club("Real Betis", "Real Betis", "La Liga")
rayo = Club("Rayo Vallecano", "Rayo Vallecano", "La Liga")
barcelona = Club("Barcelona", "Barcelona", "La Liga")
athletic = Club("Athletic Club", "Athletic Club", "La Liga")
espanyol = Club("Espanyol", "Espanyol", "La Liga")
osasuna = Club("Osasuna", "Osasuna", "La Liga")
valencia = Club("Valencia", "Valencia", "La Liga")
villarreal = Club("Villarreal", "Villarreal", "La Liga")
celta = Club("Celta Vigo", "Celta Vigo", "La Liga")
mallorca = Club("Mallorca", "Mallorca", "La Liga")
granada = Club("Granada", "Granada", "La Liga")
alaves = Club("Alaves", "Alavés", "La Liga")
elche = Club("Elche", "Elche", "La Liga")
cadiz = Club("Cadiz", "Cádiz", "La Liga")
getafe = Club("Getafe", "Getafe", "La Liga")
levante = Club("Levante", "Levante", "La Liga")

bavaria = Club("Bayern Munich", "Bayern Munich", "Bundesliga")
borussia_d = Club("Borussia Dortmund", "Dortmund", "Bundesliga")
bayer = Club("Bayer Leverkusen", "Bayer Leverkusen", "Bundesliga")
union = Club("Union Berlin", "Union Berlin", "Bundesliga")
freiburg = Club("Freiburg", "Freiburg", "Bundesliga")
hoffenheim = Club("Hoffenheim", "Hoffenheim", "Bundesliga")
wolfsburg = Club("Wolfsburg", "Wolfsburg", "Bundesliga")
rb_leipzig = Club("RasenBallsport Leipzig", "RB Leipzig", "Bundesliga")
mainz = Club("Mainz 05", "Mainz 05", "Bundesliga")
koln = Club("FC Cologne", "Köln", "Bundesliga")
borussia_m = Club("Borussia M.Gladbach", "Mönchengladbach", "Bundesliga")
eintracht = Club("Eintracht Frankfurt", "Eintracht Frankfurt", "Bundesliga")
bochum = Club("Bochum", "Bochum", "Bundesliga")
hertha = Club("Hertha Berlin", "Hertha BSC", "Bundesliga")
stuttgart = Club("VfB Stuttgart", "Stuttgart", "Bundesliga")
augsburg = Club("Augsburg", "Augsburg", "Bundesliga")
arminia = Club("Arminia Bielefeld", "Arminia", "Bundesliga")
greuther = Club("Greuther Fuerth", "Greuther Fürth", "Bundesliga")

psg = Club("Paris Saint Germain", "Paris Saint-Germain", "Ligue 1")
marseille = Club("Marseille", "Marseille", "Ligue 1")
rennes = Club("Rennes", "Rennes", "Ligue 1")
nice = Club("Nice", "Nice", "Ligue 1")
lens = Club("Lens", "Lens", "Ligue 1")
strasbourg = Club("Strasbourg", "Strasbourg", "Ligue 1")
monaco = Club("Monaco", "Monaco", "Ligue 1")
angers = Club("Angers", "Angers", "Ligue 1")
montpellier = Club("Montpellier", "Montpellier", "Ligue 1")
lyon = Club("Lyon", "Lyon", "Ligue 1")
brest = Club("Brest", "Brest", "Ligue 1")
lille = Club("Lille", "Lille", "Ligue 1")
nantes = Club("Nantes", "Nantes", "Ligue 1")
reims = Club("Reims", "Reims", "Ligue 1")
troyes = Club("Troyes", "Troyes", "Ligue 1")
lorient = Club("Lorient", "Lorient", "Ligue 1")
clermont = Club("Clermont Foot", "Clermont Foot", "Ligue 1")
bordeaux = Club("Bordeaux", "Bordeaux", "Ligue 1")
metz = Club("Metz", "Metz", "Ligue 1")
saint_etienne = Club("Saint-Etienne", "Saint-Étienne", "Ligue 1")

zenit = Club("Zenit St. Petersburg", "Zenit", "RPL")
dinamo = Club("Dinamo Moscow", "Dynamo Moscow", "RPL")
sochi = Club("PFC Sochi", "Sochi", "RPL")
cska = Club("CSKA Moscow", "CSKA Moscow", "RPL")
krasnodar = Club("FC Krasnodar", "Krasnodar", "RPL")
lokomotiv = Club("Lokomotiv Moscow", "Lokomotiv Moscow", "RPL")
akhmat = Club("FK Akhmat", "Akhmat Grozny", "RPL")
samara = Club("Krylya Sovetov Samara", "Samara", "RPL")
spartak = Club("Spartak Moscow", "Spartak Moscow", "RPL")
rubin = Club("Rubin Kazan", "Rubin Kazan", "RPL")
ural = Club("Ural", "Ural Yekaterinburg", "RPL")
arsenal_tula = Club("Arsenal Tula", "Arsenal Tula", "RPL")
nizhny_novgorod = Club("Nizhny Novgorod", "Nizhny Novgorod", "RPL")
rostov = Club("FC Rostov", "Rostov", "RPL")
ufa = Club("FC Ufa", "Ufa", "RPL")
khimki = Club("Khimki", "FC Khimki", "RPL")

EPL = [chelsea, manchester_city, liverpool, west_ham, arsenal, manchester_united, brighton, wolverhampton, tottenham,
       crystal_palace, everton, leicester, southampton, brentford, leeds, aston_villa, watford, burnley, newcastle,
       norwich]
Serie_A = [napoli, milan, inter, atalanta, roma, juventus, bologna, fiorentina, lazio, h_verona, empoli, sassuolo,
           torino, udinese, sampdoria, venezia, spezia, genoa, cagliari, salernitana]
La_liga = [real, atletico, real_sociedad, sevilla, betis, rayo, barcelona, athletic, espanyol, osasuna, valencia,
           villarreal, celta, mallorca, granada, alaves, elche, cadiz, getafe, levante]
Bundesliga = [bavaria, borussia_d, bayer, union, freiburg, hoffenheim, wolfsburg, rb_leipzig, mainz, koln, borussia_m,
              eintracht, bochum, hertha, stuttgart, augsburg, arminia, greuther]
Ligue_1 = [psg, marseille, rennes, nice, lens, strasbourg, monaco, angers, montpellier, lyon, brest, lille, nantes,
           reims, troyes, lorient, clermont, bordeaux, metz, saint_etienne]
RPL = [zenit, dinamo, sochi, cska, krasnodar, lokomotiv, akhmat, samara, spartak, rubin, ural, arsenal_tula,
       nizhny_novgorod, rostov, ufa, khimki]

leagues = {
    "EPL": EPL,
    "La Liga": La_liga,
    "Serie A": Serie_A,
    "Bundesliga": Bundesliga,
    "Ligue 1": Ligue_1,
    "RPL": RPL,
}

leagues_select = {
    1: EPL,
    2: La_liga,
    3: Serie_A,
    4: Bundesliga,
    5: Ligue_1,
    6: RPL
}
