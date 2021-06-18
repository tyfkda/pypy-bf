import bf
import os

def putc(c):
  os.write(1, chr(c))

def getc():
  return ord(os.read(0, 1)[0])

def run(fp):
  program_contents = ''
  while True:
    read = os.read(fp, 4096)
    if len(read) == 0:
      break
    program_contents += read
  os.close(fp)
  program, bm = bf.parse(program_contents)
  bf.mainloop(program, bm, putc, getc)

def entry_point(argv):
  try:
    filename = argv[1]
  except IndexError:
    print('You must supply a filename')
    return 1

  run(os.open(filename, os.O_RDONLY, 0o777))
  return 0

def target(*args):
  return entry_point, None

if __name__ == '__main__':
  import sys
  entry_point(sys.argv)
