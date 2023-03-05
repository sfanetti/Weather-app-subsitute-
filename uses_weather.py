import weather

print("I am using the weather.py but it does not call main")

temp_kelvin = 287
print(f"The Kelvin temperature is {temp_kelvin}K.")
print(f"In Fahrenheit it's {weather.to_fahrenheit(temp_kelvin)} Degrees")
print(f"In Celcius it's {weather.to_celcius(temp_kelvin)} Degrees")