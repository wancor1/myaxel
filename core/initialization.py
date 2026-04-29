import sys,os
import data.const as const
import data.store as store

EXT=const.EXT

class Initialization:
    def __init__(self) -> None:
        self.arg=sys.argv[1:]
        if len(self.arg)==0:
            print("require filename or filepath.")
            print('usage: main.py <path|filename> [-D|--debug]')
            sys.exit(1)
        self.input_path,self.cwd=self.arg[0],os.getcwd()

    def main(self) -> None:
        if os.path.isabs(self.input_path): filepath=self.input_path
        else: filepath=os.path.join(self.cwd, self.input_path)
        filepath,dirpath,filename=os.path.abspath(filepath),os.path.dirname(filepath),os.path.basename(filepath)
        fn=self.arg[0].split('.')
        if fn[-1]!="myx":
            filename=filename + EXT
            filepath=os.path.abspath(os.path.join(dirpath, filename))
        if not os.path.isfile(filepath):
            print(f"file not found: {filepath}")
            print('usage: main.py <path|filename> [-D|--debug]')
            sys.exit(2)
        const.FILEPATH,const.DIRPATH,const.FILENAME=filepath,dirpath,filename
        if '--debug' in self.arg or '-D' in self.arg: store.debug=True

        if store.debug:
            print("arg >", self.arg)
            print("path>", filepath)
            print("dir >", dirpath )
            print("file>", filename)
