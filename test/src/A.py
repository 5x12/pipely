import time

class A:
    def run(self):
        for i in range(0, 5):
            time.sleep(5)
            print(f'1.py ... step {i}')

    def __call__(self):
        self.run()
