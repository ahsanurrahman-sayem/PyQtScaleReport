def openFile(fp):
        #Open files using this method
    if platform.system() == "Windows" or platform.system == "nt":
        os.startfile(fp)
    elif platform.system() == "Darwin":
        subprocess.run(["open", fp])
    else:
        subprocess.run(["xdg-open", fp])
