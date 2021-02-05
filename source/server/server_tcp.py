import Snake
import time
import json
import pickle
import threading
import socket


with open('../levels/level.json') as f:
	world = json.load(f)

env = Snake.environment(19, 11, repeat = True, world = world, tilesize = 50)
players = {}

debugging = False

s = socket.socket()
s.bind(('', 65231))
s.listen(10)

def debug(*msg):
	if debugging:
		print(*msg)

def listen_for_connections(lock):
	global players
	while True:
		print("listening...")
		conn, addr = s.accept()  # handles connections
		print(f"got connection: {conn}, {addr}")
		conn.setblocking(True)

		newsnake = Snake.snake(-4,5,3)
		debug("listen_for_connections: acquiring")
		with lock:
			debug("listen_for_connections: acquired")

			conn.send(pickle.dumps(env)) # send world and initial state data to new player
			players[conn] = newsnake

			threading.Thread(target=handle_client_rqsts, args=(conn, newsnake, lock)).start()    # start a new rqsts handler
			debug(env.snakes, players[conn])
		debug("listen_for_connections: released")

	s.close()
	print("Server stopped listening.")


def handle_client_rqsts(conn, snk, lock):
	global players
	print("New thread started.")
	while True:
		try:
			rqst = conn.recv(16).decode()
		except ConnectionAbortedError:
			continue
		except ConnectionResetError:
			continue

		debug("handle_client_rqsts: acquiring")
		with lock:
			debug("handle_client_rqsts: acquired")
			# parse request
			if rqst == 'LEAVE':
				try:
					env.rmsnake(snk)
				except ValueError:
					pass
				del players[conn]
				conn.sendall('LEFT'.encode())
				conn.close()
				break
			elif rqst == 'JOIN':
				if not snk in env.snakes:
					snk.reset(0,5,5)
					env.addsnake(snk)
				print(env.snakes)
			elif rqst == 'ML':
				snk.changedir(1)
			elif rqst == 'MR':
				snk.changedir(0)
			elif rqst == 'MU':
				snk.changedir(2)
			elif rqst == 'MD':
				snk.changedir(-1)
		debug("handle_client_rqsts: released")

	print("Player left. Lock released.")

def update_loop(lock):
	global players
	while True:
		debug("update_loop: acquiring")
		with lock:
			debug("update_loop: acquired")
			env.update()
			data = pickle.dumps((env.snakes, env.foods))
			header = len(data).to_bytes(4, 'little')
			try:
				for player in players:
					player.sendall(header)
				for player in players:
					player.sendall(data)
			except ConnectionAbortedError:
				pass
			debug(data)
		debug("update_loop: released")
		time.sleep(0.1)   # update game world and send status every .1 seconds


def start():
	lock = threading.Lock()

	t1 = threading.Thread(target=listen_for_connections, args=(lock,))    # handles new connections
	t2 = threading.Thread(target=update_loop, args=(lock,))      # updates game loop and sends results

	t1.start()
	t2.start()
	print("started")


start()
