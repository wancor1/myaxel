import sys,os
import data.const as const
import data.store as store

EXT=const.EXT

class loader:
    def __init__(self) -> None:
        if len(sys.argv) < 2:
            print("require filename or filepath.")
            sys.exit(1)
        self.input_path,self.cwd=sys.argv[1],os.getcwd()

    def main(self):
        if os.path.isabs(self.input_path): filepath=self.input_path
        else: filepath=os.path.join(self.cwd, self.input_path)

        filepath,dirpath,filename=os.path.abspath(filepath),os.path.dirname(filepath),os.path.basename(filepath)
        name,ext=os.path.splitext(filename)

        if ext=="":
            filename=name + EXT
            filepath=os.path.abspath(os.path.join(dirpath, filename))
        
        if not os.path.isfile(filepath):
            print(f"file not found: {filepath}")
            sys.exit(2)

        const.FILEPATH,const.DIRPATH,const.FILENAME=filepath,dirpath,filename

        if store.debug:
            print("path>", filepath)
            print("dir >", dirpath )
            print("file>", filename)
