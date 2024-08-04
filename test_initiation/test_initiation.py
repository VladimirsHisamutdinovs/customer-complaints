from redis import Redis, ConnectionError
import time

def initiate_complaint(redis_host):
    try:
        redis = Redis(host=redis_host, port=6379)
        message = {"complaint": "The internet is severely lagging in Qatar right now"}
        redis.xadd('initiate_complaints', message)
        print("Initiation message sent to 'initiate_complaints' stream")
    except ConnectionError as e:
        print(f"Could not connect to Redis: {e}")

if __name__ == "__main__":
    while True:
        initiate_complaint(redis_host='redis')
        time.sleep(10)  # Sleep for 10 seconds
