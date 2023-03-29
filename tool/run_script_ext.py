import sys
import argparse
import os
import re
import json

# extract rule from the tree 
cmd1 = python RFCextract/extract_extended_rule.py ../input/ext-config/bgp_packet.json ../input/config/rfc_config_bgp.json
cmd1 = python RFCextract/extract_extended_rule.py ../input/ext-config/dhcp_packet.json ../input/config/rfc_config_dhcp.json

cmd1 = python RFCextract/extract_extended_rule.py ../input/ext-config/dhcp_packet_v1.json ../input/config/rfc_config_dhcp_v1.json

cmd1 = python RFCextract/extract_extended_rule.py ../input/ext-config/ntp_packet.json ../input/config/rfc_config_dhcp_v1.json

# generate impl used rule 

cmd2 = python ext_res/gen_impl_used_rule.py 1 ext_res/meta/Gen_frr_meta.json  ext_res/proc_info/frr.json  

cmd2-1 = python ext_res/gen_impl_used_rule.py  2 ../input/ext-release/frrouting.txt ext_res/tree/Gen_frr_rfcinfo.json 

cmd2 = python ext_res/gen_impl_used_rule.py 1 ext_res/meta/Gen_bird_meta.json  ext_res/proc_info/bird.json

cmd2-1 = python ext_res/gen_impl_used_rule.py 2 ../input/ext-release/Bird-NEWS ext_res/tree/Gen_bird_rfcinfo.json

cmd2 = python ext_res/gen_impl_used_rule.py  1 ext_res/meta/Gen_openbgpd_meta.json ext_res/proc_info/openbgpd.json

cmd2-1 = python ext_res/gen_impl_used_rule.py  2 ../input/ext-release/openbsd.txt ext_res/tree/Gen_openbgpd_rfcinfo.json


cmd2 = python ext_res/gen_impl_used_rule.py 1 ext_res/meta/Gen_dhcpcd_meta.json  ext_res/proc_info/dhcpcd.json

cmd2 = python ext_res/gen_impl_used_rule.py  1 ext_res/meta/Gen_iscdhcp_meta.json ext_res/proc_info/iscdhcp.json


cmd2-1 = python ext_res/gen_impl_used_rule.py 2 ../input/ext-release/isc-dhcpRELNOTES ext_res/tree/Gen_iscdhcp_rfcinfo.json 

cmd2 = python ext_res/gen_impl_used_rule.py  1 ext_res/meta/Gen_busybox_meta.json ext_res/proc_info/busybox.json 


cmd2 = python ext_res/gen_impl_used_rule.py 1 ext_res/meta/Gen_freebsd_meta.json ext_res/proc_info/freebsd.json


cmd2 = python ext_res/gen_impl_used_rule.py 1 ext_res/meta/Gen_openbsd_meta.json ext_res/proc_info/openbsd.json

cmd2-1 = python ext_res/gen_impl_used_rule.py  2 ../input/ext-release/openbsd.txt ext_res/tree/

cmd2 = python ext_res/gen_impl_used_rule.py 1 ext_res/meta/Gen_ntp_meta.json ext_res/proc_info/ntpd.json 

cmd2 = python ext_res/gen_impl_used_rule.py ext_res/meta/Gen_ntpsec_meta.json ext_res/proc_info/ntpd.json
# check rule of value range T2
---
cmd3 = ./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/bgpd.bc ext_res/proc_rule/Impl_Gen_frr_meta.json bgp_process_packet 2

./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/bgpd.bc ext_res/proc_rule/Impl_Gen_frr_meta.json ext_res/tree/Gen_frr_tree.json ext_res/rule/Gen_frr_rule.json


python ext_res/annotation_release.py /share/test-target/frr-frr-8.4.2/bgpd/ ext_res/Impl/Cand_id_bgpd.json ext_res/meta/Gen_frr_meta.json /share/test-target/frr-frr-8.4.2/bgpd/



---

cmd3 = ./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/bird.bc ext_res/proc_rule/Impl_Gen_bird_meta.json bgp_rx 2

./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/bird.bc ext_res/proc_rule/Impl_Gen_bird_meta.json ext_res/tree/Gen_bird_tree.json ext_res/rule/Gen_bird_rule.json


python ext_res/annotation_release.py /share/test-target/bird-2.0.12/proto/ ext_res/Impl/Cand_id_bird.json  ext_res/meta/Gen_bird_meta.json /share/test-target/bird-2.0.12/proto/bgp/
----
cmd3 =./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/openbgpd.bc ext_res/proc_rule/Impl_Gen_openbgpd_meta.json session_process_msg 2 

