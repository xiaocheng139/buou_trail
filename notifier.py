import requests
import logging


class Notifier:
    def __init__(self, feishu_webhook=None, telegram_token=None, telegram_chat_id=None) -> None:
        self.feishu_webhook = feishu_webhook
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        # 配置日志
        log_file = "log/ok_bot.log"
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        self.logger = logger

    def send_notification(self, message):
        if self.feishu_webhook:
            try:
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "msg_type": "text",
                    "content": {
                        "text": message
                    }
                }
                response = requests.post(self.feishu_webhook, json=payload, headers=headers)
                if response.status_code == 200:
                    self.logger.info("飞书通知发送成功")
                else:
                    self.logger.error("飞书通知发送失败，状态码: %s", response.status_code)
            except Exception as e:
                self.logger.error("发送飞书通知时出现异常: %s", str(e))

        if self.telegram_token and self.telegram_chat_id:
            try:
                payload = {
                    'chat_id': self.telegram_chat_id,
                    'text': message
                }

                # 发送 HTTP POST 请求
                url = f'https://api.telegram.org/bot{self.telegram_token}/sendMessage'
                response = requests.post(url, data=payload)

                # 检查请求是否成功
                if response.status_code == 200:
                    self.logger.info("Telegram消息发送成功！")
                else:
                    self.logger.error(f"Telegram发送失败，状态码: {response.status_code}")
            except Exception as e:
                self.logger.error("发送飞书通知时出现异常: %s", str(e))