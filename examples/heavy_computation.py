from pyhooks import precall_register, postcall_register, Hook
import time


class HeavyComputation(object):

    @precall_register('heavy_computation')
    def begin_computation(self, *args, **kwargs):
        print("The ongoing operation could take some time to complete")

    @postcall_register('heavy_computation')
    def end_computation(self, *args, **kwargs):
        print("The running operation has ended")


class LifeQuestion(HeavyComputation):

    @Hook
    def heavy_computation(self):
        time.sleep(2)
        return 42


class Bruteforcer(HeavyComputation):

    @Hook
    def heavy_computation(self):
        time.sleep(1)
        return 'aldfjqorqlkjt'


computer = LifeQuestion()
print(computer.heavy_computation())
computer = Bruteforcer()
print(computer.heavy_computation())
