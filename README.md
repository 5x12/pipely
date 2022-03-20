To install the library:
```bash
pip install pipely
``` 

# 1. About

The library `pipely` can execute any class or any sequence of classes in any order.

# 2. How it works

## 2.1. Declarative way

To build a pipeline with classes to execute, you have to create a config `.yml` file in a *root* directory in the following form:

```text
steps:
    [step_name_1]:
        exec: [relative path to a file]:[class to execute]
    [step_name_2]:
        exec: [relative path to a file]:[class to execute]
    [step_name_3]:
        exec: [relative path to a file]:[class to execute]
```
Let's create a config file with the name `collect.yml`:

```text
steps:
    preProcessing:
        exec: src/calculation.py:Calculate
    kMeans:
        exec: src/models.py:Kmeans
    hyperTuning:
        exec: src/tuning.py:GridSearch
        depends_on:
            - preProcessing
            - kMeans
```
Pipely will be able to automatically detect which steps are independent and could be done in parallel. In this case, it will execute steps `preProcessing` and `kMeans` in parallel, and right after they are finished, start executing `hyperTuning`.

In order for the pipely to work,
- the names of your [steps] in `collect.yml` should be unique;
- the executable classes should have a ``__call__`` method. For instance, if we open `src/calculation.py` and look at `Calculate` class that we trigger, we see __call__ method in the end. It's possible to add an argument to ``__call__``. The said argument is used by pipely to share a dictionary between classes, thus permitting simple value transmission from class to class.

```python
#src/calculation.py

class Calculate(object):
	def sum(self):
		a=2
		b=4
		self.c=a+b

	def divide(self):
		f=4
		self.d = self.c/f

    def show_result(self):
            print(self.d)

	def __call__(self): # or __call__(self, context): ### if some value exchange is needed
		self.sum()
		self.divide()
        # context['calcul_result'] = self.d ### to use the result in an other class
        self.show_result()
```

After creating a configuration .yml file in your root directory, use the following command to trigger the pipeline in terminal:

```bash
python -m pipely from-pipeline collect.yml
```

## 2.2. Imperative way
Pipely can also trigger a specific class from a specific .py file.

```bash
python -m pipely from-class path/to/file.py:TestClass
```

Below is an example of command that triggers a `Calculate` class from `src/calculation.py` file.

```bash
python -m pipely from-class src/calculation.py:Calculate
```

Again, `Calculate` class should have a `__call__` method that executes desired class functions.

If your class need to operate on a a shared dictionary, the command from-class could use an optional second argument.
This argument await a path to a json representing the shared dictionary.

```bash
python -m pipely from-class src/calculation.py:Calculate src/context.json
```
