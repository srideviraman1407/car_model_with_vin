"""This function is to return vehicle model and year based on vin"""
import re
from flask import Flask
from flask_restful import Api, Resource


APP = Flask(__name__)
API = Api(APP)

#below are the car model details
CAR_MODEL = [
    {
        "vin_prefix": "WAU",
        "make": "Audi",
        "Y": "2000", "1": "2001", "2": "2002", "3":"2003", "4": "2004", "5": "2005",
        "6":"2006", "7": "2007", "8":"2008", "9": "2009", "A": "2010", "B": "2011",
        "C": "2012", "D":"2013", "E": "2014", "F": "2015", "G":"2016", "H": "2017",
        "J":"2018", "K": "2019"
    },
    {
        "vin_prefix": "WPO",
        "make": "Porsche",
        "Y": "2000", "1": "2001", "2": "2002", "3":"2003", "4": "2004", "5": "2005",
        "6":"2006", "7": "2007", "8":"2008", "9": "2009", "A": "2010", "B": "2011",
        "C": "2012", "D":"2013", "E": "2014", "F": "2015", "G":"2016", "H": "2017",
        "J":"2018", "K": "2019"
    },
    {
        "vin_prefix": "WVW",
        "make": "Volkswagen",
        "Y": "2000", "1": "2001", "2": "2002", "3":"2003", "4": "2004", "5": "2005",
        "6":"2006", "7": "2007", "8":"2008", "9": "2009", "A": "2010", "B": "2011",
        "C": "2012", "D":"2013", "E": "2014", "F": "2015", "G":"2016", "H": "2017",
        "J":"2018", "K": "2019"
    },
]

class carModels(Resource):
    """Class to validate and get car models"""
    def get(self, vin):
        """Function to get car models"""
        vin_pre = vin[0:3]
        vin_year = vin[9]
        regex = re.compile('[@_!#$%^&*()<>?/|}{~:]')
        for car in CAR_MODEL:
            #To validate the vin with length , prefix and string standards
            if(vin_pre == car["vin_prefix"] and len(vin) == 17 and regex.search(vin) is None):
                car_model_info = {'make':car["make"], 'year':car[vin_year]}
                return car_model_info, 200
        return "car model not found, Please verify your vin and try again", 404

API.add_resource(carModels, "/vin/<string:vin>")

if __name__ == "__main__":
    APP.run(host='0.0.0.0', debug=True)
    

