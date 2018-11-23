# -*- coding: utf-8 -*-
import sys

from confluent_kafka import Consumer, KafkaException, KafkaError

conf = {
    'bootstrap.servers': '10.8.1.43:9092',
    'group.id': "httptraffic-consumer",
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'},
    #     'security.protocol': 'SASL_SSL',
    # 'sasl.mechanisms': 'SCRAM-SHA-256',
    #     'sasl.username': os.environ['CLOUDKARAFKA_USERNAME'],
    #     'sasl.password': os.environ['CLOUDKARAFKA_PASSWORD']
}
topics = ['test']


def consume_msg():
    c = Consumer(**conf)
    c.subscribe(topics)
    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                # Error or event
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    # Error
                    raise KafkaException(msg.error())
            else:
                # Proper message
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))
                print(msg.value().decode('utf-8'))

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')

    # Close down consumer to commit final offsets.
    c.close()


if __name__ == '__main__':
    consume_msg()
