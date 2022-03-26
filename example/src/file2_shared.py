class aSum:
    def run(self, context):
        a1 = context["a1"] #extracting from shared dictionary
        a2 = context["a2"] #extracting from shared dictionary
        self.result = a1 + a2

    def __call__(self, context):
        self.run(context)
        context["aSum"] = self.result #saving to shared dictionary