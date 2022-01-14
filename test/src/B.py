import time

class B:
    def run(self):
        for i in range(0, 4):
            time.sleep(2)
            print(f'2.py ... step {i}')

    def __call__(self):
        self.run()

# if __name__ == '__main__':
#     B()()