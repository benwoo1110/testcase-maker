# Sum of Digits

Testcase generation code for [Sum of Digits](https://www.codechef.com/problems/FLOW006) task on CodeChef.


## `generate.py`
```python
from testcase_maker.generator import TestcaseGenerator
from testcase_maker.values import ValueGroup, NamedValue, RandomInt, LoopValue, ValueRef


# Firstly, create a new container to make the testcase stdin structure.
values = ValueGroup()

# The first line contains an integer T, the total number of testcases.
values.add(NamedValue(
    name="T",
    value=RandomInt(min=1, max=1000)
))

values.newline()

# Then follow T lines, each line contains an integer N.
values.add(LoopValue(
    value=RandomInt(min=1, max=1000000),
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
    res = 0
    while n:
        res += n % 10
        n //= 10
    print(res)
```
