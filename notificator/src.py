import os
import time

from kafka import KafkaConsumer


class UsersFromKafka:
    def __init__(self):
        self.topic = os.getenv("RESPONSES_KAFKA_TOPIC", "responses")
        self.host = os.getenv("KAFKA_HOST", "localhost")
        self.port = os.getenv("KAFKA_PORT", "9092")
        self.consumer = self.__get_consumer()

    def __get_consumer(self):
        return KafkaConsumer(
            self.topic,
            bootstrap_servers=f"{self.host}:{self.port}"
        )

    def __call__(self, *args, **kwargs):
        for message in self.consumer:
            yield message.value.decode()


class UsersFromRedis:
    """
    Another implementation of streaming, to get all users by one request
    """
    def __init__(self):
        redis = object  # do not forget to import real Redis
        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = os.getenv('REDIS_PORT', 6379)
        self.password = os.getenv('REDIS_PASSWORD', 'rpass')
        self.redis: redis.Redis = redis.Redis(host=self.host,
                                              port=self.port,
                                              password=self.password,
                                              decode_responses=True)

    def stream_users(self) -> str:
        users = {}
        for user in self.get_users():
            users[user] = self.redis.get(user)
        result = str(users) + "<br>"
        return result

    def get_users(self) -> list:
        return sorted(self.redis.keys())

    def get_user_status(self, user_name: str) -> str:
        return self.redis.get(user_name)

    def __next__(self):
        time.sleep(1)
        return self.stream_users()

    def __iter__(self):
        return self
