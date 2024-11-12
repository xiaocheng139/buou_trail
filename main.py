import json
from chua_ok_all import MultiAssetTradingBot
from notifier import Notifier

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config_data = json.load(f)

    platform_config = config_data['okx']
    monitor_interval = config_data.get("monitor_interval", 4)
    feishu_webhook = config_data.get('feishu_webhook', None)
    telegram_token = config_data.get('telegram_token', None)
    telegram_chat_id = config_data.get('telegram_chat_id', None)

    notifier = Notifier(feishu_webhook, telegram_token, telegram_chat_id)

    bot = MultiAssetTradingBot(platform_config, notifier=notifier, monitor_interval=monitor_interval)
    bot.monitor_total_profit()