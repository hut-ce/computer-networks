from multiprocessing import Process
from so1 import so1_program
from so2 import so2_program
from so3 import so3_program


if __name__ == '__main__':
    p1 = Process(target=so1_program)
    p2 = Process(target=so2_program)
    p3 = Process(target=so3_program)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
