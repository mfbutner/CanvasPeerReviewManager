class Task:
    def do(self, stack):
        pass


class AddTask(Task):
    def __init__(self, what_to_do):
        self.what_to_do = what_to_do
        pass

    def do(self, stack):
        stack.append(self.what_to_do)


class BackTask(Task):
    def __init__(self):
        pass

    def do(self, stack):
        stack.pop()


class QuitTask(Task):
    def __init__(self):
        pass

    def do(self, stack):
        stack.clear()
