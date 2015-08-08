# KSP X-55 Script Version 1

# Clear your X-55 profile to enable the mode switch to act as buttons.
# M1: Plane mode
# M2: Rocket mode (Switches Roll and Yaw controls)
# M3: EVA mode

# This script assumes default keyboard settings, except you should bind
# "camera reset" to "slash". The default button for this is backspace, which is also bound to "abort".

# vJoy joystick should have all axes enabled. Axes in KSP should have dead zones disabled except the rover throttle.
# Axes in KSP should be bound as follows:
#
# (Flight) Pitch Axis: vJoy - Virtual Joystick Axis 1
# (Flight) Roll Axis: vJoy - Virtual Joystick Axis 0
# (Flight) Yaw Axis: vJoy - Virtual Joystick Axis 2
# (Flight) Throttle Axis: vJoy - Virtual Joystick Axis 5 INVERTED
#
# (Vessel) Steering Axis: vJoy - Virtual Joystick Axis 2 INVERTED
# (Vessel) Throttle Axis: vJoy - Virtual Joystick Axis 5 INVERTED and WITH a dead zone
#
# (Game) Camera Horizontal: vJoy - Virtual Joystick Axis 3
# (Game) Camera Vertical: vJoy - Virtual Joystick Axis 4

# This script can bind the X-55 mouse stick as joystick axes. This requires a registry modification:
# https://www.reddit.com/r/hotas/comments/2rs6un/how_to_turn_x55_mouse_ministick_into_joystick_axes/
# With this modification, it will become an analog camera control hat.

# Edit these values to change dead zones
xDeadzone = 0.05
yDeadzone = 0.05
twistDeadzone = 0.1
rotaryDeadzone = 0.05

range = 1000 # Maximum value of joystick axis
stick = joystick[1] # May need to change joystick ids
throttle = joystick[2]

def curve(x, a=0.66): # Change "a" value to change joystick curve. 0 is linear, 1 is cubic
	x = (x*1.0)/range
	return (a*x*x*x + (1-a)*x)*range

def mapToVJoy(x):
	return (x*vJoy[0].axisMax)/range

rocketMode = stick.getDown(15)
evaMode = stick.getDown(16)

if rocketMode:
	vJoy[0].x = mapToVJoy(curve(filters.deadband(stick.zRotation, twistDeadzone, -range, range)))
	vJoy[0].y = mapToVJoy(curve(filters.deadband(stick.y, yDeadzone, -range, range)))
	vJoy[0].z = mapToVJoy(curve(filters.deadband(stick.x, xDeadzone, -range, range)))
elif evaMode:
	vJoy[0].rx = mapToVJoy(curve(filters.deadband(stick.x, xDeadzone, -range, range))) - mapToVJoy(throttle.sliders[1])
	vJoy[0].ry = mapToVJoy(curve(filters.deadband(stick.y, twistDeadzone, -range, range))) + mapToVJoy(throttle.sliders[0])
	keyboard.setKey(Key.E, stick.zRotation > range/2)
	keyboard.setKey(Key.Q, stick.zRotation < -range/2)
else:
	vJoy[0].x = mapToVJoy(curve(filters.deadband(stick.x, xDeadzone, -range, range)))
	vJoy[0].y = mapToVJoy(curve(filters.deadband(stick.y, yDeadzone, -range, range)))
	vJoy[0].z = mapToVJoy(curve(filters.deadband(stick.zRotation, twistDeadzone, -range, range)))

#diagnostics.watch(stick.x)
#diagnostics.watch(vJoy[0].x)

throttleAxis = mapToVJoy(throttle.y)
if throttleAxis == 16382:
	throttleAxis *= 2
vJoy[0].rz = throttleAxis

if not evaMode:
	vJoy[0].rx = -mapToVJoy(throttle.sliders[1])
	vJoy[0].ry = mapToVJoy(throttle.sliders[0])
	
vJoy[0].slider = mapToVJoy(filters.deadband(throttle.xRotation, rotaryDeadzone, -range, range))
vJoy[0].dial = mapToVJoy(filters.deadband(throttle.z, rotaryDeadzone, -range, range))

#diagnostics.watch(throttle.y)
#diagnostics.watch(vJoy[0].rz)

keyboard.setKey(Key.R, stick.getDown(2))
keyboard.setKey(Key.M, stick.getDown(4))

