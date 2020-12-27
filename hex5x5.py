#Raw code to draw hexes
# more to come

import pygame	# the main workhorse
import os		# i KNOW I'll need to detect OS and handle paths, etc
import sys		# for sys.exit
import math 	# for square roots on hex and other polygons

# allows us to use the == QUIT later instead of pygame.locals.QUIT
from pygame.locals import * 


# fixme: put my defs in a functions.py and import them

'''
desc: figure our starting hex
input: starting point, hex built from there
output: return list of tuples of coorids
'''
def hexstart(hops,size,strtx,strty,xy):
	hx1,hy1,hx2,hy2,hx3,hy3,hx4,hy4,hx5,hy5,hx6,hy6,hx7,hy7 = [None]*14
	
	hy6 = strty + ((math.sqrt(3)/2) * size) * 2
	hy2 = strty - ((math.sqrt(3)/2) * size)
 
	if xy == 'y': return strty + (hy2 - hy6) * hops
	if xy == 'x': return strtx - (1.5 * size) * hops

'''
desc:
input:
output:
'''
def draw_board(surf,pulse1,pulse2,lw):

	for xy in h:
		#olor = h[xy][0][0]		# the h dict of lsits has a troubleshooting color
		poly  = h[xy][1]
		pygame.draw.polygon(surf, pulse2,
			poly,
			lw
		)

'''
desc: calc some hex cooridinates and "next one"
input: color, hex count, startx, starty, size of leg, next direction
output: return list of tuples of coorids
'''
def get_hex(color,hxcnt,sx,sy,sz,dr):

	global xs
	global ys

	# reset to default
	xstep,ystep = [0]*2

	# these are the legs for THIS hex
	hx1 = sx - 1.5 * sz
	hy1 = sy + ((math.sqrt(3)/2) * sz)
	hx2 = sx - 1.5 * sz
	hy2 = sy - ((math.sqrt(3)/2) * sz)
	hx3 = sx
	hy3 = sy - ((math.sqrt(3)/2) * sz) * 2
	hx4 = sx + .5 * 3 * sz
	hy4 = sy - ((math.sqrt(3)/2) * sz)
	hx5 = sx + .5 * 3 * sz
	hy5 = sy + ((math.sqrt(3)/2) * sz)
	hx6 = sx
	hy6 = sy + ((math.sqrt(3)/2) * sz) * 2
	hx7 = hx1
	hy7 = hy1

	# but update for the next hex
	if dr == 'nw':
		xstep = sx - 1.5 * sz
		ystep = sy - (hy6 - hy2)
		xs = xstep
		ys = ystep
	elif dr == 'ne':
		xstep = sx + 1.5 * sz
		ystep = sy - (hy6 - hy2)
		xs = xstep
		ys = ystep
	elif dr == 'se':
		xstep = sx + 1.5 * sz
		ystep = sy + hy6 - hy2
		xs = xstep
		ys = ystep
	elif dr == 'sw':
		xstep = sx - 1.5 * sz
		ystep = sy + hy6 - hy2
		xs = xstep
		ys = ystep
	elif dr == 'e':
		xstep = sx + (1.5 * sz * 2)
		xs = xstep
		#ys = ystep
	elif dr == 'w':
		xstep = sx - (1.5 * sz * 2)
		xs = xstep
		#ys = ystep

	# our list of xys are built, kick it back to caller
	# may not use color (can't pulse if we do), but it's here for troubleshooting
	h[hxcnt] = [
		[(color)],
		[(hx1,hy1),(hx2,hy2),(hx3,hy3),(hx4,hy4),(hx5,hy5),(hx6,hy6),(hx7,hy7)]
	]


'''
just pulse 255 to 0 back to 255 repeat 
set boundaries so we don't get invalid rgb value
input: state of the flip, and current color code
return: updated flip and color code
'''
def get_pulse(flipped,c,step):

	if flipped:
		if c < 255: c += step
		else:
			c = 255
			flipped = 0
	else:
		if c > step: c -= step
		else:
			c = 0
			flipped = 1

	if c > 255: c = 255
	if c < 0: c = 0

	return (c,flipped)

'''
desc:
input:
output:
'''
def main():
	# can't run pygame without init, just do it
	pygame.init()

	# clock required to limit fps
	FPS = pygame.time.Clock()

	# one of (possibly many) surfaces to draw on
	SURF = pygame.display.set_mode((W,H))

	# the title bar
	pygame.display.set_caption(title)

	# default colors start at black
	r1,g1,b1 = (0,0,0)
	r2,g2,b2 = (0,0,0)

	# used to pulse color
	flip_r1,flip_g1,flip_b1 = (1,1,1)
	flip_r2,flip_g2,flip_b2 = (1,1,1)

	#Game loop begins
	while True:
		# current color of pulse, r,g,b set at bottom of while 
		r1,flip_r1 = get_pulse(flip_r1,r1,1) # mix and match your pulse, red
		b2,flip_b2 = get_pulse(flip_b2,b2,5) # mix and match your pulse, red
		pulse1 = (r1,g1,b1)
		pulse2 = (r2,g2,b2)

		# fill our surface with white
		SURF.fill(GY)

		# event section
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:

				# update where we just clicked
				(x,y) = pygame.mouse.get_pos()

			if event.type == QUIT:
				# pygame has a buggy quit, do both
				pygame.quit()
				sys.exit()

		
		draw_board(SURF,pulse1,pulse2,lw)
		# update the screen object itself
		pygame.display.update()	# update entire screen if no surface passed

		# tick the fps clock
		FPS.tick(60)


