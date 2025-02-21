# from kafka import KafkaConsumer
#
# def ingest_stream(bootstrap_servers, topic, group_id):
#     """
#     Consumes data from a Kafka stream.
#     :param bootstrap_servers: Kafka bootstrap servers.
#     :param topic: Kafka topic name.
#     :param group_id: Kafka consumer group ID.
#     :return: List of messages from the stream.
#     """
#     consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, group_id=group_id, auto_offset_reset='earliest')
#     return [{"source": "stream", "content": msg.value.decode("utf-8"), "metadata": {"offset": msg.offset}} for msg in consumer]
