#include <cstdio>
#include <fstream>
#include <unordered_map>
#include <iostream>
#include <stack>
#include <vector>

using namespace std;

void mainloop(const string& program, unordered_map<int, int>& bracketMap) {
  auto tape = vector<unsigned char>(30000);
  unsigned char *head = &tape[0];
  for (int pc = 0; pc < static_cast<int>(program.size()); ++pc) {
    auto code = program[pc];
    switch (code) {
    case '>':  ++head; break;
    case '<':  --head; break;
    case '+':  ++*head; break;
    case '-':  --*head; break;
    case '.':  putchar(*head); break;
    case ',':  *head = getchar(); break;
    case '[':  if (*head == 0)  pc = bracketMap[pc]; break;
    case ']':  if (*head != 0)  pc = bracketMap[pc]; break;
    default:  break;
    }
  }
}

auto parse(const string& program) {
  string parsed;
  unordered_map<int, int> bracketMap;
  stack<int> leftstack;

  for (size_t i = 0; i < program.size(); ++i) {
    int c = program[i];
    if (strchr("[]<>+-,.", c) != NULL) {
      int pc = parsed.size();
      parsed.push_back(c);

      switch (c) {
      case '[':
        leftstack.push(pc);
        break;
      case ']':
        {
          int left = leftstack.top();
          leftstack.pop();
          int right = pc;
          bracketMap[left] = right;
          bracketMap[right] = left;
        }
        break;
      default:  break;
      }
    }
  }

  struct Result {
    string parsed;
    unordered_map<int, int> bracketMap;
  };
  return Result {parsed, bracketMap};
}

string readFile(const string& filename) {
  std::ifstream file(filename);

  if (!file.is_open())
    throw "Cannot open file";

  std::string content;
  while (file.good()) {
    int c = file.get();
    if (file.eof())
      break;
    content.push_back(c);
  }
  return content;
}

int main(int argc, char *argv[]) {
  if (argc < 2) {
    cerr << "argc < 2" << endl;
  }

  try {
    auto source = readFile(argv[1]);
    auto [program, bm] = parse(source);
    mainloop(program, bm);
  } catch (const char *err) {
    cerr << err << endl;
    return 1;
  }

  return 0;
}
