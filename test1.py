m = 'examplemutant0'
o = 'example'
line = 'from example2 import xyz'
line = line.replace(o,m)
print(line)
line = line.replace(m,o)
print(line)

