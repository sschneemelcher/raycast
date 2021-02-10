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
			field_value = field[mx][my]
			if field_value > 0:
				dof=8
			else:
				rx += xo
				ry += yo
				dof+=1
		dist = get_dist(player[0],rx,player[1],ry,player[4],ra)
		temp_ray = [rx, ry, dist, 0, field_value]
	
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
			field_value = field[mx][my]
			if field_value > 0:
				dof=8
			else:
				rx += xo
				ry += yo
				dof+=1

		dist = get_dist(player[0],rx,player[1],ry,player[4],ra) 
		if dist >= temp_ray[2]:
			ray_list.append(temp_ray)
		else:
			ray_list.append([rx, ry, dist, 1, field_value])
		ra += np.pi/180
		ra %= 2*np.pi

	px = player[0]//scale+player_size//scale//2
	py = player[1]//scale+player_size//scale//2
	lines = [] 
	rects = []
	for idx, ray in enumerate(ray_list):
		lines.append([px, py, ray[0]//scale, ray[1]//scale])
		lh = block_size*512/ray[2]
		rects.append([[idx*16+40, 256-lh/2, 16, lh],colors[2*ray[4]-ray[3]]])
	return rects, lines

def render(rects=[]):
	eel.drawRects(rects)

def create_world():
	blocks = [[[0,0,len(field[0])*block_size//scale-1, len(field)*block_size//scale-1],[10,10,10]]]
	for x in range(len(field)):
		for y in range(len(field[x])):
			if field[x][y] > 0:
				blocks.append([[x*block_size//scale,y*block_size//scale,(block_size//scale)-1,(block_size//scale)-1],colors[field[x][y]*2]])
	return blocks

def move_player(player, moves_safe):
	player[0] += moves_safe[1]*player[2]*2
	player[0] -= moves_safe[3]*player[2]*2
	player[1] += moves_safe[1]*player[3]*2
	player[1] -= moves_safe[3]*player[3]*2
	player[4] -= moves_safe[0]*0.05
	player[4] += moves_safe[2]*0.05
	player[4] %= 2*np.pi
	player[2] = np.cos(player[4])
	player[3] = np.sin(player[4])
	return player

moves = np.zeros(4) # left up right down
field = [[1,1,1,1,1,1,1,1],
	 [1,0,3,0,0,0,0,1],
	 [1,0,1,0,0,0,0,1],
	 [1,0,0,0,0,0,0,1],
	 [1,0,0,0,2,1,0,1],
	 [1,1,1,0,0,0,0,1],
	 [1,0,0,0,0,0,0,1],
	 [1,1,1,1,1,1,1,1]]


block_size = 64
player_size = 16
scale = 4
colors = {1:[225,225,225],2:[175,175,175],
	  3:[225,0,0],4:[175,0,0],
	  5:[0,225,0],6:[0,175,0]}
world = create_world()
background = [[[40,0,976,256],[10,10,175]],
	      [[40,256,976,256],[75,75,75]]]



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
	blocked = 0
	if moves[1] == 1:
		if (field[int((player[0]+10*player[2])//64)][int((player[1]+10*player[3])//64)] > 0):
			blocked = 1
	if moves[3] == 1:
		if (field[int((player[0]-10*player[2])//64)][int((player[1]-10*player[3])//64)] > 0):
			blocked = 1
	if 1 in moves:
		scene = []
		r, l = draw_rays()
		scene += background
		scene += r
		scene += world
		scene += [[[player[0]//scale, player[1]//scale, player_size//scale, player_size//scale],[0,255,0]]]
		render(scene)
		eel.drawLines(l)
		if blocked:
			player = move_player(player, [moves[0],0,moves[2],0])
		else:
			player = move_player(player, moves)
	if (datetime.datetime.now() - start).seconds:
		start, fps = print_fps(start, fps)
	fps += 1
		
