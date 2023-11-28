import os
import subprocess

dirname = r"C:\Users\lasse\Documents\OhPeOhjaus\Demo1t2" #Folder that has all the named demo return folders
resultDir = r"C:\Users\lasse\Documents\OhPeOhjaus\Demo1t2result.txt" #Text file to write results
targetfile = []
expectedResult = "11" #Tavoiteltu arvo/nimi joka pitäisi näkyä ohjelman tulostuksessa





def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        if not dirname.find(".git"):
            subfolders.extend(fast_scandir(dirname))
    return subfolders


#workDir = r"C:\Users\lasse\Documents\OhPeOhjaus\Demo1t1"

subfolder = fast_scandir(dirname)

for i in range(len(subfolder)):
    obj = os.scandir(subfolder[i])
    
    for entry in obj:
        if entry.is_file():
            if '.py' in entry.name:
                targetfile.append(entry.path)



    
with open(resultDir, "w", encoding="utf-8") as result_file:
    for i in range(len(targetfile)):
        try:
            file = subprocess.Popen(['python', targetfile[i]],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
            out, err = file.communicate(b'+10\n*10\n-10\n/8\n\n') #Desired inputs should be separated with \n
            file.stdin.close
            if not err:
                outString = out.decode(encoding="utf-8", errors="replace")
                if expectedResult in outString:
                    words= str(subfolder[i]).split("\\")
                    result_file.write(f"{words[-1]}: Got expected result {outString}\n")
                else:
                    words= str(subfolder[i]).split("\\")
                    print(words[-1])
                    print(outString)
                    result_file.write(f"{words[-1]}: Unexpected result: {outString}\n")
            else:
                words= str(subfolder[i]).split("\\")
                result_file.write(f"{words[-1]}: Error in code {err}\n")
            i += 1
        except Exception as e:
            print(f"Error in {targetfile[i]}")
            print(e)
            i += 1