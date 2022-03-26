class printDone:
    def run(self):
        print("Done.")

    def __call__(self):
        self.run()

class printShared:
    def run(self, context): #include context
        result = context["example_value"] #to extract from shared dictionary
        print(result)

    def __call__(self, context): #include context
        self.run(context) #to run the function