class Stdout:
    id = 'stdout'
    async def execute(self, data):
        print('[{}] ❤️ {}'.format(data['date'], data['hr']))