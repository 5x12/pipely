class aSum:
    def run(self, context): #include context
        a1 = context["a1"] #to extract from shared dictionary
        a2 = context["a2"] #to extract from shared dictionary
        self.result = a1 + a2

    def __call__(self, context): #include context
        self.run(context) #to run the function
        context["aSum"] = self.result #and save into shared dictionary