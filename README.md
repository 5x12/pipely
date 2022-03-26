The light pipeline library `pipely` can execute any class or any sequence of classes in any order. Install with:
```bash
pip install pipely
```

# 1. Quick Start

To build a pipeline with executable classes, create a config `.yaml` file in the following format:

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

> - `[steps]` names should be unique;
> - `depends_on` defines order and enables pipely to detect independent steps and execute them in parallel;
> - the executable classes should have a ``__call__`` method (see example below);



Then trigger the pipeline in cli:

```bash
python -m pipely from-pipeline <file.yaml> [dict.json]
```

> - `<file.yaml>` (required) is the path to a yaml config file (any format): `../../file.yaml`, or `path/to/file.yaml`, or `file.yaml`.
> - `[dict.json]` (optional argument) is the path to a shared dictionary `json` file if value exchange between classes is needed (more in Section 1.2.)


<!-- > - it's possible to add an argument to ``__call__``, which is used by pipely to share a dictionary between classes, thus permitting simple value transmission from class to class (see example below); -->

## 1.1. Example

Let's create a [test.yaml](example/test.yaml) config file:

```text
steps:
    a1_print:
        exec: src/file1.py:firstA
    a2_print:
        exec: src/file1.py:secondA
    final_print:
        exec: src/file2.py:printDone
        depends_on:
        - a1_print
        - a2_print
```
`depends_on` parameter sets the following order for pipely:

1. firstly execute `a1_print` and `a2_print` in parallel
2. and then execute `final_print`

Let's look at executable classes. To use pipely, the executable classes should have a `__call__` method, as shown below (check [example/src/](example/src)):

```python
#example/src/file1.py

class firstA:
    def run(self):
        a = 32
        print(a)

    def __call__(self): #call method
        self.run()

class secondA:
    def run(self):
        a = 12
        print(a)

    def __call__(self): #call method
        self.run()
```
```python
#example/src/file2.py

class printDone:
    def run(self):
        print("Done.")

    def __call__(self): #call method
        self.run()
```

To start pipely, type in cli:
```bash
python -m pipely from-pipeline test.yaml
```


## 1.2. Example w/ a shared dictionary

Let's create a [`testContext.yaml`](example/testContext.yaml) config file:

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
`depends_on` parameter sets the following order for pipely:

1. executes `a_first` and `a_second` in parallel
2. then executes `a_sum`, which sums up both a's in the previous steps
3. finally executes `a_sum_print`, which prints the final result previously calculated in `a_sum`

Let's look at executale classes to understand how values are transferred between them (check [example/src](/example/src) folder):

```python
#example/src/file1_shared.py

class firstA:
    def run(self):
        a = 32
        self.result = a

    def __call__(self, context): #include context
        self.run()
        context["a1"] = self.result #to save into shared dictionary

class secondA:
    def run(self):
        a = 12
        self.result = a

    def __call__(self, context): #include context
        self.run()
        context["a2"] = self.result #to save into shared dictionary
```
Now we can use previously saved values `a1` and `a2` in another class, as shown below: 

```python
#example/src/file2_shared.py

class aSum:
    def run(self, context): #include context
        a1 = context["a1"] #to extract from shared dictionary
        a2 = context["a2"] #to extract from shared dictionary
        self.result = a1 + a2

    def __call__(self, context): #include context
        self.run(context) #to run the function
        context["aSum"] = self.result #and save into shared dictionary
```

Then trigger the pipeline in cli with an optional second argument `--context-path`, which the path to a shared dictionary [example_context.json](example/example_context.json):

```bash
python -m pipely from-pipeline testContext.yaml --context-path example_context.json
```

# 2. Imperative way
Pipely can also trigger a specific class from a specific .py file.

```bash
python -m pipely from-class <path/to/file.py>:<TestClass>
```

Below is an example of a command that triggers a `printDone` class from [src/file4.py](example/src/file4.py) file.

```bash
python3 -m pipely from-class src/file4.py:printDone
```

If your class needs to operate on a shared dictionary, the command `from-class` could use an optional second argument `--context-path`. This argument awaits a path to a json representing the shared dictionary.

```bash
python -m pipely from-class src/file4.py:printShared --context-path example_context.json
```
