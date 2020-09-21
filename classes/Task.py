class Task:
    def __init__(self, max_number):
        self.max_number = max_number
        self.interrupt_requested = False

    def __call__(self):
        print("Started:", datetime.datetime.now(), self.max_number)
        last_number = 0
        for i in xrange(1, self.max_number + 1):
            if self.interrupt_requested:
                print("Interrupted at", i)
                break
            last_number = i * i
        print("Reached the end")
        return last_number

    def interrupt(self):
        self.interrupt_requested = True
