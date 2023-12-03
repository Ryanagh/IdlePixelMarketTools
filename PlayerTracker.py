import time
import requests
from datetime import datetime

class MarketMonitor:
    def __init__(self, player_id, watch_items):
        self.player_id = player_id
        self.watch_items = watch_items
        self.previous_last_seen = {item: None for item in watch_items}
        self.iteration_delay = 5

    def fetch_market_data(self, item):
        url = f'https://idle-pixel.com/market/browse/{item}/'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching market data for {item}: {e}")
            return []

    def check_for_player_post(self, entries, item):
        for entry in entries:
            if entry.get('player_id') == self.player_id:
                last_seen = entry.get('market_item_post_timestamp')
                if self.previous_last_seen[item] != last_seen:
                    self.previous_last_seen[item] = last_seen
                    readable_timestamp = datetime.fromtimestamp(last_seen / 1000).strftime('%H:%M:%S:%f')[:-3]
                    print(f"Player ID: {entry['player_id']}, item: {entry['market_item_name']}, amount: {entry['market_item_amount']}, price each: {entry['market_item_price_each']}, timestamp: {last_seen}, readable timestamp: {readable_timestamp}")

    def monitor_market(self):
        while True:
            for item in self.watch_items:
                entries = self.fetch_market_data(item)
                self.check_for_player_post(entries, item)
            time.sleep(self.iteration_delay)


if __name__ == '__main__':
    player_id = 100008
    watch_items = ["red_mushroom", "pine_logs", "maple_logs"]
    market_monitor = MarketMonitor(player_id, watch_items)
    market_monitor.monitor_market()
