# EBugDec
EBugDec is a tool which performs evolutionary bug detection in protocol implementations. It supports the following functionality:

1. Given a series of RFC documents and clue in IANA, it can reconstruct RFC relationship and infer evolutionary rules.
2. It can identify the rule-related code location by code annotations and release notes.
3. It can detect both rule condition violations and incomplete error handling issues.

Currently, EBugDec supports detection on C/C++ protocol implementations only.

# File structure
The most important folders in EBugDec's root directory are:


1. **'tool'**, directory containing the Python scripts for rule extraction and the LLVM pass for bug detection.

2. **'input'**, directory containing examples of configuration file and RFC documents. 

    i. **'doc/rfcxxx.json'** contains the RFC document of network protocol. 
    
    ii. **'config/xx.json'**, example of evolutionary tree and evolutionary rules generated based on the Frrouting-BGP and Openbsd-BGP RFC supported.
    
    iii. **'proc/xx.bc'**, example of  .bc file of network protocol implementations complied with LLVM.

    iv. **'Text-info/'**, contains the Release notes file and source code of protocol implementations.


3. **'output'**, directory containing examples of identified  and bug detection.

    i. **'result_of_identify/Identify_xx.json'**: Rule-Related code Location, such as parsing function or field access location.
   
    ii. **'evolutionary_bug/bug_report_xx'**: evolutionary bugs reported by EBugDec.


# How to use

To use EBugDec, it is necessary to perform the following steps:
1. Ensure pre-requisites are met
2. Complie the under-considering protocol implementation into one .bc file by WLLVM
3. Use EBugDec to perform evolutionary bug detection on the file.

## Ensuing pre-requisites

EBugDec has been tested on Ubuntu 16.04. It should work on any recent Linux distribution. Support for other platform has not been tested. In a nutshell, the advised pre-requisites are:
* Ubuntu 16.04 
* Pyhton3.6, NLTK, spacy 
* LLVM 10.0, Clang 10.0
* WLLVM
* Z3 Solver 4.8.10

## Compiling Target Implementation

Before performing bug detection, one should compile the target protocol implementation with WLLVM.

```
export LLVM_COMPILER=clang
CC=wllvm CXX=wllvm++  ./configure  CFLAGS="-g -O0"
extract-bc <target_dir> 
```
## Run EBugDec

To  perform inconsistency bug detection on the implementation, run the following command under tool directory:
```
tool/run_script.py -bc <input bitcode> -erule <evolutionary rules> -info <Text-info dir>  
-bc                .bc file of the implementation
-erule               Evolutionary Rules generated based on the implemenation RFC supported

-info              Release notes and source code of the implementation

eg: tool/run_script.py -bc input/proc/bgpd.bc -erule input/Gen_frr_tree.json -info input/Text-info/frr
```
## Results of EBugDec

**Result of Evolutionary Rule Extractor**

Examples of evolutionary tree reconstruction and evolutionary rules extraction result can be found under input/config/ directory.
e.g. input/config/Gen_frr_bgp_packet.json
```
{
  "Message Header Format": {
    ...   // Open message -> Optional Parameters -> Capabilities
    "Capabilities": {
      "struct": {
        "Capability Code": {
          "bitwidth": 8
          "extend_value": {   
            "Multiprotocol Extensions for BGP-4": {"value": "1"},
            ...
            "Long-Lived Graceful Restart (LLGR) Capability": { "value": "71"},
          },
          "rule": [{  // chk_bf(range(Capability_Code)=[1,...71], access(Capability_Code))
            "OP": { "USE": "Capability Code"},       //  access(Capability_Code)
            "Cond": [{                                      
              "rfc_cond": [                          // range(Capability_Code)=[1,...71]
                {"lhs": "x", "predicate": "32", "rhs": "1" },
                ...
                {"lhs": "x","predicate": "32", "rhs": "71"}
              ],
            "connect": [2],
            "type": 3,
            "keyword": "Capability Code"
            }]
          }]
        },
        "Capability Length": {
          "bitwidth": 8,
          "rule":[]
        },
        "Capability Value": {
          "bitwidth": -1,
          "extend_struct":{
            "Long-Lived Graceful Restart (LLGR) Capability": {  // if Capabiltiy_Code == 71
              "struct": {
                "Address Family Identifier": {"bitwidth": 16},
                "Subsequent Address Family Identifier": {"bitwidth": 8},
                "Flags for Address Family": {"bitwidth": 8},
                "Long-lived Stale Time":{"bitwidth": 24}
              },  
              "rule": [{ // chk_bf(Capability_Length % 7 == 0, access(Capabiltiy_Value)) if Capabiltiy_Code == 71
                "OP": { "USE": "Capability Value" },                            // access(Capabiltiy_Value)
                "Cond":[{
                  "rfc_cond": [{"lhs": "x", "predicate": "35", "rhs": "56" }],  //Capability_Length % 7 == 0
                  type": 1,
                  "keyword": "Capability Length"
                }]
              }]
            }
          }
}}}}}
```

**Result of Rule-related Code Identifier**

Examples of Rule-related Code identified by our tool based on pattern and Text-info, which can be found under output/result_of_identify/ directory.

e.g. output/result_of_identify/Identify_frr_bgp.json
```
...
"Capabilities":{
    "loc":["bgp_capability_parse"]

    "Multiprotocol Extensions for BGP-4": {
      "Type": 1,
      "loc": ["bgp_capability_mp"]
    },
    ...
    "ADD-PATH Capability": {
      "Type": 69,
      "loc": ["bgp_capability_addpath"]
    },
    "Long-Lived Graceful Restart (LLGR) Capability": {
      "Type": 71,
      "loc": ["bgp_capability_llgr"]
    }
}
```

**Result of Rule Violation Detector**

Example of rule violations can be found under  output/evolutionary_bug/ directory.

e.g. output/evolutionary_bug/bug_report_frr_bgp.json
```
=============
Rule violation:
Rule: chk_bf(Capability_Length % 7 == 0, access(Capabiltiy_Value)) if Capabiltiy_Code == 71
Function : bgp_capability_llgr Get: stream_getw in line:../bgpd/bgp_open.c 607
[Error] Missing Len check, value is 7
   BR: ( 4 + stream_get_getp() ) 37 end
-------
.....
```
## Evolutionary bugs that has been confirmed and fixed

We have reported 12 evolutionary bugs discovered by EBugDec to the developers. So far, we have received 7 confirmed.


**Frrouting(2)**

https://github.com/FRRouting/frr/issues/13099

https://github.com/FRRouting/frr/issues/13098

**Wolfssl(3)**

https://github.com/wolfSSL/wolfssl/issues/5436

**Openbsd-BGP(1)**

https://marc.info/?l=openbsd-bugs&m=167938589111527&w=2

**Freebsd-DHCP(1)**

https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=270379

**ISC DHCP(5)**

We have send the email, waiting for response.
