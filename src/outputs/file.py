class File:
    id = 'file'
    def __init__(self):
        self.fh = self.openFile(path='./var/hr.txt', keepHistory=False)

    async def execute(self, data):
        self.fh.write(f'{data['hr']}\n')
        self.fh.flush()

    def openFile(self, path='./var/hr.txt', keepHistory=True):
        mode = 'a+' if keepHistory else 'w+' 
        return open(path, mode)