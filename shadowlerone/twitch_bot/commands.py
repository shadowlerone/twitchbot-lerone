class Command():
	def __init__(self, func):
		pass
x = {}
def command(name: str, desc: str):
	print(name, desc)
	def wrap(f):
		x[name] = f
		f()
	return wrap

print('after dec')

@command('shadow', 'lerone')
def test():
	print("test successful")

print('after func')
print(x)
x['shadow']()