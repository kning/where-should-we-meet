from geopy.geocoders import Nominatim
from yelpapi import YelpAPI
import os
import random
import re

class MeetupFinder:
    """
    This class takes in a Yelp API key and finds a highly rated coffee shop between two zip codes
    """
    def __init__(self, api_key, app_name='where-should-we-meet'):
        self.yelp_api = YelpAPI(api_key)
        self.geolocator = Nominatim(user_agent=app_name)
    
    def is_proper_zip(self, zip):
        zipcode_re = re.compile(r"^\d{5}$")
        return zipcode_re.match(zip)

    def get_addresses(self):
        """
        Ask user for input on two zipcodes (NYC only) and return those values as a tuple
        """
        print("Find a good coffee spot to meet up in between two zipcodes.")
        print()

        while True:
            zip1 = input('Enter in zipcode 1 (5 digits): ')
            if self.is_proper_zip(zip1):
                break
            elif zip1 == 'null':
                print('Welcome back Mr. Null! Please put in a zipcode this time.')
            else:
                print("Invalid zipcode. Try again.")
        
        while True:
            zip2 = input('Enter in zipcode 2 (5 digits): ')
            if self.is_proper_zip(zip2):
                break
            else:
                print("Invalid zipcode. Try again.")

        return zip1, zip2

    def get_midpoint(self, zip1, zip2):
        """
        Return the Euclidean midpoint between two zips
        """

        # TODO: catch exception gracefully here if zipcode doesn't resolve
        location1 = self.geolocator.geocode({'postalcode': zip1}, country_codes='US')
        location2 = self.geolocator.geocode({'postalcode': zip2}, country_codes='US')

        midpoint_latitude = (location1.latitude + location2.latitude) / 2.0
        midpoint_longitude = (location1.longitude + location2.longitude) / 2.0
        
        midpoint_location = self.geolocator.reverse(f"{midpoint_latitude}, {midpoint_longitude}")
        midpoint_address = midpoint_location.raw.get('address')

        # get zip for the midpoint by parsing the string
        midpoint_zip = midpoint_address.get('postcode')
        return midpoint_zip

    def get_coffee_shops(self, zipcode):
        """
        Returns a well-rated random coffee shop between two zipcodes
        """
        response = self.yelp_api.search_query(term='coffee', location=zipcode, sort_by='rating', limit=10)
        results = response.get('businesses')

        selection = random.sample(results, 1)[0]

        print(f"Let's meet at {selection.get('name')}!")
        print(selection.get('location').get('address1'))
        print(selection.get('url').split('?')[0])

    def run(self):
        zip1, zip2 = self.get_addresses()
        self.get_coffee_shops(self.get_midpoint(zip1, zip2))
        

if __name__ == "__main__":
    # assumes your Yelp API key is saved to the YELP_API_KEY environment variable
    meetup_finder = MeetupFinder(os.environ['YELP_API_KEY'])
    meetup_finder.run()
 