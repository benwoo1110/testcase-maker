<div align="center">
    <h1>Testcase Maker</h1>
    <h3>Competitive programming testcases made easy!</h3>
    <a href="https://pypi.org/project/testcase-maker/" target="_blank">
        <img src="https://img.shields.io/pypi/v/testcase-maker" alt="pypi" />
    </a>
    <a href="https://testcase-maker.readthedocs.io/en/stable/" target="_blank">
        <img src="https://img.shields.io/readthedocs/testcase-maker" alt="docs" />
    </a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/pypi/pyversions/testcase-maker" alt="python version" />
    </a>
    <a href="LICENSE">
        <img src="https://img.shields.io/github/license/benwoo1110/testcase-maker" alt="license" />
    </a>
</div>

## About
**\*\*NOTE:  The library is a work-in-progress, there may be breaking changes.**

When creating competitive programming challenges, we will also need to create testcases. These testcases mey be very
large with millions of numbers, which makes it near impossible to do manually. This library will allow you to 
automatic this process. It provides an intuitive API to build, generate and validate testcases. 

#### **Testcase Maker** aims to be:

* Very modular and expandable API structure
* Fast and efficient
* Extensive documentation and examples

#### **Testcase Maker** is feature-packed with:

* Highly customisable values to suit large range of challenges
* Separate constraints for subtasks
* Execute answer scripts in java, cpp or python to get stdout

## Installation
This lib is hosted on pypi, thus you can install this lib by typing the following line below:
```
pip install testcase-maker
```

## Basics Usage
You can get start generating testcases with just a few lines of code. Here is simple an example of generating testcases
with N number of random integers, i.
```python
from testcase_maker.generator import TestcaseGenerator
from testcase_maker.values import ValueGroup, NamedValue, RandomInt, LoopValue, ValueRef

values = ValueGroup()
# Define the N value.
values.add(NamedValue(name="N", value=RandomInt(min=50, max=1000)))
values.newline()
# Define the N number of integers.
values.add(LoopValue(
    value=NamedValue(name="i", value=RandomInt(min=1, max=1000)),
    amount=ValueRef("N"),
    delimiter=" ",
))

# Generate stdin testcases
generator = TestcaseGenerator(values=values)
generator.generate_stdin()
```

Some challenge has subtasks with testcases requiring different constraints. Cotinuing from the previous example, here is
how you can do it with **Testcase Maker**.
```python
# ...replacing generator code from the simple example...
# Generate stdin testcases
generator = TestcaseGenerator(values=values)

# Reduce the range of both N and i values.
easy = generator.new_subtask(no_of_testcase=2)
easy.override_value(name="N", value=RandomInt(min=2, max=5))
easy.override_value(name="i", value=RandomInt(min=1, max=100))

# Reduce the range of N. Slightly harder but still less than default.
medium = generator.new_subtask(no_of_testcase=2)
medium.override_value(name="N", value=RandomInt(min=6, max=50))

# Using default constraints. This will generate the largest set of testcases.
hard = generator.new_subtask(no_of_testcase=2)

generator = TestcaseGenerator(values=values)
generator.generate_stdin()
```

Apart from stdin, you can also generate stdout with an answer script. 
```python
# ...replacing generator code from the simple example...
# Generate stdin and stdout testcases
generator = TestcaseGenerator(values=values, answer_script="./solutions.py")
generator.generate()
```

```python
# solution.py
N = int(input())
numbers = [int(x) for x in input().split()]
numbers.sort()
print(" ".join([str(x) for x in numbers]))
```

## Advanced
There is still so many things you can do with this library. For more advanced and detailed usage guide, please refer to 
the [official documentation](https://testcase-maker.readthedocs.io/en/stable/)!
