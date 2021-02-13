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
		t_m = (t_m+v)%2
	
def print_fps(start, fps):
	print(fps)
	return datetime.datetime.now(), 0

def sign(a):
	if (a > 0):
		return 1
	return -1

def dot(a, b):
	return [sum([a[i]*b[i][j] for i in [0,1]]) for j in [0,1]]

def dda():
	rects = []
	lines = []
	w = map_width*k
	llh = 0	
	for x in range(w):
		camera_x = 2 * x / k / map_width - 1
		ray_dir = [player[i+2] + plane[i] * camera_x for i in [0,1]]
		if 0 in ray_dir:
			continue

		map_coords = [int(p) for p in player[:2]]
		steps = [sign(rd) for rd in ray_dir]
		delta_dists = [steps[i]/ray_dir[i] for i in [0,1]]
		hit = 0
		
		side_dists = [(steps[i] * map_coords[i] + (steps[i]+1)*0.5 + (-steps[i]) * player[i]) * delta_dists[i] for i in [0,1]]

		dof = 0
		while not hit and dof < max_dof:
			side = int(side_dists[1] < side_dists[0])
			map_coords[side] = (map_coords[side]+steps[side]) % map_width
			side_dists[side] += delta_dists[side]
			field_value = field[map_coords[0]][map_coords[1]]
			if field_value:
				hit = 1
			dof += 1
		if not hit:
			continue
	
		perp_wall_dist = (map_coords[side] - player[side] + (1 - steps[side]) * 0.5) * ray_dir[side]**-1
		lh = screen_height
		if perp_wall_dist:
			lh /= perp_wall_dist
		lw = screen_width//w
		px = (player[0]*bs+ps*0.5)-camera_x
		py = (player[1]*bs+ps*0.5)
		rects.append([[x*lw, (screen_height-lh)*0.5, lw, lh],colors[2*field_value-side]])
		lines.append([px, py, px+(ray_dir[0]*perp_wall_dist)*bs, py+(ray_dir[1]*perp_wall_dist)*bs])
	return rects, lines[::k]

def render(scene=[],lines=[]):
	eel.sleep(0.00001)
	eel.drawRects(scene)
	eel.drawLines(lines)

def create_world():
	blocks = [[[0,0,map_width*bs-1, map_height*bs-1],[10,10,10]]]
	for x in range(map_width):
		for y in range(map_height):
			if field[x][y] > 0:
				blocks.append([[x*bs,y*bs,bs-1,bs-1],colors[field[x][y]*2]])
	return blocks

def rotate(mat, sgn):
	rot_mat = [[cos, sgn*(-sin)],
		   [sgn*sin, cos]]
	return dot(mat,rot_mat)

def move_player(player, plane, moves_safe):
	r = moves_safe[0] - moves_safe[2]
	if r:
		player[2:] = rotate(player[2:], r)
		plane = rotate(plane, r)

	player[0] += (moves_safe[1] - moves_safe[3])*player[2]*0.03
	player[1] += (moves_safe[1] - moves_safe[3])*player[3]*0.03
	return player, plane

moves = [0,0,0,0] # left up right down
## parameters ##
t_m = 0 # toggle map
deg = np.pi/180	 # 1 degree in radian
rot = deg*2 # rotation angle for the player
sin = np.sin(rot)
nsin = np.sin(-rot)
cos = np.cos(rot)
block_size = 64
scale = 8 # scale for the minimap
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
map_width = 20
map_height = 20
field = np.pad(np.random.choice([0,1,2,3], size=(map_width-2,map_height-2), p=(2/3,1/9,1/9,1/9)), [(1,1),(1,1)], mode='constant', constant_values=(1))
field[1,1] = 0
max_dof = (map_width-1)//2 #max ray length in block sizes
background = [[[0,0,screen_width//(map_width*k)*(map_width*k),screen_height*0.5],[50,0,145]]]
world = create_world()

player = [1,1,1,0]
plane = [0,0.66]

eel.init('app')
eel.start('index.html', size=(screen_width+20,screen_height+50), block=False)
#eel.setup()
start = datetime.datetime.now()
fps = 0
p = t_m*[[[player[0]*bs, player[1]*bs, ps, ps],colors[0]]]
r, l = dda()
render(background + r + t_m*world + p, t_m*l)
while True:
	if 1 in moves:
		blocked = 1
		if moves[1] == 1 or moves[3] == 1:
			if (field[int((player[0]+ (1-2*moves[3]) * 0.1*player[2])), int((player[1]+ (1-2*moves[3]) * 0.1*player[3]))] > 0):
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
