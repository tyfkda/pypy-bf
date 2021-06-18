import bf

def putc(c):
  sys.stdout.write(chr(c))  #; sys.stdout.flush()

def getc():
  return ord(sys.stdin.read(1))

def run(input):
  program, map = bf.parse(input.read())
  bf.mainloop(program, map, putc, getc)

if __name__ == '__main__':
  import sys
  run(open(sys.argv[1], 'r'))
