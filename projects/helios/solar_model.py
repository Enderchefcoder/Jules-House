import random

class SolarModel:
    """Simulates weather-driven solar energy production."""
    def __init__(self):
        self.weather_states = ["Sunny", "Cloudy", "Overcast", "Stormy"]
        self.current_weather = "Sunny"

    def update_weather(self):
        self.current_weather = random.choice(self.weather_states)
        print(f"[HELIOS Solar] Weather shifted to: {self.current_weather}")

    def get_production(self, gaia_weather=None):
        base_production = 100.0

        if gaia_weather:
            # Use GAIA weather modifiers
            mods = gaia_weather.get_modifiers()
            prod = base_production * mods["energy"]
            # print(f"[HELIOS Solar] Using GAIA modifiers ({gaia_weather.current_weather}): {prod:.1f} units.")
        else:
            modifiers = {
                "Sunny": 1.2,
                "Cloudy": 0.8,
                "Overcast": 0.5,
                "Stormy": 0.2
            }
            prod = base_production * modifiers.get(self.current_weather, 1.0)
            print(f"[HELIOS Solar] Production: {prod:.1f} units.")
        return prod

if __name__ == "__main__":
    model = SolarModel()
    model.update_weather()
    model.get_production()