pov = stick.pov[0]
keyboard.setKey(Key.UpArrow, pov == 0 or pov == 4500 or pov == 31500)
keyboard.setKey(Key.RightArrow, pov == 4500 or pov == 9000 or pov == 13500)
keyboard.setKey(Key.DownArrow, pov == 13500 or pov == 18000 or pov == 22500)
keyboard.setKey(Key.LeftArrow, pov == 22500 or pov == 27000 or pov == 31500)

keyboard.setKey(Key.V, throttle.getDown(27))
keyboard.setKey(Key.C, throttle.getDown(28))
keyboard.setKey(Key.Period, throttle.getDown(9))
keyboard.setKey(Key.Comma, throttle.getDown(10))
keyboard.setKey(Key.Slash, throttle.getDown(34))

if throttle.getPressed(29):
	mouse.wheel = mouse.wheelMax

if throttle.getPressed(30):
	mouse.wheel = -mouse.wheelMax

if evaMode:
	keyboard.setKey(Key.Space, stick.getDown(0))
	keyboard.setKey(Key.B, stick.getDown(1))
	keyboard.setKey(Key.F, stick.getDown(3))
	keyboard.setKey(Key.LeftAlt, stick.getDown(5))
	
	keyboard.setKey(Key.L, throttle.getDown(4))
	
	keyboard.setKey(Key.W, throttle.getDown(20))
	keyboard.setKey(Key.S, throttle.getDown(22))
	keyboard.setKey(Key.A, throttle.getDown(26))
	keyboard.setKey(Key.D, throttle.getDown(24))
	keyboard.setKey(Key.LeftShift, throttle.getDown(34) or throttle.getDown(23))
	keyboard.setKey(Key.LeftControl, throttle.getDown(25))
else:
	keyboard.setKey(Key.F, stick.getDown(0))
	keyboard.setKey(Key.Space, stick.getDown(1))
	keyboard.setKey(Key.T, stick.getDown(3))
	keyboard.setKey(Key.B, stick.getDown(5))
	
	keyboard.setKey(Key.CapsLock, throttle.getDown(0))
	keyboard.setKey(Key.Backspace, throttle.getDown(1))
	keyboard.setKey(Key.G, throttle.getDown(3))
	keyboard.setKey(Key.U, throttle.getDown(4))
	
	trimming = stick.getDown(7) or stick.getDown(9) or stick.getDown(10) or stick.getDown(11) or stick.getDown(12) or stick.getDown(13) or throttle.getDown(2)
	keyboard.setKey(Key.LeftAlt, trimming)
	keyboard.setKey(Key.W, stick.getDown(10))
	keyboard.setKey(Key.S, stick.getDown(12))
	keyboard.setKey(Key.X, throttle.getDown(2))
	if rocketMode:
		keyboard.setKey(Key.D, stick.getDown(11))
		keyboard.setKey(Key.A, stick.getDown(13))
		keyboard.setKey(Key.E, stick.getDown(7))
		keyboard.setKey(Key.Q, stick.getDown(9))
	else:
		keyboard.setKey(Key.E, stick.getDown(11))
		keyboard.setKey(Key.Q, stick.getDown(13))
		keyboard.setKey(Key.D, stick.getDown(7))
		keyboard.setKey(Key.A, stick.getDown(9))

	keyboard.setKey(Key.H, throttle.getDown(20))
	keyboard.setKey(Key.N, throttle.getDown(22))
	keyboard.setKey(Key.K, throttle.getDown(23))
	keyboard.setKey(Key.L, throttle.getDown(24))
	keyboard.setKey(Key.I, throttle.getDown(25))
	keyboard.setKey(Key.J, throttle.getDown(26))
	
	keyboard.setKey(Key.D1, throttle.getDown(11))
	keyboard.setKey(Key.D2, throttle.getDown(12))
	keyboard.setKey(Key.D3, throttle.getDown(13))
	keyboard.setKey(Key.D4, throttle.getDown(14))
	keyboard.setKey(Key.D5, throttle.getDown(15))
	keyboard.setKey(Key.D6, throttle.getDown(16))
	keyboard.setKey(Key.D7, throttle.getDown(5))
	keyboard.setKey(Key.D8, throttle.getDown(6))
	keyboard.setKey(Key.D9, throttle.getDown(7))
	keyboard.setKey(Key.D0, throttle.getDown(8))