import pvleopard

ACCESS_KEY='IEgSOHOe/DMdOBcOyD/mP5bFZTNncQKFx4ITB7iqO24OP5pj3wbUfA=='
leopard = pvleopard.create(access_key=ACCESS_KEY)

print("started")
transcript, _ = leopard.process_file('./a1.mp3')
print(transcript)
