import sys
import argparse
import os
import re
import json


# frrouting: 
# python run_script.py -bc ../input/proc/bgpd.bc -erule ../input/config/Gen_frr_tree.json -info ../input/Text-info/frr

# iscdhcp:
# python run_script.py -bc ../input/proc/dhclient.bc -erule ../input/config/Gen_iscdhcp_tree.json -info ../input/Text-info/isc-dhcp


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


    
    # EBug_exec="../../RIBDetector-1126/tool/Release_build/bin/rfc"
    EBug_exec="./rfc"
    # RIB_exec="./Debug-build/bin/rfc"

    print("Step1: Rule-Related Code Identification")

    cmd1 = "python gen_impl_used_rule.py 1 ../input/config/Gen_"+evname+"_meta.json ../input/proc/"+evname+".json"
    os.system(cmd1)


    cmd2 = EBug_exec+" -IdentifyExt "+bc_path+" tmp_res/Impl_Gen_"+evname+"_meta.json "+evolrule+" ../input/config/Gen_"+evname+"_rule.json"
    print("cmd: " + cmd2)
    os.system(cmd2)

    print("Step2: Rule Violation Detection")
    cmd3 = EBug_exec+" -IdentifyOP "+bc_path+" ../output/result_of_identify/Impl_strGen_"+evname+"_meta_use.json" 
    print("cmd: " + cmd3)
    os.system(cmd3)





    # cmd1 ="cd ../input && python extract.py "+config_path
    # print("step 1: run Rule Extractor  ...")
    # print("Cmd: ",cmd1)
    # print(os.system(cmd1))
    # # print(os.system("pwd"))

    # cmd2 = RIB_exec+" --Identify "+bc_path+" "+meta_info_path
    # print("step 2: run Identifier  ...")
    # print("Cmd:", cmd2)
    # print(os.system(cmd2))
    # # print(bcname)

    # if os.path.exists(pkt_rule):
    #     cmd3 = RIB_exec+" --PktDetectz3 "+bc_path+" "+Identify_errule+" "+pkt_rule+" > ../output/inconsistency_bug/bug_report_"+bcname+"_"+raw_path.replace(".json",".txt")+" 2>&1"
    #     print("step 3: Pkt vailation detection ...")
    #     print("Cmd: ",cmd3)
    #     print(os.system(cmd3))

    
    # if os.path.exists(errrule_info_path):

    #     cmd4 = "./rfc --ErrDetect "+bc_path+" "+Identify_errule+" "+errrule_info_path+" > ../output/inconsistency_bug/bug_report_"+bcname+"_"+raw_path.replace(".json",".txt")+" 2>&1"
    #     print("step 4: Error Handling vailation detection ...")
    #     print("Cmd:", cmd4)
    #     print(os.system(cmd4))

    # if os.path.exists(fsm_rule):

    #     cmd5 = "./rfc --FSMDetect "+bc_path+" "+Identify_errule
    #     print("step5: State Machine vailation detection ...")
    #     print("Cmd:", cmd5)
   
    
    #     cmd6 ="python RFCextract/fsm_compare.py "+fsm_rule+ " "+fsm_prule+" >>  ../output/inconsistency_bug/bug_report_"+bcname+"_"+raw_path.replace(".json",".txt")+" 2>&1"
    #     print("Cmd:", cmd5)
    #     print("Cmd:", cmd6)
    #     print(os.system(cmd5))
    #     print(os.system(cmd6))
    
    




   