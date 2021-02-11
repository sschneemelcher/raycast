import eel
import numpy as np
import datetime

@eel.expose
def move(k, v):
	if 36 < k < 41:
		global moves
		moves[k-37] = v
	elif k == 77:
		global t_m
		if v:
			t_m = (t_m+1)%2
	
def print_fps(start, fps):
	print(fps)
	return datetime.datetime.now(), 0

def dda():
	rects = []
	lines = []
	w = map_width*k
	for x in range(w):
		camera_x = 2 * x / k / map_width - 1
		ray_dir = player[2:4] + plane * camera_x
		if 0 in ray_dir:
			continue

		map_coords = player[:2]//1
		steps = np.sign(ray_dir)
		delta_dists = steps/ray_dir
		hit = 0
		
		side_dists = (steps * map_coords + (steps+1)*0.5 + (-steps) * player[:2]) * delta_dists

		dof = 0
		while hit == 0 and dof < max_dof:
			side = int(side_dists[1] < side_dists[0])
			map_coords[side] = (map_coords[side]+steps[side]) % map_width
			side_dists[side] += delta_dists[side]
			field_value = field[int(map_coords[0])][int(map_coords[1])]
			if field_value:
				hit = 1
			dof += 1
		if not hit:
			continue
	
		perp_wall_dist = (map_coords[side] - player[side] + (1 - steps[side]) / 2) / ray_dir[side]
		lh = screen_height
		if perp_wall_dist:
			lh /= perp_wall_dist
		lw = screen_width//w
		px = (player[0]*bs+ps*0.5)+player[2]-camera_x
		py = (player[1]*bs+ps*0.5)+player[3]
		rects.append([[x*lw, (screen_height-lh)*0.5, lw, lh],colors[2*field_value-side]])
		lines.append([px, py, px+(ray_dir[0]*perp_wall_dist)*bs-player[2], py+(ray_dir[1]*perp_wall_dist)*bs-player[3]])
	return rects, lines[::int(k**0.5)]

def render(scene=[],lines=[]):
	eel.sleep(0.005)
	eel.drawRects(scene)
	eel.drawLines(lines)

def create_world():
	blocks = [[[0,0,map_width*bs-1, map_height*bs-1],[10,10,10]]]
	for x in range(map_width):
		for y in range(map_height):
			if field[x][y] > 0:
				blocks.append([[x*bs,y*bs,bs-1,bs-1],colors[field[x][y]*2]])
	return blocks

def rotate(mat, degree):
	rot_mat = [[np.cos(degree), -np.sin(degree)],
		   [np.sin(degree), np.cos(degree)]]
	return np.dot(mat,rot_mat)

def move_player(player, plane, moves_safe):
	r = moves_safe[0] - moves_safe[2]
	if r:
		rot = deg*2
		player[2:4] = rotate(player[2:4], r*rot)
		plane = rotate(plane, r*rot)

	player[0] += (moves_safe[1] - moves_safe[3])*player[2]*0.03
	player[1] += (moves_safe[1] - moves_safe[3])*player[3]*0.03
	return player, plane

moves = np.zeros(4) # left up right down
field = [[1,1,1,1,1,1,1,1,1,1],
	 [1,0,3,0,0,0,0,0,0,1],
	 [1,0,1,0,0,1,1,1,0,1],
	 [1,0,1,1,1,1,0,1,0,1],
	 [1,0,0,0,0,0,0,1,0,1],
	 [1,1,1,1,2,1,0,0,0,1],
	 [1,0,0,0,0,0,0,0,0,1],
	 [1,0,0,2,0,0,0,3,3,1],
	 [1,0,0,2,0,0,0,0,0,1],
	 [1,1,1,1,1,1,1,1,1,1]]

## parameters ##
t_m = 0 # toggle map
deg = np.pi/180	 # 1 degree in radian
block_size = 64
scale = 4 # scale for the minimap
k = 24 # rays per block 
bs = block_size//scale
player_size = 16
ps = player_size//scale
colors = {0:[0,255,0],
	  1:[225,225,225],2:[175,175,175],
	  3:[225,0,0],4:[175,0,0],
	  5:[0,225,0],6:[0,175,0]}
screen_width = 960
screen_height = 480
map_width = 10
map_height = 10
max_dof = map_width #max ray length in block sizes
background = [[[0,0,screen_width//(map_width*k)*(map_width*k),screen_height*0.5],[50,0,145]]]
world = create_world()

player = np.zeros(4)
player[:3] = 1
plane = np.zeros(2)
plane[1] = 0.66

eel.init('app')
eel.start('index.html', size=(screen_width+20,screen_height+50), block=False)
start = datetime.datetime.now()
fps = 0
p = t_m*[[[player[0]*bs, player[1]*bs, ps, ps],colors[0]]]
r, l = dda()
render(background + r + t_m*world + p, t_m*l)
while True:
	if 1 in moves:
		blocked = 1
		if moves[1] == 1:
			if (field[int((player[0]+0.1*player[2]))][int((player[1]+0.1*player[3]))] > 0):
				blocked = 0
		if moves[3] == 1:
			if (field[int((player[0]-0.1*player[2]))][int((player[1]-0.1*player[3]))] > 0):
				blocked = 0
		r, l = dda()
		p = t_m*[[[player[0]*bs,player[1]*bs,ps,ps],[colors[0]]]]
		render(background+r+t_m*world + p, t_m*l)
		player, plane = move_player(player, plane, [moves[0],moves[1]*blocked,moves[2],moves[3]*blocked])
	else:
		eel.sleep(0.02)
	fps += 1
	if (datetime.datetime.now() - start).seconds:
		start, fps = print_fps(start, fps)
