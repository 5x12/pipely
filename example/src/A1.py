import time

class A:
    def run(self):
        result = []
        for i in range(0, 5):
            time.sleep(5)
            result.append(i)
            print(f'A1.py ... step {i}')
        self.result = result

    def __call__(self, context):
        self.run()
        context[self.__class__.__name__] = self.result
