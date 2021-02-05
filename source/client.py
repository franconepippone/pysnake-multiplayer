import Snake
import pygame as pg
import sys
import renderer as gui
import time
import threading
import socket
import pickle
import json

print("Starting...")

with open('configs.json','r') as f:
	cfgs = json.load(f)
print("Configurazioni caricate.")

s = socket.socket()
print("Socket create.")

chunksize = cfgs['net']['chunk_size']
errsize = cfgs['net']['errsize']

executing = True

def recvheader():
	h = s.recv(4)
	return int.from_bytes(h, 'little')

def empty(sock):
	sock.setblocking(False)
	while 1:
		try:
			sock.recv(1024)
		except:
			break
	sock.setblocking(True)

def recvall(size, chunk=chunksize):
	data = bytearray()
	if size > errsize:
		empty(s)
		size = 0
	while len(data) < size:
		print(size, len(data))
		data += s.recv(chunk)
	return data


def connect():
	global env
	try:
		s.connect((cfgs['host'], cfgs['port']))
	except ConnectionRefusedError as e:
		print("Server unavailable.", e)
		return False
	print(f"Connessione a {cfgs['host']} riuscita.")

	#with lock:
	print("Lock acquisito.")
	data = s.recv(10000)
	time.sleep(.1)
	print("Dati di inizializzazione ricevuti.")
	start_env = pickle.loads(data)
	print("Ambiente caricato.")
	env = Snake.environment(start_env)
	print("Mondo di gioco creato.")
	return True

def quit():
	global executing
	executing = False
	pg.quit()
	try:
		s.sendall('LEAVE'.encode())
	finally:
		time.sleep(1)
		s.close()
	print("Quitting...")
	time.sleep(1)
	sys.exit()

def update_env(lock):
	empty(s)
	while executing:
		try:
			size = recvheader()
			data = recvall(size)
		except BlockingIOError as e:
			print(e)
			continue
		except OSError as e:
			print(e)
			continue
		except ConnectionResetError as e:
			print(e)
			continue

		try:
			data = pickle.loads(data)
		except (NameError, KeyError, pickle.UnpicklingError, EOFError) as e:
			print(e)
			empty(s)
			continue

		with lock:
			env.storenew(data)
		print("ENDUPDATE")


def main():
	lock = threading.Lock()
	while not connect():
		print("Reconnecting...")
		time.sleep(5) # Attempt connection to server
	gui.init()
	print("Gui inizializzata.")
	# starts app threads
	t1 = threading.Thread(target = update_env, args= (lock,))
	t1.start()

	# rendering loop
	while True:
		pg.time.Clock().tick(144)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				quit()
				break
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					s.sendall('MU'.encode())
				elif event.key == pg.K_LEFT:
					s.sendall('ML'.encode())
				elif event.key == pg.K_DOWN:
					s.sendall('MD'.encode())
				elif event.key == pg.K_RIGHT:
					s.sendall('MR'.encode())
				elif event.key == pg.K_SPACE:
					s.sendall('JOIN'.encode())
					print("sent")
				elif event.key == pg.K_ESCAPE:
					quit()
					break

		with lock:
			gui.render_scene(env)
		gui.update()

main()
