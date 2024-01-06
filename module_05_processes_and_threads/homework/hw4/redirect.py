"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""
import sys
import traceback
from types import TracebackType
from typing import Type, Literal, IO


class Redirect:
    def __init__(self, stdout: IO = None, stderr: IO = None) -> None:
        self.stdout = stdout
        self.stderr = stderr
        # self.stdout_origin = sys.stdout
        # self.stderr_origin = sys.stderr


    def __enter__(self):
        if self.stdout is not None:
            sys.stdout = self.stdout
        if self.stderr is not None:
            sys.stderr = self.stderr

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        if exc_type:
            sys.stderr.write(traceback.format_exc())
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        if self.stdout is not None:
            self.stdout.close()
        if self.stderr is not None:
            self.stderr.close()
        return True


# print('Hello stdout')
#
# stdout_file = open('stdout.txt', 'w')
# stderr_file = open('stderr.txt', 'w')
#
# with Redirect(stdout=stdout_file, stderr=stderr_file):
#     print('Hello stdout.txt')
#     raise Exception('Hello stderr.txt')
#
# print('Hello stdout again')
# raise Exception('Hello stderr')