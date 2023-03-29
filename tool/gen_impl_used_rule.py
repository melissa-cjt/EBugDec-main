import os
import sys
import json
import time
import copy
import re
from collections import OrderedDict

def get_meta_json():

    with open(sys.argv[2], 'r') as f:
        meta = json.load( f)
    return meta
    pass


def get_impl_json():

    with open(sys.argv[3], 'r') as f:
        impl = json.load(f)
    

    return impl
    pass
def isProcess(field):
    if "Error" in field or "subcodes" in field:
        return True
    if "Flags" in field:
        return True
    return False

def generate_impl_used_rule(meta, impl):

    field_values = meta["Value_list"]

    gen_impl = {}

    val_count = 0

    

    for field,  info in field_values.items():

        if isProcess(field):
            continue

        gen_impl[field] = {}
        vals = []
        for k , v in info.items():
            vals.append(v)
        gen_impl[field]["Value"]=vals


        if field in impl.keys():
            gen_impl[field]["PreInfo"]=impl[field]["PreInfo"]
        else:
            gen_impl[field]["PreInfo"]=[]

    if "SPECIAL" in impl.keys():
        for k, v in impl["SPECIAL"].items():
            gen_impl[k]["Value"] += v

    if "Decrpyted&Reserved" in impl.keys():
        for k, v in impl["Decrpyted&Reserved"].items():
            for dv in v:
                gen_impl[k]["Value"].remove(dv)
    
    for k , v in gen_impl.items():
        print(k, len(v["Value"]))
        val_count +=len(v["Value"])


    if "FUNC_PKT" in impl.keys():
        print("ok")
        
        gen_impl["FUNC_PKT"] = impl["FUNC_PKT"]
        # print(gen_impl["FUNC_PKT"])
    if "Entry_Cand" in impl.keys():
        gen_impl["Entry_Cand"] = impl["Entry_Cand"]

    if "Struct_list" in meta.keys():
        gen_impl["Struct_list"] = meta["Struct_list"]

    # ext_res/proc_rule/Impl_
    with open("tmp_res/Impl_"+os.path.split(sys.argv[2])[1], 'w') as f:
        json.dump(gen_impl, f, indent=2)
    pass

    print("Val num: ", val_count)

def isinExt(valist ,field):

    for ext , info in valist.items():
        if field in info.keys():
            ty = info[field]
            return True, ext, ty
    return False, "",""

def generate_impl_used_struct_rule(meta, impl):

    field_struct = meta["Struct_list"]
    field_values = meta["Value_list"]
    field_fixval = meta["FixVal_list"]
    str_count = 0

    gen_impl_struct = {"OTHER":{}}

    for field , value in field_struct.items():
        
        flag , ext, ty = isinExt(field_values, field)
        if flag:
            if ext in gen_impl_struct.keys():
                gen_impl_struct[ext][field] = {"Type":ty, "Len": value[0], "Indirect":"", "arg":255}
                str_count +=1
            else:
                
                gen_impl_struct[ext] = {"Impl_Loc":[],"Array":0, field:{"Type":ty, "Len": value[0], "Indirect":"", "arg":255}}
                str_count +=1
        else:
            
            gen_impl_struct["OTHER"][field] = {"Type":0, "Len":  value[0], "Indirect":"", "arg":255}


    for field, value in field_fixval.items():
        flag , ext, ty = isinExt(field_values, field)
        if flag:
            if ext in gen_impl_struct.keys():
                gen_impl_struct[ext][field] = {"Type":ty, "Len": value, "Indirect":"", "arg":255}
                str_count +=1
            else:
                gen_impl_struct[ext] = {"Impl_Loc":[],"Array":0, field:{"Type":ty, "Len": value, "Indirect":"", "arg":255}}
                str_count +=1
        else:
            
            gen_impl_struct["OTHER"][field] = {"Type":0, "Len": value, "Indirect":""} 

       
    
    if "FUNC_PKT" in impl.keys():
        gen_impl_struct["FUNC_PKT"] = impl["FUNC_PKT"]
    # ext_res/proc_rule/Impl_str
    with open("tmp_res/Impl_str"+os.path.split(sys.argv[2])[1], 'w') as f:
        json.dump(gen_impl_struct, f, indent=2)
    
    print("Struct/Fixed num : ", str_count)

