#!/usr/bin/env python3

import cProfile
import zencad
from zencad import *
import time
import zencad.libs.treedy as treedy
import zencad.libs.forces as forces
from zencad.libs.screw import screw
import zencad.libs.kinematic as kinematic

L = 200
rot = kinematic.rotator(name="RBODY",ax=(0,0,1))
body = zencad.assemble.unit(name="N", shape=sphere(20))
a = zencad.assemble.unit(name="A", shape=(cylinder(h=L, r=5)+sphere(10).up(L)).rotateX(deg(90)))
b = zencad.assemble.unit(name="B", shape=(cylinder(h=L, r=5)+sphere(10).up(L)).rotateX(deg(90)))

ra = kinematic.rotator(name="RA",ax=(1,0,0), location=translate(0,-20,0), parent=body)
rb = kinematic.rotator(name="RB",ax=(1,0,0), location=translate(0,20,0)*rotateZ(deg(180)), parent=body)

ra.link(a)
rb.link(b)
rot.link(body)

treedy.attach_inertia(a, mass=1, Ix=1, Iy=1, Iz=1, pose=forw(L))
treedy.attach_inertia(b, mass=1, Ix=1, Iy=1, Iz=1, pose=forw(L))

forces.gravity(unit=a,vec=(0,0,-9.81)).attach(a)
forces.gravity(unit=b,vec=(0,0,-9.81)).attach(b)

t = treedy.tree_dynamic_solver(rot)

#s.set_speed_screw(screw(lin=(0.1,0.1,0.1),ang=(0,0,0)))

#t.calculate_impulses()

t.print_state()
t.print_pre_kinematic_frames()
t.print_post_inertial_objects()
t.print_post_force_sources()
t.print_impulses()

cancel = False
DELTA = 0

cp = cProfile.Profile()

def evaluate():
	global DELTA
	starttime = time.time()
	lasttime = starttime

	time.sleep(2)

	cp.enable()
	while True:
		rot.set_speed(30)
		if cancel:
			return
		maxdelta = 0.0005
		curtime = time.time()
		delta = curtime - lasttime
		lasttime = curtime

		if delta > maxdelta:
			delta = maxdelta
		DELTA = delta

		t.onestep(delta=delta)
#		cp.run("t.onestep(DELTA)")

def animate(self):
	rot.location_update(deep=True, view=True)

import threading
evalthr = threading.Thread(target=evaluate)
evalthr.start()

def close_handle():
	global cancel
	cancel = True
	cp.disable()
	cp.print_stats(sort=1)

disp(rot)
show(animate=animate, animate_step = 0.00001, close_handle=close_handle)