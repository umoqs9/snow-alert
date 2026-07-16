import os
import requests

# We will use Falls Creek as our target resort for the script
resort_name = "Falls Creek"
api_url = "https://api.open-meteo.com/v1/forecast?latitude=-36.8631&longitude=147.2806&daily=snowfall_sum&timezone=Australia%2FSydney"

def check_snow():
    try:
        response = requests.get(api_url)
        data = response.json()
        
        # Get the predicted snowfall for today (in cm)
        snowfall_cm = data['daily']['snowfall_sum'][-1]
        
        # If it's snowing, trigger the Discord alert!
        if snowfall_cm > 0:
            send_discord_alert(snowfall_cm)
        else:
            print(f"No fresh snow forecast today for {resort_name}.")
            
    except Exception as e:
        print(f"Error checking weather: {e}")

def send_discord_alert(snow_amount):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL environment variable not found.")
        return

    payload = {
        "content": f"❄️ **Fresh Snow Alert for {resort_name}!** ❄️\nForecast predicts **{snow_amount} cm** of fresh powder today! Time to hit the slopes! 🏂⛷️"
    }
    
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Alert sent successfully to Discord!")
    else:
        print(f"Failed to send Discord alert. Status code: {response.status_code}")

if __name__ == "__main__":
    check_snow()
