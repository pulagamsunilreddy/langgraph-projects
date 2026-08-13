from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
flight_results = search_flights("Plan a 5 days trip to singapore")
print(flight_results)
#results = tavily_search("best hotels in tirupathi")
#print(results)