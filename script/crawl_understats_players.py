import asyncio
import pandas as pd
import aiohttp
from pymongo import MongoClient
from understat import Understat

#listleague = ['EPL','La_liga','Bundesliga','Ligue_1','Serie_A']

listleague = ['Ligue_1']

for league in listleague:

    allteam_df =[]
    allmatch_df = []
    league_k = league

    print (2021)
    teamlist = []
    matchs = []

    async def main():
        async with aiohttp.ClientSession() as session:
            understat = Understat(session)
            fixtures = await understat.get_league_results(
                league_k,
                2021
            )

            for i in fixtures:
                matchs.append(i)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    teamlist = list(set([team['h']['title'] for team in matchs]))

    print (teamlist)

    df_all = []

    for i, match in enumerate(matchs):

        async def main():
            async with aiohttp.ClientSession() as session:
                understat = Understat(session)
                players = await understat.get_match_players(match['id'])

                player_home = pd.DataFrame(players['h']).T
                player_away = pd.DataFrame(players['a']).T

                play_con = pd.concat([player_home, player_away])
                df_all.append(play_con)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

    df_players = pd.concat(df_all)

    json_all = []
    for idx in df_players.player_id.unique():
        df_player = df_players[df_players.player_id == idx].reset_index(drop=True)
        json_construct = {'player_id': idx,
                          'player_name': df_player['player'][0],
                          'position': df_player['position'][0],
                          'matchs_stats': df_player.to_dict(orient='records')
                          }
        json_all.append(json_construct)

    client = MongoClient('mongodb+srv://gurrenlagan:gurrenlagan@cluster0.2ffdj.mongodb.net/')
    dblist = client['data_sorare'].list_collections()

    if "players" in dblist:

        client['data_sorare'].drop_col('players')
        client['data_sorare'].players.insert_many(json_all)
        print("maj ok")

    else:

        client['data_sorare'].players.insert_many(json_all)
        print("maj ok")