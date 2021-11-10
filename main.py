import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.108',
                                                                   port=5672))
    channel = connection.channel()

    channel.basic_publish('e.general', 'r.request.test', bytes('Hello hey1', 'utf-8'))


if __name__ == '__main__':
    main()