def GetVersionRelease(RL, mark):

    ver=[]
    Release={}
    
    for line in RL:

        if line.strip() == mark:
            print(ver[0])
            Release[ver[0]]=copy.deepcopy(ver[1:])
            ver=[]
        else:
            ver.append(line.strip())
            # print(line)

    # print(Release)
    return Release
def match_RFCX(sentence, RInfo):

    if re.findall(r'rfc(\d+)',sentence.lower()):
        res = re.findall(r'rfc(\d+)',sentence.lower())
        if "RFC"+res[0] in RInfo:
            return True, "RFC"+res[0]
    elif re.findall(r'rfc (\d+)', sentence.lower()):
        res = re.findall(r'rfc (\d+)',sentence.lower())
        if "RFC"+res[0] in RInfo:
            return True, "RFC"+res[0]
    
    return False, ""
    
def match_RFCTitle(sentence, RInfo):

    for rfcx, title in RInfo.items():
        if title.lower() in sentence.lower():
            
            return True, rfcx
    return False, ""



def getRFCtoVersion(RV, RInfo):

    R2V = {}
    count = 0
    rcount = 0
    RFClist = []
    # RFCX = RInfo.keys()

    for ver, notes in RV.items():
        R2V[ver]=[]
        for note in notes:
            if "rfc" in note.lower():
                flag, r =  match_RFCX(note, RInfo)
                if flag:
                    R2V[ver].append(r)
            elif "support" in note.lower() or "implement" in note.lower() or "add" in note.lower():
                flag, r = match_RFCTitle(note, RInfo)
                if flag:
                    
                    R2V[ver].append(r)
                # else:
                #     R2V[ver].append(note)
            else:
                flag, r = match_RFCTitle(note, RInfo)
                if flag:
                    R2V[ver].append(r)
        R2V[ver] = list(set(R2V[ver]))
        RFClist+=R2V[ver]
        count += len(R2V[ver])
    print(R2V, count)
    print(RFClist)
    return R2V

def prepocess_release():
    Rnote = sys.argv[2]
    print(os.path.split(os.path.splitext(Rnote)[0])[1])
    f = open(Rnote,'r')
    RL = f.readlines()
    mark = "--------"
    # mark = " -- "
    f.close()

    RInfo = sys.argv[3]
    f = open(RInfo, 'r')
    RI = f.read()
    RI = eval(RI)
    f.close()
    

    RV = GetVersionRelease(RL, mark)
    R2V = getRFCtoVersion(RV,RI)

    with open("ext_res/Impl/Gen_"+os.path.split(os.path.splitext(Rnote)[0])[1]+"_ImplVer.json",'w') as f:
        json.dump(R2V, f, indent=2)
    

    # RFCValue = list(set([]))
    # print(RFCValue)

def getPktRoot():

    RInfo = sys.argv[2]

    with open(RInfo, 'r') as reader:
        RI = json.load(reader, object_pairs_hook=OrderedDict)


    root = {}

    for k, v in RI.items():
        print(k)
        pktstr = v["struct"]
        root[k] = OrderedDict()
        for fi, val in pktstr.items():
            root[k][fi]=val["bitwidth"]["len"]

    print(root)

    




    


if __name__ == '__main__':
    start = time.time()

    Step = sys.argv[1]

    if Step == "1":

        meta_json = get_meta_json()

        impl_json = get_impl_json()

        generate_impl_used_rule(meta_json, impl_json)

        generate_impl_used_struct_rule(meta_json, impl_json)

    elif Step == "2":
        prepocess_release()
    elif Step == "3":
        getPktRoot()



    end = time.time()
    print("Total Time: ",end-start)