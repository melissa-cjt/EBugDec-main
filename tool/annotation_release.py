import sys
import os
import re
import time
import json

def get_filelist(dir, Filelist):
    
    newDir = dir
    # print(newDir)
    if os.path.isfile(dir):
        filename, ftype = os.path.splitext(dir)
        if ftype != ".h" and ftype != ".c":
            return Filelist
        Filelist.append(dir)
    elif os.path.isdir(dir):
        # print("isdir")
        for f in os.listdir(dir):
            # print(f)
            newDir = os.path.join(dir, f)
            get_filelist(newDir, Filelist)

    return Filelist

def get_and_mark_define_annotation(Flist):


    df_annos={}
    for F in Flist:
        filename, ftype = os.path.splitext(F)
        if ftype != ".h":
            continue
        # print(F)
        if not os.path.exists(F):
            continue
        f = open(F, "r")
        # print(f)
        lines = f.readlines()
        f.close() 
        
        for l in lines:
            if l.startswith("#define"):
                if re.findall(r'\#define (.*)  (.*)\/\* (.*) \*\/', l.strip()):
                    an = re.findall(r'\#define (.*)  (.*)\/\* (.*) \*\/', l.strip())
                    # print(l)
                    df_annos[an[0][0].strip()] = {"an":an[0][2],"lines":[]}
    # print(df_annos)


    for F in Flist:
        if not os.path.exists(F):
            continue
        f = open(F,"r")
        lines = f.readlines()
        f.close()

        for l in lines:
            for df in df_annos.keys():
                if df in l:
                    df_annos[df]["lines"].append(F+" "+str(lines.index(l)+1))


    # print(df_annos)
    with open("ext_res/Impl/def_"+os.path.split(sys.argv[2])[1], 'w') as f:
        json.dump(df_annos, f, indent = 2)

def get_annotation(FileName, Line, Flist):
    dir = sys.argv[1]

    FileName = dir + FileName

def get_above_anno(Func_SLoc, Flist):

    dir = sys.argv[1]

    # print(dir)
    
    File, L = Func_SLoc.split(" ")
    File = dir+File
    # print(File)
    # if File not in Flist:
    #     return False
    if not os.path.exists(File):
        return False, ""

    f = open(File, "r")
    lines = f.readlines()
    f.close()

    startidex = int(L)-1

    # startline = lines[int(L)-1]
    # print(startidex)
    anend = startidex
    anstart = startidex

    if "*/" in lines[startidex-1]:
        anend = startidex-1 
        for i in range(anend, 0 , -1):
            if "/*" in lines[i]:
                anstart = i
                break 

    if anend == startidex:
        return False, ""
    if anstart == anend:
        prog_an = getsingleAN(lines[anstart])
        # print(prog_an)
        return True, prog_an
    else:
        prog_an = getmultiAN(lines[anstart: anend+1])
        # print(prog_an)
        return True, prog_an

def get_inside_anno(FLoc):

    StartF = FLoc["Func_SLoc"]
    EndF = FLoc["Func_ELoc"]
    if EndF == "UNKNOWN":
        return False, []

    dir = sys.argv[1]
    
    File, L = StartF.split(" ")
    File, eL = EndF.split(" ")
    File = dir+File

    if not os.path.exists(File):
        return False, []

    f = open(File, "r")
    lines = f.readlines()
    f.close()

    func_line = lines[int(L) : int(eL)]

    an_list = []
    tmpan = []
    flag = False

    for l in func_line:
        if re.findall(r'\/\* (.*) \*\/', l.strip()):
            an = re.findall(r'\/\* (.*) \*\/', l.strip())
            an_list.append(an[0])
            continue


        elif l.strip()=="/*" or l.strip() == "/**":
            flag = True
        elif re.findall(r'\/\* (.*)', l.strip()):
            flag = True
            tmpan.append(l.strip().replace("/*",""))
        elif l.strip() == "*/":
            flag = False
            an_list.append(" ".join(tmpan))
            tmpan=[]
        elif re.findall(r'(.*)\*\/', l.strip()):
            # print(tmpan)
            flag = False
            tmpan.append(l.strip().replace("*/", ""))
            an_list.append(" ".join(tmpan))
            tmpan=[]

        elif flag:
            # l = l.replace("/*","")
            l = l.replace("* ", "")
            
            tmpan.append(l.strip())
    
    # print(an_list)

    if len(an_list) != 0:
        return True , an_list
    else:
        return False, an_list

    

        
def getsingleAN(line):
    pro_an =  re.findall(r'\/\* (.*) \*\/', line.strip())
    return pro_an[0]

def getmultiAN(lines):

    tmpan = []
    
    for l in lines:
        # print(l)
        if l.strip() == "/*" or l.strip() == "/**":
            continue
        elif re.findall(r'\/\* (.*)', l.strip()):
            
            tmpan.append(l.strip().replace("/*", ""))
        elif l.strip() == "*/":
            # print(tmpan)
            return " ".join(tmpan)
        elif re.findall(r'(.*)\*\/', l.strip()):
            # print(tmpan)
            tmpan.append(l.strip().replace("*/", ""))
            return " ".join(tmpan)
        else:
            tmpan.append(l.strip().replace("*", ""))
            



