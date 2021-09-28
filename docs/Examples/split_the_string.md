# Split the Str Ing

Testcase generation code for [Split the Str Ing](https://www.codechef.com/problems/SPLITIT) task on CodeChef.

## `generate.py`
```python
import string

from testcase_maker.generator import TestcaseGenerator
from testcase_maker.values import ValueGroup, NamedValue, RandomInt, LoopValue, ValueRef, RandomItem

# Firstly, create a new container to make the testcase stdin structure.
values = ValueGroup()

# The first line of the input contains a single integer T denoting the number of test cases.
values.add(NamedValue(
    name="T",
    value=RandomInt(min=1, max=10**4)
))
values.newline()

# For each testcase:
#  - The first line of each test case contains a single integer N.
#  - The second line contains a single string S.
testcase = ValueGroup()
testcase.add(NamedValue(
    name="N",
    value=RandomInt(min=2, max=10**5)
))
testcase.newline()
testcase.add(LoopValue(
    value=RandomItem(items=list(string.ascii_lowercase)),
    amount=ValueRef(name="N"),
    delimiter=""
))

# Then create T number of testcases.
values.add(LoopValue(
    value=testcase,
    amount=ValueRef(name="T"),
    delimiter="\n"
))


# Generate the testcases
generator = TestcaseGenerator(values=values, answer_script="./solution.py")
generator.generate()
```

## `solution.py`
```python
T = int(input())

for _ in range(T):
    n = int(input())
    word = input().rstrip()
    mapping = {}
    for letter in word:
        if letter in mapping:
            mapping[letter] += 1
        else:
            mapping[letter] = 1

    last = mapping.get(word[-1], 0)
    print("YES" if last > 1 else "NO")
```
