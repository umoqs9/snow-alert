import os
import requests

# List of resorts with coordinates and their custom Snowatch links
resorts = [
    {
        "name": "Falls Creek",
        "url": "https://api.open-meteo.com/v1/forecast?latitude=-36.8631&longitude=147.2806&daily=snowfall_sum&timezone=Australia%2FSydney",
        "snowatch": "https://www.snowatch.com.au/15-day-forecasts/falls-creek/"
    },
    {
        "name": "Mt Hotham",
        "url": "https://api.open-meteo.com/v1/forecast?latitude=-36.9800&longitude=147.1325&daily=snowfall_sum&timezone=Australia%2FSydney",
        "snowatch": "https://www.snowatch.com.au/15-day-forecasts/hotham/"
    },
    {
        "name": "Mt Buller",
        "url": "https://api.open-meteo.com/v1/forecast?latitude=-37.1472&longitude=146.4484&daily=snowfall_sum&timezone=Australia%2FSydney",
        "snowatch": "https://www.snowatch.com.au/15-day-forecasts/mt-buller/"
    }
]

def check_snow():
    for resort in resorts:
        try:
            response = requests.get(resort["url"])
            data = response.json()
            
            # Grabs the 3-day overhead forecast (Index 3)
            snowfall_cm = data['daily']['snowfall_sum'][3]
            
            # TEST MODE: Set to -1 to force all alerts out for our test run
            if snowfall_cm > -1:
                send_discord_alert(resort["name"], snowfall_cm, resort["snowatch"])
            else:
                print(f"No fresh snow forecast in 3 days for {resort['name']}.")
                
        except Exception as e:
            print(f"Error checking weather for {resort['name']}: {e}")

def send_discord_alert(resort_name, snow_amount, snowatch_link):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL environment variable not found.")
        return

    # Flattened payload message text string to ensure zero syntax or formatting errors
    message_text = f"❄️ **Fresh Snow Alert for {resort_name}!** ❄️\nForecast predicts **{snow_amount} cm** of fresh powder in 3 days! Time to prep! 🏂⛷️\n🔗 Check out the full outlook here: {snowatch_link}"
    
    payload = {"content": message_text}
    
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print(f"Alert sent successfully for {resort_name}!")
    else:
        print(f"Failed to send alert for {resort_name}. Status: {response.status_code}")

if __name__ == "__main__":
    check_snow()
