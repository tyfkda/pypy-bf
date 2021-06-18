def mainloop(program, bracket_map, putc, getc):
  tape = [0] * 30000
  pc = 0
  head = 0
  while pc < len(program):
    code = program[pc]

    if code == '>':
      head += 1
    elif code == '<':
      head -= 1
    elif code == '+':
      tape[head] += 1
    elif code == '-':
      tape[head] -= 1
    elif code == '.':
      putc(tape[head])
    elif code == ',':
      tape[head] = getc()
    elif code == '[':
      if tape[head] == 0:
        pc = bracket_map[pc]
    elif code == ']':
      if tape[head] != 0:
        pc = bracket_map[pc]

    pc += 1


def parse(program):
  parsed = []
  bracket_map = {}
  leftstack = []

  pc = 0
  for char in program:
    if char in ('[', ']', '<', '>', '+', '-', ',', '.'):
      parsed.append(char)

      if char == '[':
        leftstack.append(pc)
      elif char == ']':
        left = leftstack.pop()
        right = pc
        bracket_map[left] = right
        bracket_map[right] = left
      pc += 1

  return ''.join(parsed), bracket_map
