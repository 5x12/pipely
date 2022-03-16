import time

class C:
    def run(self):
        for i in range(0, 10):
            time.sleep(5)
            print(f'3.py ... step {i}')

    def __call__(self):
        self.run()