def ismatch(prog_an, CName):

    meta = sys.argv[3]
    
    with open(meta, "r") as f:
        keyword = json.load(f)
    
    # print(prog_an)
    if CName.lower() in prog_an.lower():
        return True
    
    if CName in keyword["Struct_list"]:
        keyL = keyword["Struct_list"][CName][2]
        for k in keyL:
            if k.lower() in prog_an.lower():
                return True
    return False

def searchanno(empty_CN, Flist):
    annos={}
    print(Flist)
    
    for F in Flist:
        # print(F)
        filename, ftype = os.path.splitext(F)
        if ftype != ".c":
            continue
        
        f = open(F, "r")
        # print(f)
        lines = f.readlines()
        f.close()
        tmpan =[]
        flag = False
        for l in lines:
            if re.findall(r'\/\* (.*) \*\/', l.strip()):
                an = re.findall(r'\/\* (.*) \*\/', l.strip())
                annos[an[0]]= F+" "+str(lines.index(l))
                continue

            elif l.strip()=="/*" or l.strip() == "/**":

                flag = True
            elif re.findall(r'\/\* (.*)', l.strip()):
                flag = True
                tmpan.append(l.strip().replace("/*",""))

            elif l.strip() == "*/":
                flag = False
                annos[" ".join(tmpan)]=F+" "+str(lines.index(l))
                tmpan=[]
            elif re.findall(r'(.*)\*\/', l.strip()):
                # print(tmpan)
                flag = False
                tmpan.append(l.strip().replace("*/", ""))
                annos[" ".join(tmpan)]=F+" "+str(lines.index(l))
                # an_list.append(" ".join(tmpan))
                tmpan=[]

            elif flag:
                # l = l.replace("/*","")
                l = l.replace("* ", "")
                
                tmpan.append(l.strip())
    # annos = [an for an in annos if not an.startswith("Copyright (c)")]
    annos ={k:v for k, v in annos.items() if not k.startswith("$OpenBSD: ")}
    annos ={k:v for k, v in annos.items() if not k.startswith("Copyright (c) ")}
    annos ={k:v for k, v in annos.items() if not k.startswith("DOC:")}
    # print(len(annos))
    annos ={k:v for k ,v in annos.items() if "Copyright " not in k}
    annos ={k:v for k ,v in annos.items() if "+MS = Protocol" not in k}


    with open("ext_res/Impl/Full_"+os.path.split(sys.argv[2])[1], 'w') as f:
        json.dump(annos, f, indent = 2)
    CN_Cand ={}
    for key in annos.keys():
        for ety in empty_CN:
            if ety not in CN_Cand.keys():
                CN_Cand[ety] =[]
            if ismatch(key, ety):
                CN_Cand[ety].append((key, annos[key]))
    
    # print(len(empty_CN))
    for k, v in CN_Cand.items():
        print(k, len(v))
    # print(CN_Cand)
    with open("ext_res/Impl/search_find_"+os.path.split(sys.argv[2])[1], 'w') as f:
        json.dump(CN_Cand, f, indent = 2)
    
def checkannotation(Flist, Cand_IdList):
    empty_CN=[]
    for CName,  CFuLoc in Cand_IdList.items():
        # if CName != "Attribute Type Code":
        #     continue
        print("---------")
        print(CName)
        if len(CFuLoc) == 1:
            print("Has only one Candidate, we will make sure future. ")
            continue
        
        print(len(CFuLoc))
        if len(CFuLoc) == 0:
            empty_CN.append(CName)

        cand_loc = []
        for FL in CFuLoc:
            print("Get Above ...", FL["Func_SLoc"])
            # print FL["Func_Sloc"]
            cand_an_list = []
            gtab, prog_an = get_above_anno(FL["Func_SLoc"], Flist)
            if gtab:
                # print(prog_an)
                # cand_an_list.append(prog_an)
                if ismatch(prog_an, CName):
                    print("Find!!! ", prog_an)
                    cand_loc.append(FL["Func_SLoc"])
            
            
            # print(FL)
            gtin, prog_an = get_inside_anno(FL)
            if gtin:
                print(prog_an)
                for pa in prog_an:
                    if ismatch(pa, CName):
                        print("Find!!!!", pa)
                

                

            # print("Get Func inside ...")

            # FL.replace("..", "")
            # Filename, Line = FL.split(" ")
    print(len(empty_CN))
    searchanno(empty_CN, Flist)

def getusefulfile(Flist):
    # print(Flist)

    Flist = [f for f in Flist if f.startswith(sys.argv[4])]
    return Flist

if __name__ == '__main__':
    start = time.time()

    Flist = get_filelist(sys.argv[1], [])
    Flist = getusefulfile(Flist)
    
    get_and_mark_define_annotation(Flist)

    with open(sys.argv[2], 'r') as reader:

        Cand_IdList = json.load(reader)

    
    checkannotation(Flist, Cand_IdList)


    end = time.time()
    print("Total Time: ",end-start)