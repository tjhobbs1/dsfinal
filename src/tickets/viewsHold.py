from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import TicketForm




# Create your views here.


# def home_view(request):
    
#     form = TicketForm(request.POST or None)

#     if request.method == 'POST'and form.is_valid():
#         x = form.cleaned_data['flight_num']
#         y = form.cleaned_data['flight_num2']
#         c = x + y
#         u = "ty"
#         print(c)

#         t ={'result': c, 'name': u}

        
#         return render(request,'test.html',t)
        
        
#         return redirect('home')
#     else:
#         context = {
#             'form' : form,
#         }

#         return render(request,'home.html',context)

def home_view(request):
    
    form = TicketForm(request.POST or None)

    if request.method == 'POST'and form.is_valid():
        x = form.cleaned_data['flight_num']
        y = form.cleaned_data['flight_num2']
        
        num_of_stops = 5
        routes = get_flights("DSM","ATL",num_of_stops)
        # for num_of_stops in routes:
        #     print(num_of_stops)

        
        return render(request,'test.html',{"routes":routes})
        
        
        return redirect('home')
    else:
        context = {
            'form' : form,
        }

        return render(request,'home.html',context)



def trial_view(request):
    url = request.session.get('flight_num')





import csv

from collections import defaultdict

from random import randint


class FlightNetwork:
    def __init__(self):
        self.neighbors = defaultdict(list)
        self.cost = defaultdict(list)

    def add_flight(self, source, destination, price):
        self.neighbors[source].append(destination)
        self.cost[source].append(price)

    def show_flights(self):
        print("Destinations:");print(dict(self.neighbors))
        print("Cost:");print(dict(self.cost))

    def get_price(self,dest):
        return self.cost[dest]

    def get_route(self, destination, source, parent):
        if destination[0] == source:
            return [source]
        routes = []
        for p in parent[destination]:
            routes.extend([r + "-->" + destination[0] for r in self.get_route(p, source,  parent)])
        #print(routes)
        return routes

    def level_order_traversal(self, source, max_stops):


        # The BFS queue
        queue = [(source, 0, -1)]


        # Parent dictionary used for finding the actual routes once level order traversal is done
        parent = defaultdict(list)
        #print(f'Parent1 {parent}')

        # Continue until the queue is empty
        while queue:
            #print(f'Queue{queue}')

            # Pop the front element of the queue.
            location, cost_till_now, stops_since_source = queue.pop(0)

            # If the current location has eny neighbors i.e. any direct flights, iterate over those neighbors
            if location in self.neighbors:
                for neighbor, cost in zip(self.neighbors[location], self.cost[location]):
                    """
                        THIS STEP IS VERY IMPORTANT. We record all the parents of this `location` via which a path
                        starting from S reached `location` in `stops_since_source + 1` steps.
                    """
                    parent[(neighbor, stops_since_source + 1)].append((location, stops_since_source))

                    # If the number of stops till now is < max_stops, then we can add this `location` node for processing.
                    if stops_since_source < max_stops:
                        queue.append((neighbor, cost + cost_till_now, stops_since_source + 1))
        #print(f'Parent: {parent}')
        # Return parent node for route backtracking.
        return parent


f = FlightNetwork()

f.add_flight("DSM","ORD",100)
f.add_flight("DSM","ATL",200)
f.add_flight("DSM","DEN",300)
f.add_flight("DSM","LAS",400)
f.add_flight("DSM","LAX",500)
f.add_flight("ORD","PHX",300)
f.add_flight("ORD","JFK",300)
f.add_flight("JFK","MIA",100)
f.add_flight("DSM","MSP",50)
f.add_flight("MSP","STL",600)
f.add_flight("ORD","ATL",600)
f.add_flight("DEN","ATL",600)
f.add_flight("PHX","ATL",600)





def get_flights(start,end,num_of_alloted_stops):
    #This make a call that returns a dictionary of the nodes with the number of stops from the origin that is given.
    parent = f.level_order_traversal(start, (num_of_alloted_stops))

    flights = []
    for num_of_alloted_stops in range(0, 5):
        print("\nFlights with {} stops in between are as follows:".format(num_of_alloted_stops))
        #passes the destination and the number of stops allowed and the destination and the parent dictionary to the function.
        routes = f.get_route((end, num_of_alloted_stops), start, parent)

        for num_of_alloted_stops in routes:
            flights.append(num_of_alloted_stops)
            #print(num_of_alloted_stops)
    print(flights)
    return flights

    