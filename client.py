import aiohttp
import asyncio
import json


async def fetch():
    """
    Transform stations into a different structure 
    and to apply some filtering and sorting on it
    """  
    try:
        station_url = 'https://wegfinder.at/api/v1/stations'
        async with aiohttp.ClientSession() as session:
            async with session.get(station_url) as response:
                response_obj = await response.json()
                stations = list(filter(lambda x: x['free_bikes'] > 0, response_obj))
                for station in stations:
                    free_ratio = station['free_boxes']/station['boxes']
                    station['free_ratio'] = free_ratio
                    coordinates = [station['longitude'], station['latitude']]
                    station['coordinates'] = coordinates
                    station.pop('longitude')
                    station.pop('latitude')
                    if station['status'] == 'aktiv':
                        station['active'] = True
                        station.pop('status')
                sorted_stations = sorted(stations, key=lambda k: (-int(k['free_bikes']), k["name"]))
                final_stations = await fetch_address(sorted_stations)
                print("**********************Final Results***********************")
                pretty_stations = json.dumps(final_stations, indent=4)
                print(pretty_stations)      # Stations in json format
                #print(final_stations)     # The list of stations 
                print(f'Total Stations: {len(final_stations)}')
    except Exception as e:
        print('Connection Error', str(e))
    
    return final_stations
  

async def fetch_address(sorted_stations) -> list:
    """
    Add a property called “address” to each station.
    """    
    address_url = 'https://api.i-mobility.at/routing/api/v1/nearby_address'
    for stat in sorted_stations:
        params = {'latitude' : stat['coordinates'][1], 'longitude': stat['coordinates'][0]}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(address_url, params=params) as resp:
                    json_body = await resp.json()
                    address = (json_body['data']['name'])
                    stat['address'] = address
        except Exception as e:
            print('Connection Error', str(e))
    return sorted_stations
    
                       
loop = asyncio.get_event_loop()
loop.run_until_complete(fetch())