'''
desc: builds global dict of hex data
input: 
output: data for a globla dictionary is built.  ID is unique per hex
# fixme:  why global here, why can't I call build_hexes from inside main?
# fixme: move hc into get_hex
'''
def build_hexes():
	global hc

	# the outer ring of hexes
	get_hex(WH,hc,xs, ys, hx,    'sw'); hc += 1;
	for x in range(0,3,1): get_hex(WH,hc,xs,ys, hx,'sw'); hc += 1;
	for x in range(0,4,1): get_hex(WH,hc,xs,ys, hx,'se'); hc += 1;
	for x in range(0,4,1): get_hex(WH,hc,xs,ys, hx,'e');  hc += 1;
	for x in range(0,4,1): get_hex(WH,hc,xs,ys, hx,'ne'); hc += 1;
	for x in range(0,4,1): get_hex(WH,hc,xs,ys, hx,'nw'); hc += 1;
	for x in range(0,3,1): get_hex(WH,hc,xs,ys, hx,'w');  hc += 1;
	get_hex(WH,hc,xs,ys,hx,'sw'); hc += 1

	# the next inner ring of hexes
	for x in range(0,3,1): get_hex(BL,hc,xs,ys,hx,'sw'); hc += 1
	for x in range(0,3,1): get_hex(BL,hc,xs,ys,hx,'se'); hc += 1
	for x in range(0,3,1): get_hex(BL,hc,xs,ys,hx,'e'); hc += 1
	for x in range(0,3,1): get_hex(BL,hc,xs,ys,hx,'ne'); hc += 1
	for x in range(0,3,1): get_hex(BL,hc,xs,ys,hx,'nw'); hc += 1
	for x in range(0,2,1): get_hex(BL,hc,xs,ys,hx,'w'); hc += 1
	get_hex(BL,hc,xs,ys,hx,'sw'); hc += 1

	# the next inner ring of hexes
	for x in range(0,2,1): get_hex(RE,hc,xs,ys,hx,'sw'); hc += 1
	for x in range(0,2,1): get_hex(RE,hc,xs,ys,hx,'se'); hc += 1
	for x in range(0,2,1): get_hex(RE,hc,xs,ys,hx,'e'); hc += 1
	for x in range(0,2,1): get_hex(RE,hc,xs,ys,hx,'ne'); hc += 1
	for x in range(0,2,1): get_hex(RE,hc,xs,ys,hx,'nw'); hc += 1
	for x in range(0,1,1): get_hex(RE,hc,xs,ys,hx,'w'); hc += 1
	get_hex(RE,hc,xs,ys,hx,'sw'); hc += 1

	# the last few, most inner ring
	get_hex(BL,hc,xs,ys,hx,'sw'); hc += 1
	get_hex(BL,hc,xs,ys,hx,'se'); hc += 1
	get_hex(BL,hc,xs,ys,hx,'e'); hc += 1
	get_hex(BL,hc,xs,ys,hx,'ne'); hc += 1
	get_hex(BL,hc,xs,ys,hx,'nw'); hc += 1
	get_hex(BL,hc,xs,ys,hx,'sw'); hc += 1

	# the center hex
	get_hex(GR,hc,xs,ys,hx,'sw'); hc += 1


# fixme: put these in a config and import them
title = '5x5 hexes'

# fixed colors not in pulse
WH = (255,255,255)  # white
BL = (0,0,0)        # black
GY = (128,128,128)  # grey
RE = (255,0,0)      # red
GR = (0,255,0)	    # green
BU = (0,0,255)		# blue

# this can be adjusted if you like
scale = 40  # 30-80 is probably best scale range
legs = 10 	# this board is 9 hexes across (4,1,4) so +1 on each side = 11
ctr  = 5.5 	#ctr is related to legs.  6 because 1 margin + 4 hexes + 1 center = 6?
			# ratio seems to be:  1/2 of legs + 1, but round down
lw = 3      # line width of polygons, play with odd/even to see what looks best

# 4x4= 2.5
# 5x5= 3.0  
# 6x6= 3.5
hx_sz = 3   		# larger number, scales down the hex
hx = scale/hx_sz	# this is the leg length of each side of hex

# relative game board size based pm legs and scale
W  = int(legs*scale)
H  = int(legs*scale)

# just globals
hc = 100				# just a counter for the dict key
h = {}					# this dict holds the hexes 

xs = ctr * scale 		# starts at center
ys = ctr * scale 		# starts at center
xs = hexstart(5,hx,xs,ys,'x') # well, lets figure it out based on center at least
ys = hexstart(5,hx,xs,ys,'y') # figure it out based on center

# fixme:  need to move this maybe
build_hexes()

if __name__ == '__main__':
	# capture ctrl c
	try:
		main()
	except KeyboardInterrupt:
		# pygame has a buggy quit, do both
		pygame.quit()
		sys.exit()
