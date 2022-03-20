class aSumPrint:
    def run(self):
         a_sum = context["aSum"] #extracting from shared dictionary
         print(a_sum)

    def __call__(self, context):
        self.run()
