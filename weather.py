import requests
from rich.console import Console
from rich.table import Table
from datetime import datetime
import os

# Initialize console
console = Console()

from dotenv import load_dotenv
load_dotenv()

# Get API key (preferably set as environment variable)
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def kelvin_to_celsius(k):
    return round(k - 273.15, 2)

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return None

def display_weather(data):
    city = data["name"]
    country = data["sys"]["country"]
    temp = kelvin_to_celsius(data["main"]["temp"])
    feels_like = kelvin_to_celsius(data["main"]["feels_like"])
    weather = data["weather"][0]["description"].title()
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S')

    table = Table(title=f"Weather in {city}, {country}")

    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Temperature", f"{temp} °C")
    table.add_row("Feels Like", f"{feels_like} °C")
    table.add_row("Condition", weather)
    table.add_row("Humidity", f"{humidity}%")
    table.add_row("Wind Speed", f"{wind} m/s")
    table.add_row("Sunrise", sunrise)
    table.add_row("Sunset", sunset)

    console.print(table)

def main():
    console.print("[bold blue]🌤️  Welcome to CLI Weather App[/bold blue]")
    city = console.input("Enter a city: ")

    data = get_weather(city)
    if data:
        display_weather(data)

if __name__ == "__main__":
    main()
