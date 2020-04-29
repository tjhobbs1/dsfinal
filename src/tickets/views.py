from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import TicketForm




# Create your views here.



def home_view(request):
   
    x = f.airportList()
    

    if request.method == 'POST':
        ResultedForm = TicketForm(request.POST, my_arg=x)

        if ResultedForm.is_valid():
            x = ResultedForm.cleaned_data['flightFrom']
            y = ResultedForm.cleaned_data['destination']
            num_of_stops = ResultedForm.cleaned_data['numOfStops']
            num_of_stops = int(num_of_stops) +1
            passed_num_of_stops = num_of_stops-1
            
            routes = get_flights(x,y,num_of_stops)
            

            return render(request,'result.html',{'results': routes,'x':x,'y':y,'stops':passed_num_of_stops})
            
    else:
        
        context = {
            
            'form' : TicketForm(my_arg=x),
            
        }

        return render(request,'home.html',context)






from collections import defaultdict

import random


class FlightNetwork:
    def __init__(self):
        """
        Consturctor for the Flight Network
        """
        self.neighbors = defaultdict(list)
        self.distance = defaultdict(list)

    def add_flight(self, source, destination,miles):
        """
        A function to add a flight path

        :source:  The sending airport
        :destination: The Recieving airport
        :miles: distance between airports

        """
        self.neighbors[source].append(destination)
        self.distance[source].append(miles)

    def show_flights(self):
        """
        A Function to show flights
        """
        print("Destinations:");print(dict(self.neighbors))
        print("Dist:");print(dict(self.distance))


    def get_route(self, destination, source, parent):
        """
        A recursive function that is used to get the route between two points. 
        :destination: the destination airport
        :source: the starting airport
        :parent: the dictonary returned from the level_order_traversal of the flight network graph.
        :returns: a list of the routes between the two airports.  
        """

        if destination[0] == source:
            return [source]
        #Add list to 
        routes = []
        for p in parent[destination]:
            routes.extend([r + "," + destination[0] for r in self.get_route(p, source,  parent)])
        
        return routes

    def level_order_traversal(self, source, stops_range):
        """
        The purpose of this function is to perfrom a breadth first traversal of the graph so that we can 
        get the routes from the starting destination with the given stop_range. 
        :source: the starting destination
        :stop_range: the number of max and min number of stops
        """
        least_stops, max_stops = stops_range

        # The BFS queue
        queue = [(source, 0, -1)]


        # Parent dictionary used for finding the actual routes once level order traversal is done
        parent = defaultdict(list)

        # Continue until the queue is empty
        while queue:

            # Pop the front element of the queue.
            location, cost_till_now, stops_since_source = queue.pop(0)

            # If the current location has eny neighbors i.e. any direct flights, iterate over those neighbors
            if location in self.neighbors:
                for neighbor, cost in zip(self.neighbors[location], self.distance[location]):
                   
                    parent[(neighbor, stops_since_source + 1)].append((location, stops_since_source))

                    # If the number of stops till now is < max_stops, then we can add this `location` node for processing.
                    if stops_since_source < max_stops:
                        queue.append((neighbor, cost + cost_till_now, stops_since_source + 1))
        # Return parent node for route backtracking.
        return parent


    def bubbleSort(self,alist):
        """
        A Bubble Sort sort function, that takes the list of airports and sorts it out.
        :param alist: the unsorted list of airport
        :return: sorts the list. 
        """
        for passnum in range(len(alist)-1,0,-1):
            for i in range(passnum):
                if alist[i]>alist[i+1]:
                    temp = alist[i]
                    alist[i] = alist[i+1]
                    alist[i+1] = temp

    def airportList(self):
        """
        A function that creates a list of airports
        :return: a list of airports. 
        """
        airports1 = []
        for index,item in enumerate(self.neighbors):
            airports1.append(item)

        self.bubbleSort(airports1)
        return airports1



f = FlightNetwork()

