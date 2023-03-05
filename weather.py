import pprint
import requests
from matplotlib import pyplot as plt
from datetime import datetime
from dotenv import dotenv_values

config = dotenv_values(".env")

DEG_FAHRENHEIT = "F"
DEG_CELCIUS = "C"

def to_fahrenheit(K):
    return round((float(K) - 273.15)* 1.8000+ 32.00)

def to_celcius(K):
    return round(float(K) - 273.15)

def formatter(dates):
    def get_dates(x):
        try:
            return dates[int(x)]
        except:
            return ""
    def fmt(x):
        dt = datetime.fromisoformat(get_dates(x))
        if dt.hour == 0 or x == 0 or x == len(dates) - 1:
            return dt.strftime("%b %d %#I %p")
        else:
            return dt.strftime("%#I %p")
    return lambda x,pos: fmt(x)


def get_region_weather(region, units = DEG_FAHRENHEIT):
    API_KEY = config["API_KEY"]
    API_URL = f"https://api.openweathermap.org/data/2.5/forecast?appid={API_KEY}&q={region}"
    r = requests.get(API_URL)
    response = r.json()

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response)

    forecast_list = response["list"]

    dates = []
    temps = []

    temperature_formatter = to_fahrenheit if units is DEG_FAHRENHEIT else to_celcius

    for forecast in forecast_list:
        dt = forecast["dt_txt"]
        temp = temperature_formatter(forecast["main"]["feels_like"])
        dates.append(dt)
        temps.append(temp)
    return dates, temps, units

def plot_data(region, dates, temps, units):
    plt.title(f"The 5 day forecast for {region}")
    plt.plot(dates, temps)

    plt.xlabel("Dates")

    unit = "Fahrenheit" if units is DEG_FAHRENHEIT else "Celcius"
    plt.ylabel(f"Tempertures in {unit}")

    ax = plt.gca()
    ax.xaxis.set_major_formatter(formatter(dates))

    plt.tick_params(axis="x", labelrotation=90)
    plt.show()


def main():
    region = input("Weather Forecast\nFor what region do you want weather? ")
    if len(region) == 0 or region.upper() == 'NONE':
        exit()
    try:
        units = input("Celcius or Fahrenheit(default) - choose 'C','F' or Enter: ") or DEG_FAHRENHEIT
        if units.upper() != DEG_CELCIUS and units.upper() != DEG_FAHRENHEIT:
            raise ValueError("You must enter a valid unit like 'c' or 'f'")
        
        data = get_region_weather(region, units)
        print("Generating Plot...")
        plot_data(region, *data)
    except ValueError as e:
        print (str(e))
        exit()
    except:
        print("Sorry - could not find that region")
        exit()

if __name__ == "__main__":
    main()