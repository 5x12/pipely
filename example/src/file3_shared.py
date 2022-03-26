class aSumPrint:
    def run(self, context): #include context
         a_sum = context["aSum"] #to extract from shared dictionary
         print(f'a_sum = {a_sum}')

    def __call__(self, context):
        self.run(context) #to run the function
