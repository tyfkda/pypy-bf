try:
  from rpython.rlib.jit import JitDriver
  from rpython.rlib.jit import purefunction
except ImportError:
  class JitDriver(object):
    def __init__(self,**kw): pass
    def jit_merge_point(self,**kw): pass
    def can_enter_jit(self,**kw): pass

  def purefunction(f):
    return f

def get_location(pc, program, bracket_map, tape):
    return "%s_%s_%s" % (
      program[:pc], program[pc], program[pc+1:]
    )

jitdriver = JitDriver(
  greens=['pc', 'program', 'bracket_map', 'tape'],
  reds=['head'],
  get_printable_location=get_location)

@purefunction
def get_matching_bracket(bracket_map, pc):
    return bracket_map[pc]

def mainloop(program, bracket_map, putc, getc):
  tape = [0] * 30000
  pc = 0
  head = 0
  while pc < len(program):
    jitdriver.jit_merge_point(pc=pc, head=head, tape=tape, program=program,
                              bracket_map=bracket_map)

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
        #pc = bracket_map[pc]
        pc = get_matching_bracket(bracket_map, pc)
    elif code == ']':
      if tape[head] != 0:
        #pc = bracket_map[pc]
        pc = get_matching_bracket(bracket_map, pc)

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
