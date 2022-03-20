class printDone:
    def run(self):
        print("Done.")

    def __call__(self):
        self.run()