./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/openbgpd.bc ext_res/proc_rule/Impl_Gen_openbgpd_meta.json ext_res/tree/Gen_openbgpd_tree.json ext_res/rule/Gen_openbgpd_rule.json

---
//dhcpcd
cmd3 = ./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/dhcpcd.bc ext_res/proc_rule/Impl_Gen_dhcpcd_meta.json dhcp_handledhcp 1


python ext_res/annotation_release.py /share/test-target/dhcpcd-9.4.1/src/ ext_res/Impl/Cand_id_dhcpcd.json ext_res/meta/Gen_dhcpcd_meta.json /share/test-target/dhcpcd-9.4.1/src/

./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/dhcpcd.bc ext_res/proc_rule/Impl_Gen_dhcpcd_meta.json ext_res/tree/Gen_dhcpcd_tree.json ext_res/rule/Gen_dhcpcd_rule.json



--
// busybox


cmd3 = ./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/busybox.bc ext_res/proc_rule/Impl_Gen_busybox_meta.json udhcpc_main 1


./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/busybox.bc ext_res/proc_rule/Impl_Gen_busybox_meta.json ext_res/tree/Gen_busybox_tree.json ext_res/rule/Gen_busybox_rule.json

python ext_res/annotation_release.py /share/test-target/busybox-1.35.0 ext_res/Impl/Cand_id_busybox.json ext_res/meta/Gen_dhcpcd_meta.json /share/test-target/busybox-1.35.0/networking/udhcp/


--
//iscdhcp
cmd3 = ./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/dhclient.bc ext_res/proc_rule/Impl_Gen_iscdhcp_meta.json do_packet 1


./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/dhclient.bc ext_res/proc_rule/Impl_Gen_iscdhcp_meta.json ext_res/tree/Gen_iscdhcp_tree.json ext_res/rule/Gen_iscdhcp_rule.json

 python ext_res/annotation_release.py /share/test-target/dhcp-4.4.3-P1/build_clang/common/ ext_res/Impl/Cand_id_dhclient.json ext_res/meta/Gen_iscdhcp_meta.json /share/test-target/dhcp-4.4.3-P1/common
// remember to change the pktvar in IdntifyExt.cpp
---
//freebsd

./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/freebsd-dhcp.bc ext_res/proc_rule/Impl_Gen_freebsd_meta.json ext_res/tree/Gen_freebsd_tree.json ext_res/rule/Gen_freebsd_rule.json

python ext_res/annotation_release.py /share/test-target/freebse-dhcp/ ext_res/Impl/Cand_id_freebsd-dhcp.json ext_res/meta/Gen_freebsd_meta.json /share/test-target/freebse-dhcp/

---
//openbsd
./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/openbsd-dhcp.bc ext_res/proc_rule/Impl_Gen_openbsd_meta.json ext_res/tree/Gen_openbsd_tree.json ext_res/rule/Gen_openbsd_rule.json

python ext_res/annotation_release.py /share/test-target/openbsd-dhcpd/ ext_res/Impl/Cand_id_openbsd-dhcp.json ext_res/meta/Gen_openbsd_meta.json /share/test-target/openbsd-dhcpd/

---

./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/ntpsec.bc    ext_res/proc_rule/Impl_Gen_ntpsec_meta.json parse_packet 0


./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/ntpsec.bc ext_res/proc_rule/Impl_Gen_ntpsec_meta.json ext_res/tree/Gen_ntpsec_tree.json ext_res/rule/Gen_ntpsec_rule.json
python ext_res/annotation_release.py /share/test-target/ntpsec-NTPsec_1_2_1/ntpd/ ext_res/Impl/Cand_id_ntpsec.json ext_res/meta/Gen_ntpsec_meta.json /share/test-target/ntpsec-NTPsec_1_2_1/ntpd/


---
./Release_build/bin/rfc -IdentifyExt ../input/pro
ifyExt ../input/proc/ext_proc/openntpd.bc    ext_res/proc_rule/Impl_Gen_ntpd_meta.json client_dispatch 0

./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/openntpd.bc ext_res/proc_rule/Impl_Gen_ntpd_meta.json ext_res/tree/Gen_ntpd_tree.json ext_res/rule/Gen_ntpd_rule.json 


