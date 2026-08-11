from inputs import get_gamepad
while True:
  for e in get_gamepad():
      if e.ev_type == 'Absolute':
        print(e.code, e.state)
