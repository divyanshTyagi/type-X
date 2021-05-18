import os
import regex as re
root = ".\e-maxx-eng-master\src"

print(os.listdir(root))
file_number = 0
for folder in os.listdir(root):
    path = os.path.join(root,folder)
    for algo in os.listdir(path):
        file_path = os.path.join(path,algo)
        file = open(file_path,"r",encoding = "UTF-8").read()
        codes = re.findall('```[^`]*```',file)

        for code in codes:
            code = re.sub('```.*','',code)
            code = re.sub('\.\.\..*\.\.\.','',code)
            print(len(code))
            # print(code)
            file_out_path = ".\codes\\" + str(file_number)  + ".txt"
            file_out = open(file_out_path,'w')
            file_out.write(code)
            file_number+=1
file_out.close()
    # print(path)
