import sys
import argparse
import os
import re
import json


# frrouting: 
# python run_script.py -bc ../input/proc/bgpd.bc -erule ../input/config/Gen_frr_tree.json -info ../input/Text-info/frr

#openbgpd:
# python run_script.py -bc  ../input/proc/openbgpd.bc -erule ../input/config/Gen_openbgpd_tree.json -info ../input/Text-info/openbgpd


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="your script description") 
    parser.add_argument('--bitcode', '-bc', type=str, required = True, help='.bc file of the implementation')
    parser.add_argument('--evolrule', '-erule', type=str,  required = True, help='evolutionary rules generated based on the implementation RFC supported')
    parser.add_argument('--information','-info', type=str, required=True, help='Release notes and Source code of the implementation')

    # parser.add_argument('--unERRDetect', '-unerr')

    args = parser.parse_args()

    if args.bitcode:
        bc_path = args.bitcode
        (path, filename) = os.path.split(bc_path)
        # print(filename)
        bcname = filename.replace(".bc", "")
        # pos = bc_path.rfind("/")
        # bcname = bc_path[pos+1:len(bc_path)-3]
        print(bc_path, bcname)

    if args.evolrule:
        evolrule = args.evolrule
        (path, filename) = os.path.split(evolrule)

        evname = re.findall(r'Gen_(.*)_tree', filename)[0]
        print(evname)

    if args.information:
        info_path = args.information

    

    EBug_exec="./rfc"
    

    print("Step1: Rule-Related Code Identification")

    cmd1 = "python gen_impl_used_rule.py 1 ../input/config/Gen_"+evname+"_meta.json ../input/proc/"+evname+".json > /dev/null 2>&1"
    os.system(cmd1)


    cmd2 = EBug_exec+" -IdentifyExt "+bc_path+" tmp_res/Impl_Gen_"+evname+"_meta.json "+evolrule+" ../input/config/Gen_"+evname+"_rule.json > /dev/null 2>&1"
    print("cmd: " + cmd2)
    os.system(cmd2)

    print("Step2: Rule Violation Detection")
    cmd3 = EBug_exec+" -IdentifyOP "+bc_path+" ../output/result_of_identify/Impl_strGen_"+evname+"_meta_use.json "+ info_path+" > ../output/evolutionary_bug/bug_report_"+bcname+".txt 2>&1"
    # cmd3 = EBug_exec+" -IdentifyOP "+bc_path+" ../output/result_of_identify/Impl_strGen_"+evname+"_meta_use.json "
    print("cmd: " + cmd3)
    os.system(cmd3)

    print("Finished ")
