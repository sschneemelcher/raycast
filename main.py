import eel
import numpy as np
import datetime

@eel.expose
def print_log(k, v):
	print(k, v)

@eel.expose
def move(k, v):
	if 36 < k < 41:
		global moves
		moves[k-37] = v
	
def print_fps(start, fps):
	print(fps)
	return datetime.datetime.now(), 0


def get_dist(x1, x2, y1, y2, a1, a2):
	ca = np.cos((a1-a2)%(2*np.pi))
	return (np.abs(x1 - x2)+np.abs(y1 - y2))*ca

def draw_rays():
	ray_list = []
	ra = (player[4]-30*np.pi/180)%(2*np.pi)
	for r in range(61):
		rx, ry, xo, yo, mx, my, dof = [0]*7
		#check horizontal lines
		if ra == 0:
			atan = 10*10
		else:
			atan = -(np.cos(ra)/np.sin(ra))
		if ra > np.pi:
			ry = (player[1]//64)*64-0.0001
			rx = (player[1] - ry)*atan+player[0]
			yo = -block_size
			xo = -yo*atan
		if ra < np.pi:
			ry = (player[1]//64)*64+block_size
			rx = (player[1] - ry)*atan+player[0]
			yo = block_size
			xo = -yo*atan
		if ra == 0 or ra == np.pi:
			rx = player[0]
			ry = player[1]
			dof = 8
		while dof < 8:
			mx = min(max(int(rx//64),0),len(field)-1)
			my = min(max(int(ry//64),0),len(field)-1)
			if field[mx][my] == 1:
				dof=8
			else:
				rx += xo
				ry += yo
				dof+=1
		dist = get_dist(player[0],rx,player[1],ry,player[4],ra)
		temp_ray = [rx, ry, dist, 0]
	
		rx, ry, xo, yo, mx, my, dof = [0]*7
		#check vertical lines
		if ra == 0:
			ntan = -10*10
		else:
			ntan = -np.sin(ra)/np.cos(ra)
		if 3*np.pi/2 > ra > np.pi/2:
			rx = (player[0]//64)*64-0.0001
			ry = (player[0] - rx)*ntan+player[1]
			xo = -block_size
			yo = -xo*ntan
		if ra < np.pi/2 or ra > 3*np.pi/2:
			rx = (player[0]//64)*64+block_size
			ry = (player[0] - rx)*ntan+player[1]
			xo = block_size
			yo = -xo*ntan
		if ra == 0 or ra == np.pi:
			rx = player[0]
			ry = player[1]
			dof = 8
		while dof < 8:
			mx = min(max(int(rx//64),0),len(field)-1)
			my = min(max(int(ry//64),0),len(field)-1)
			if field[mx][my] == 1:
				dof=8
			else:
				rx += xo
				ry += yo
				dof+=1

		dist = get_dist(player[0],rx,player[1],ry,player[4],ra) 
		if dist >= temp_ray[2]:
			ray_list.append(temp_ray)
		else:
			ray_list.append([rx, ry, dist, 1])
		ra += np.pi/180
		ra %= 2*np.pi

	px = player[0]+player_size//2
	py = player[1]+player_size//2
	lines = [] 
	rects = []
	for idx, ray in enumerate(ray_list):
		lines.append([px, py, ray[0], ray[1]])
		lh = block_size*512/ray[2]
		rects.append([[idx*8+532, 256-lh/2, 8, lh],[255-ray[3]*125,0,0]])
	render(rects)
	eel.drawLines(lines)

def render(rects=[]):
	for x in range(len(field)):
		for y in range(len(field[x])):
			if field[x][y] == 1:
				rects.append([[x*block_size,y*block_size,block_size-1,block_size-1],[255,255,255]])
	rects.append([player[:2].tolist()+[player_size, player_size],[0,255,0]])
	eel.drawRects(rects)

def move_player(player):
	player[0] += moves[1]*player[2]*2
	player[0] -= moves[3]*player[2]*2
	player[1] += moves[1]*player[3]*2
	player[1] -= moves[3]*player[3]*2
	player[4] -= moves[0]*0.05
	player[4] += moves[2]*0.05
	player[4] %= 2*np.pi
	player[2] = np.cos(player[4])
	player[3] = np.sin(player[4])
	return player

moves = np.zeros(4) # left up right down
field = [[1,1,1,1,1,1,1,1],
	 [1,0,1,0,0,0,0,1],
	 [1,0,1,0,0,0,0,1],
	 [1,0,0,0,0,0,0,1],
	 [1,0,0,0,1,1,0,1],
	 [1,1,1,0,0,0,0,1],
	 [1,0,0,0,0,0,0,1],
	 [1,1,1,1,1,1,1,1]]

block_size = 64
player_size = 16

player = np.zeros(5)
player[:2]+=200
player[4] = np.pi
eel.init('app')
eel.start('index.html', size=(1064,562), block=False)
d = np.arange(4)
draw_rays()
start = datetime.datetime.now()
fps = 0
while True:
	eel.sleep(0.01)
	if 1 in moves:
		draw_rays()
		player = move_player(player)
	if (datetime.datetime.now() - start).seconds:
		start, fps = print_fps(start, fps)
	fps += 1
		
