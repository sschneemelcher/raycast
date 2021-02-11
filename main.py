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
		camera_x = 2 * x*k**-1 / map_width - 1
		ray_dir_x = player[2] + plane[0] * camera_x
		ray_dir_y = player[3] + plane[1] * camera_x
		if ray_dir_x == 0 or ray_dir_y == 0:
			continue

		map_x = int(player[0])
		map_y = int(player[1])
		
		delta_dist_x = np.abs(ray_dir_x**-1);
		delta_dist_y = np.abs(ray_dir_y**-1);
		hit = 0

		if ray_dir_x < 0:
			step_x = -1
			side_dist_x = (player[0] - map_x) * delta_dist_x
		else:
			step_x = 1
			side_dist_x = (map_x + 1 - player[0]) * delta_dist_x;

		if ray_dir_y < 0:
			step_y = -1
			side_dist_y = (player[1] - map_y) * delta_dist_y
		else:
			step_y = 1
			side_dist_y = (map_y + 1 - player[1]) * delta_dist_y;

		dof = 0
		while hit == 0 and dof < max_dof:
			if side_dist_x < side_dist_y:
				side_dist_x += delta_dist_x;
				map_x += step_x
				side = 0
			else:
				side_dist_y += delta_dist_y
				map_y += step_y
				side = 1
			field_value = field[map_x][map_y]
			if field_value > 0:
				hit = 1
			dof += 1
		if hit == 0:
			continue
	
		if side == 0:
			perp_wall_dist = (map_x - player[0] + (1 - step_x) / 2) / ray_dir_x
		else:
			perp_wall_dist = (map_y - player[1] + (1 - step_y) / 2) / ray_dir_y
		
		lh = screen_height / max(perp_wall_dist,1)
		lw = screen_width//w
		px = (player[0]*bs+ps//2)+player[2]-camera_x
		py = (player[1]*bs+ps//2)+player[3]
		rects.append([[x*lw, (screen_height*0.5)-lh*0.5, lw, lh],colors[2*field_value-side]])
		lines.append([px, py, px+(ray_dir_x*perp_wall_dist)*bs-player[2], py+(ray_dir_y*perp_wall_dist)*bs-player[3]])
	return rects, lines

def render(scene=[],lines=[]):
	eel.sleep(0.01)
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
k = 12 # rays per block 
bs = block_size//scale
player_size = 16
ps = player_size//scale
colors = {0:[0,255,0],
	  1:[225,225,225],2:[175,175,175],
	  3:[225,0,0],4:[175,0,0],
	  5:[0,225,0],6:[0,175,0]}
world = create_world()
screen_width = 960
screen_height = 480
map_width = 10
map_height = 10
max_dof = map_width #max ray length in block sizes
background = [[[0,0,screen_width//(map_width*k)*(map_width*k),screen_height*0.5],[50,0,145]]]

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
