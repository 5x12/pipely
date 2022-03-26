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
