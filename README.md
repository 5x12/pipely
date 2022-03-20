The library `pipely` can execute any class or any sequence of classes in any order. 
To install the library:
```bash
pip install pipely
```

# 1. Quick Start

To build a pipeline with executable classes, create a config `.yml` file in the following format:

```text
steps:
    [step_name_1]:
        exec: [relative path to a file]:[class to execute]
    [step_name_2]:
        exec: [relative path to a file]:[class to execute]
    [step_name_3]:
        exec: [relative path to a file]:[class to execute]
        depends_on:
        - [step_name_1]
        - [step_name_2]
```

> - names of `[steps]` should be unique;
> - the executable classes should have a ``__call__`` method (see example below);
> - with `depends_on`, pipely is able to detect independent steps and execute them in parallel;



Then trigger the pipeline in cli:

```bash
python -m pipely from-pipeline <file.yml> [dict.json]
```

- `<file.yml>` (a required argument) is the path to a yaml config file. Supports any format: `../../file.yml`, or `path/to/file.yml`, or `file.yml`.
- `[dict.json]` (an optional argument) is the path to a `json` file (a shared dictionary) if value exchange between classes is needed (more in sec 1.2.)


<!-- > - it's possible to add an argument to ``__call__``, which is used by pipely to share a dictionary between classes, thus permitting simple value transmission from class to class (see example below); -->

## 1.1. Example

Let's create a `test.yml` config file:

```text
steps:
    a1_print:
        exec: src/file1.py:firstA
    a2_print:
        exec: src/file1.py:secondA
    final_print:
        exec: src/file2.py:printDone
        depends_on:
        - a_print
        - b_print
```
Because of `depends_on` parameter:
1. firstly, `a1_print` and `a2_print` are executed in parallel
2. only then `final_print` is executed

Let's look at `firstA`, `secondA` and `printDone` classes (you can check them in `example/` folder) and ensure that each has a `__call__` method without which pipely won't work:

```python
#example/src/file1.py

class firstA:
    def run(self):
        a = 32
        print(a)

    def __call__(self):
        self.run()

class secondA:
    def run(self):
        a = 12
        print(a)

    def __call__(self):
        self.run()
```
```python
#example/src/file2.py

class printDone:
    def run(self):
        print("Done.")

    def __call__(self):
        self.run()
```

Then trigger the pipeline in cli with:
```bash
python -m pipely from-pipeline test.yml
```


## 1.2. Example w/ shared dictionary

Let's create a `testContext.yml` config file:

```text
steps:
    a_first:
        exec: src/file1_shared.py:firstA
    a_second:
        exec: src/file1_shared.py:secondA
    a_sum:
        exec: src/file2_shared.py:aSum
        depends_on:
        - a_first
        - a_second
    a_sum_print:
        exec: src/file3_shared.py:aSumPrint
        depends_on:
            - a_sum
```

1. first, `a_first` and `a_second` are executed in parallel
2. then `a_sum` sums up both a's in the previous steps
3. finally, `a_sum_print` prints the final result

Let's look at classes in the first 2 steps (you can check them in `example/` folder):

```python
#example/src/file1_shared.py

class firstA:
    def run(self):
        a = 32
        self.result = a

    def __call__(self, context): #adding context in __call__
        self.run()
        context["a1"] = self.result #to use the result in another class

class secondA:
    def run(self):
        a = 12
        self.result = a

    def __call__(self, context): #adding context in __call__
        self.run()
        context["a2"] = self.result #to use the result in another class
```
Now we can use `a1` and `a2` in another class: 

```python
#example/src/file2_shared.py

class aSum:
    def run(self, context):
        a1 = context["a1"] #extracting from shared dictionary
        a2 = context["a2"] #extracting from shared dictionary
        self.result = a1 + a2

    def __call__(self, context):
        self.run()
        context["aSum"] = self.result #saving to shared dictionary

```

Then trigger the pipeline in cli with the specified path to `context.json`:

```bash
python -m pipely from-pipeline collect.yml context.json
```

# 2. Imperative way
Pipely can also trigger a specific class from a specific .py file.

```bash
python -m pipely from-class path/to/file.py:TestClass
```

Below is an example of command that triggers a `firstA` class from `src/file1.py`.

```bash
python -m pipely from-class src/file1.py:firstA
```

If your class needs to operate on a shared dictionary, the command `from-class` could use an optional second argument. This argument awaits a path to a json representing the shared dictionary.

```bash
python -m pipely from-class src/file1_shared.py:firstA src/context.json
```