f.add_flight("Des Moines","Chicago",100)
f.add_flight("Des Moines","Atlanta",300)
f.add_flight("Des Moines","Denver",250)
f.add_flight("Des Moines","Las Vegas",400)
f.add_flight("Des Moines","Los Angeles",500)
f.add_flight("Des Moines","Minneapolis–Saint Paul",150)
f.add_flight("Des Moines","Charlotte",250)
f.add_flight("Des Moines","Washington DC",375)
f.add_flight("Des Moines","St Louis",200)
f.add_flight("Des Moines","Houston",300)
f.add_flight("Des Moines","Dallas",350)
f.add_flight("Des Moines","Atlanta",350)
f.add_flight("Los Angeles","Washington DC",550)
f.add_flight("Los Angeles","Las Vegas",100)
f.add_flight("Los Angeles","Atlanta",600)
f.add_flight("Los Angeles","Chicago",1000)
f.add_flight("Charlotte","Washington DC",150)
f.add_flight("Charlotte","New York",250)
f.add_flight("Charlotte","Miami",500)
f.add_flight("Washington DC","New York",100)
f.add_flight("Washington DC","Miami",400)
f.add_flight("Washington DC","Atlanta",400)
f.add_flight("St Louis","Houston",350)
f.add_flight("St Louis","Dallas",350)
f.add_flight("St Louis","Denver",450)
f.add_flight("St Louis","Miami",300)
f.add_flight("St Louis","Phoenix",300)
f.add_flight("Houston","Phoenix",350)
f.add_flight("Dallas","Houston",50)
f.add_flight("Dallas","Phoenix",200)
f.add_flight("Dallas","Miami",350)
f.add_flight("Chicago","Phoenix",300)
f.add_flight("Chicago","New York",300)
f.add_flight("Chicago","Miami",400)
f.add_flight("Chicago","Atlanta",350)
f.add_flight("Chicago","Las Vegas",500)
f.add_flight("Chicago","Los Angeles",400)
f.add_flight("New York","Miami",100)
f.add_flight("New York","Atlanta",300)
f.add_flight("New York","Charlotte",100)
f.add_flight("Miami","Atlanta",200)
f.add_flight("Minneapolis–Saint Paul","St Louis",600)
f.add_flight("Denver","Atlanta",600)
f.add_flight("Denver","Phoenix",100)
f.add_flight("Denver","Las Vegas",200)
f.add_flight("Denver","Los Angeles",300)
f.add_flight("Atlanta","Phoenix",600)
f.add_flight("Atlanta","Los Angeles",700)
f.add_flight("Phoenix","Los Angeles",200)
f.add_flight("Phoenix","Las Vegas",200)
f.add_flight("Las Vegas","Phoenix",200)




def get_flights(start,end, num_of_alloted_stops):
    
    #This make a call that returns a dictionary of the nodes with the number of stops from the origin that is given.
    parent = f.level_order_traversal(start, (0,4))
    

    #Dict to hold results to display
    flight_result_dict = dict()
    #airports = []

    for r in range(0,num_of_alloted_stops):
        routes = f.get_route((end, r), start, parent)

        for r in routes:
            #Rand generate a flight Number
            flight_num = random.randint(1000, 9999)
            #Splits out the results that come back from function.
            x = r.split(',')

            #Creates a key for the dict
            flight_result_dict[flight_num] = dict()

            #Adds the numOfStops to dict
            flight_result_dict[flight_num]['numOfStops'] = x.__len__()-2

            #Add Price
            flight_result_dict[flight_num]['price'] = random.randint(100,1000)

            #Add NumOfSeatsLeft
            flight_result_dict[flight_num]['numOfSeatsLeft'] = random.randint(1,15)

            # Adds the stops to dict.
            for index, item in enumerate(x):
                index1 = f'stop{index}'
                flight_result_dict[flight_num][index1] = item

       
    return flight_result_dict

       


       



    
    

   


    