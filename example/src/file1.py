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