--
./Release_build/bin/rfc -IdentifyExt ../input/pro
ifyExt ../input/proc/ext_proc/ntpd.bc    ext_res/proc_rule/Impl_Gen_ntpd_meta.json process_packet 0


./Release_build/bin/rfc -IdentifyExt ../input/proc/ext_proc/ntpd.bc ext_res/proc_rule/Impl_Gen_ntp_meta.json ext_res/tree/Gen_ntp_tree.json ext_res/rule/Gen_ntp_rule.json

python ext_res/annotation_release.py /share/test-target/ntp-4.2.8p15/ntpd/ ext_res/Impl/Cand_id_ntpd.json ext_res/meta/Gen_ntp_meta.json /share/test-target/ntp-4.2.8p15/ntpd/

---

# check rule of struct T1
cmd4= ./Release_build/bin/rfc -IdentifyOP ../input/proc/ext_proc/bgpd.bc ext_res/proc_rule/Impl_strGen_frr_meta_use.json
./Release_build/bin/rfc -IdentifyOP ../input/proc/ext_proc/bird.bc ext_res/proc_rule/Impl_strGen_bird_meta_use.json


cmd4 =  ./Release_build/bin/rfc -IdentifyOP ../input/proc/ext_proc/busybox.bc ext_res/proc_rule/Impl_strGen_busybox_meta_use.json

cmd4 = ./Release_build/bin/rfc -IdentifyOP ../input/proc/ext_proc/dhcpcd.bc ext_res/proc_rule/Impl_strGen_dhcpcd_meta_use.json

cmd4 = ./Release_build/bin/rfc -IdentifyOP ../input/proc/ext_proc/iscdhcp.bc ext_res/proc_rule/Impl_strGen_iscdhcp_meta_use.json


['RFC6037', 'RFC6368', 'RFC8092', 'RFC4271', 'RFC9015', 'RFC6793', 'RFC7753', 'Gargi_Nalawade', 'RFC9026', 'RFC9234', 'RFC6938', 'RFC8205', 'RFC8093', 'RFC4456', 'RFC5543', 'RFC8669', 'RFC7311', 'RFC4760', 'RFC6790', 'RFC9012', 'RFC4360', 'draft-ietf-idr-wide-bgp-communities', 'RFC6514', 'RFC5701', 'RFC1863', 'RFC2042', 'RFC1997', 'draft-ietf-idr-as-pathlimit', 'RFC4724', 'draft-walton-bgp-hostname-capability', 'RFC8950', 'RFC6793', 'draft-uttaro-idr-bgp-persistence', 'RFC5291', 'RFC5492', 'draft-ietf-idr-dynamic-cap', 'RFC9234', 'RFC2858', 'RFC2918', 'RFC8205', 'draft-ietf-idr-bgp-multisession', 'RFC8654', 'RFC8810', 'RFC7313', 'RFC7911', 'draft-ietf-idr-rpd-04', 'RFC8277']


# statistic annoation

# python annotation-ext.py /root/RIBDetector/test-target/frr-frr-8.4.2 ../RIBDetector-1126/tool/ext_res/tree/Gen_frr_k2r.json 
# python annotation-ext.py /root/RIBDetector/test-target/bird-2.0.12 ../RIBDetector-1126/tool/ext_res/tree/Gen_bird_k2r.json 
# python annotation-ext.py /root/RIBDetector/test-target/openbgpd-7.7 ../RIBDetector-1126/tool/ext_res/tree/Gen_openbgpd_k2r.json 
# python annotation-ext.py /root/RIBDetector/test-target/dhcp-4.4.3-P1 ../RIBDetector-1126/tool/ext_res/tree/Gen_iscdhcp_k2r.json 
# python annotation-ext.py /root/RIBDetector/test-target/dhcpcd-9.4.1 ../RIBDetector-1126/tool/ext_res/tree/Gen_dhcpcd_k2r.json 
# python annotation-ext.py /root/RIBDetector/test-target/busybox-1_36_0 ../RIBDetector-1126/tool/ext_res/tree/Gen_busybox_k2r.json 
# python annotation-ext.py /root/RIBDetector/test-target/freebse-dhcp ../RIBDetector-1126/tool/ext_res/tree/Gen_freebsd_k2r.json
# python annotation-ext.py /root/RIBDetector/test-target/openbsd-dhcpd ../RIBDetector-1126/tool/ext_res/tree/Gen_openbsd_k2r.json 
