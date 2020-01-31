
#!/usr/bin/ env python 
#coding=UTF-8
import os
import sys
import random
import datetime
import re
import shutil





BG_SET = ['background.jpg','bg1.jpg','bg2.jpg']
NOTES_PATH = "D:/Documents/Notes/"
PAGE_PATH = "D:/Documents/Coding/blog/source/_posts/"
IMAGE_PATH = "D:/Documents/Coding/blog/source/images/"


def alter(file):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            pics = re.findall("\((.*\.assets.*)\)",line)
            for pic in pics:
                line = line.replace(pic, "/images/"+pic)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)


def loadFile(filepath,filename):
    if not os.path.exists(filepath):
        return 
    with open(PAGE_PATH + filename, 'w', encoding='UTF-8') as outFile:
        
        f = filename.split('.')[0]
        date = datetime.datetime.now()
        outFile.write("---\n")
        outFile.write("title: " + f + '\n')
        outFile.write("comments: true\n")
        outFile.write("thumbnail: /gallery/" + random.choice(BG_SET) + '\n')
        outFile.write("date: " + datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S") + '\n')
        outFile.write("toc: true\n")
        #outFile.write("mathjax: true\n")
        line = input("Enable mathjax or not(true/false): ")
        outFile.write("mathjax: " +  ("true" if line.strip()[1] == 't' else "false")  + '\n')
        line = input("Enter categories(splited by space):")
        if line.strip() != "":
            categories = line.split(' ')
            outFile.write("categories:\n")
            for category in categories:
                if category == "":
                    continue
                outFile.write("\t- " + category + '\n')
        
        
        
        line = input("Enter tags(splited by space):")
        
        if line.strip() != "":
            tags = line.split(' ')
            outFile.write("tags:\n")
            for tag in tags:
                if tag == "":
                    continue
                outFile.write("\t- " + tag + '\n')

        outFile.write("---\n")
        with open(filepath, 'r', encoding='UTF-8') as inFile:
            content = inFile.readlines()
            outFile.writelines(content[:])
         
    alter(PAGE_PATH + filename)
    


def moveImages(source, target):

    if not os.path.exists(target):
        os.makedirs(target)

    if os.path.exists(source):
        # root 所指的是当前正在遍历的这个文件夹的本身的地址
        # dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
        # files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
        for root, dirs, files in os.walk(source):
            for file in files:
                src_file = os.path.join(root, file)
                shutil.copy(src_file, target)
                print(src_file)
    

def File():
    print("File Mode")
    relpath = input("Please enter the relative path:")
    if relpath[-1] != '/':
        relpath = relpath + '/'
    
    while True:
        cmd = input("Enter the command:")
        if cmd == "reset":
            relpath = input("Please enter the relative path:")
        elif cmd == "exit":
            return
        elif cmd == "update":
            os.system("d: && cd D:/Documents/Coding/blog && dir && hexo d -g")
        else:
            title = cmd.split('.')[0]
            moveImages(NOTES_PATH+relpath+title+".assets",IMAGE_PATH+title+".assets")
            loadFile(NOTES_PATH+relpath+cmd, cmd)
            
            


if __name__ == "__main__":
    

    if len(sys.argv) == 1 or sys.argv[1] == "file":  
        File()

    elif sys.argv[1] == "directory":
        print("Directory Mode")
