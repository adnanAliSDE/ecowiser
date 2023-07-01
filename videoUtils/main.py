import pvleopard

access_key="IEgSOHOe/DMdOBcOyD/mP5bFZTNncQKFx4ITB7iqO24OP5pj3wbUfA=="
leopard = pvleopard.create(access_key=access_key)

transcript, words = leopard.process_file('./a1.mp3')
print(words)