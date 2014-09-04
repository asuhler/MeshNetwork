import time,pika
rabbit = object
username = 'UAS'
password = 'UAS'
host = '10.128.4.222'
vhost = 'UASHost'
exchange = 'UAS'


creds = pika.PlainCredentials(username=username, password=password)
connection = pika.BlockingConnection(pika.ConnectionParameters(\
        host = host,\
        virtual_host = vhost,\
        credentials = creds))

channel = connection.channel()

channel.exchange_declare(exchange = exchange, \
                         type = 'topic')

result = channel.queue_declare(exclusive = True)
queue_name = result.method.queue

binding_keys = ['#']

i=0
while i<len(binding_keys):
    channel.queue_bind(exchange = exchange, \
                   queue = queue_name, \
                   routing_key = '#' )
    '''binding_keys[i]'''
    i=i+1
print ' [*] Waiting for messages. To exit press CTRL-C'



def callback(ch, method, properties, body):

    print "[x] %s: %s: %s" % (str(time.time()), method.routing_key, str(body))

    #time.sleep(2)
    #print(body)

channel.basic_consume(callback, \
                      queue = queue_name, \
                      no_ack = True)

channel.start_consuming()