from io import StringIO
import sys
import traceback

class OutputInterceptor(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


def ListenOutput(code):
    with OutputInterceptor() as output:
        try:
            eval(code)
        except Exception as e:
            print(traceback.format_exc())
    return str(output)

while True:
    print('!: '+ListenOutput(input(': ')))