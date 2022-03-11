import time

class B:
    def run(self):
        result = []
        for i in range(0, 4):
            time.sleep(2)
            result.append(i)
            print(f'B1.py ... step {i}')
        self.result = sum(result)

    def __call__(self, context):
        self.run()
        context[self.__class__.__name__] = self.result
