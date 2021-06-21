#include <stdio.h>
#include <stack>

#include "xbyak/xbyak.h"

#define MEMSIZE 30000
#define CODESIZE 50000

char* label(char ch, int num) {
  static char labelbuf[BUFSIZ];
  snprintf(labelbuf, sizeof(labelbuf), "%c%d", ch, num);
  return labelbuf;
}

class BF : public Xbyak::CodeGenerator {
 public:
  BF(FILE *input, int membuf[MEMSIZE])
      : CodeGenerator(CODESIZE)
  {
    Xbyak::Reg64 memreg = rbx;
    Xbyak::Address mem = dword[memreg];

    push(rbx);
    mov(memreg, (intptr_t) membuf);

    std::stack<int> leftstack;
    int labelNum = 0;
    int ch;
    while ((ch = getc(input)) != EOF) {
      switch (ch) {
      case '+':  inc(mem); break;
      case '-':  dec(mem); break;
      case '>':  add(memreg, 4); break;
      case '<':  add(memreg, -4); break;
      case ',':
        mov(rax, (intptr_t)getchar);
        call(rax);
        mov(mem, eax);
        break;
      case '.':
        mov(edi, mem);
        mov(rax, (intptr_t)putchar);
        call(rax);
        break;
      case '[':
        L(label('L', labelNum));
        mov(eax, mem);
        test(eax, eax);
        jz(label('R', labelNum), T_NEAR);

        leftstack.push(labelNum);
        ++labelNum;
        break;
      case ']':
        {
          int index = leftstack.top();
          leftstack.pop();

          jmp(label('L', index), T_NEAR);
          L(label('R', index));
        }
        break;
      }
    }
    pop(rbx);
    ret();
  }

  void operator()() {
    void (*code)() = getCode<void(*)(void)>();
    (*code)();
  }
};

int main() {
  static int membuf[MEMSIZE];
  BF bf(stdin, membuf);
  bf();
  return 0;
}
