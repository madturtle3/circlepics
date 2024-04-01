import pygame
import math
import numpy
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("courier",20)
def ctop(p):
    # cartesian to polar
    x = p[0]
    y = p[1]
    return math.sqrt(x**2+y**2),math.atan2(y,x)

def ptoc(p):
    # polar to cartesian
    r = p[0]
    t = p[1]
    return r*math.cos(t),r*math.sin(t)

def rtop(p):
    # pygame to real
    x = p[0]
    y = p[1]
    return (x+(window.get_width()/2),-y+(window.get_height()/2))

def ptor(p):
    # real to pygame
    x = p[0]
    y = p[1]
    return (x-(window.get_width()/2),-y-(window.get_height()/2))

def addpoint(p1,p2):
    return p1[0]+p2[0],p1[1]+p2[1]

def getcolor(colormult):
    if colormult < .5:
        return (255,0,(colormult+.5) * 255)
    elif colormult == .5:
        return (255,0,255)
    elif colormult > .5:
        return (abs(1-colormult+.5)*255,0,255)




debugprint=True
circlemode=False
fastmode=False
t=0
framerate=120
radius=250
tstep=.1



speeds=(1,13,-53)
lengths = (.41,2.02,.57)


jitter = 0
playing = True
paused=False
trackframes=True
window = pygame.display.set_mode((radius*2.5,radius*2.5))
trails = []
vectors = list(zip(lengths,speeds))
for _ in vectors:
    trails.append([])
clock = pygame.time.Clock()
# calculate total vector sizes
totalsize = 0
for size,speed in vectors:
    totalsize += size
    jitter += abs(speed)
tstep = (.1/jitter) / 25
if fastmode and circlemode:
    pygame.draw.circle(window,(255,255,255),rtop((0,0)),radius,1)
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tstep -= (tstep/2)
            if event.key == pygame.K_RIGHT:
                tstep += (tstep/2)
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_r:
                window.fill((0,0,0))
                if circlemode:
                    pygame.draw.circle(window,(255,255,255),rtop((0,0)),radius,1)
                t=0
                trails = []
                for _ in vectors:
                    trails.append([])
            if event.key == pygame.K_f:
                trackframes = not trackframes
                
            if event.key == pygame.K_v:
                window.fill((0,0,0))
                if circlemode:
                    pygame.draw.circle(window,(255,255,255),rtop((0,0)),radius,1)
                for index, trail in enumerate(trails):
                    if (debugprint == False and index == len(trails)-1) or debugprint==True:
                        colormult = (index+1)/len(trails)
                        if len(trail) > 2:
                            if fastmode:
                                pygame.draw.aaline(window,getcolor(colormult),trail[-2],trail[-1])
                            else:
                                pygame.draw.aalines(window,getcolor(colormult),False,trail)
                fastmode = not fastmode

    if not paused:
        point=(0,0)
        points=[rtop((0,0))]
        for index, (size,speed) in enumerate(vectors):
            spoint = ptoc(((size/totalsize)*radius,t*speed))
            point = addpoint(point,spoint)
            points.append(rtop(point))
            trails[index].append(rtop(point))
        if not fastmode:
            window.fill((0,0,0))
            if circlemode:
                pygame.draw.circle(window,(255,255,255),rtop((0,0)),radius,1)
            pygame.draw.aalines(window,(255,255,255),False,points)
        for index, trail in enumerate(trails):
            if (debugprint == False and index == len(trails)-1) or debugprint==True:
                colormult = (index+1)/len(trails)
                if len(trail) > 2:
                    if fastmode:
                        pygame.draw.aaline(window,getcolor(colormult),trail[-2],trail[-1])
                    else:
                        pygame.draw.aalines(window,getcolor(colormult),False,trail)
        img = font.render(f"rate:  {clock.get_fps():6.1f}/{framerate:4.1f} speed: {tstep:5.5f}",True,(255,255,255),(0,0,0))
        img2 = font.render(f"framecap (f): {trackframes:1b} fastmode (v): {fastmode:1b}",True,(255,255,255),(0,0,0))
        window.blit(img,(0,0))
        window.blit(img2,(0,20))
        pygame.display.flip()
        t += tstep
    if trackframes:
        clock.tick(framerate)
    else:
        clock.tick(10000)