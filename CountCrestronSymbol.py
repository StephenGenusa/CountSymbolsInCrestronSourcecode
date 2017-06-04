#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# By Stephen Genusa
# June 2017
#
# Copyright © 2017 by Stephen Genusa
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
##############################################################################

import argparse
import fnmatch
import glob
import os
import re
from collections import Counter, OrderedDict

class CountUniqueCrestronSymbols:

    def __init__(self, includemodules, showfilenames, inputpath):
        self.symbolsfound = []
        self.firstpass = True
        self.longestsymname = 10
        self.includemodules = includemodules
        self.showfilenames = showfilenames
        self.inputpath = inputpath
        self.excludedDevices = []
    

    def countSymbols(self, filelist):
        if len(filelist) > 0:
            for orig_filename in filelist:
                if self.firstpass:
                    self.firstpass = False
                    print " " * 4 + "Processing Path: "  + os.path.dirname(self.inputpath)
                if self.showfilenames:
                    print " " * 8 + os.path.basename(orig_filename)
                if os.path.isfile(orig_filename): 
                    with open(orig_filename, 'r') as content_file:
                        file_contents = content_file.read()
                        regexresults = re.findall(r"\[\n(.*?)\n\]", file_contents, re.DOTALL)
                        for regexfind in regexresults:
                            if "ObjTp=Sm" in regexfind:
                                if "Nm=" in regexfind:
                                    nameex = re.search(r"Nm\=(.*?)\n", regexfind, re.DOTALL).group(1)
                                    # Exclude some devices
                                    if nameex not in ["Logic", "Ethernet", "DefineArguments", "Network Modules", "Central Control Modules", "C2 COM Two-way serial driver", ""]:
                                        # Exclude some other devices
                                        devicesToExcludeBeginWith = ['12001-',  '4001-', '8001-', 'AAE', 'AAS-', 'ADAGIO-', 'ADMS-', 'AM-', 'AMP-', 'AMS-', 'ATC-', 'AV2 With Card Cage', 'AV3 ', 'C2COM-', 'C2ENET-', 'C2I-', 'C2IR One-way serial driver', 'C2IR-', 'C2N-', 'C2NI-', 'C2Net-', 'C2PAC2MENET-1', 'C2QENET-1', 'C2VEQ-', 'C2Z-', 'C2ZPAC2MENET-', 'C2ZQ-', 'C3', 'C3CN-', 'C3COM-', 'C3IO-', 'C3IR-', 'C3RY-', 'CAEN-', 'CAPTURE-', 'CC2I-', 'CCS-', 'CEN-', 'CH-', 'CHV-', 'CLC-', 'CLCI-', 'CLF-', 'CLFI-', 'CLS-', 'CLW-', 'CLWI-', 'CLX-', 'CN-', 'CNAMP', 'CNAMPX-', 'CNAO-', 'CNCOMH-', 'CNCOMH-2 Two-way serial driver', 'CNET-', 'CNIR-', 'CNIRHT-', 'CNLDAB-', 'CNLDM-', 'CNLIO-', 'CNLSP-', 'CNRF', 'CNRS-', 'CNRY-', 'CNTTD-', 'CNWM-', 'CNWMVC-', 'CNX', 'CNX-', 'CNXAO-', 'CNXRMCOM-', 'CP3 ', 'CP3N ', 'CPC-', 'CSA-', 'CSC-', 'CSM-', 'CT-', 'Crestron ', 'DA-', 'DAP8 ', 'DAP8COM-', 'DCA-', 'DGE-', 'DIN-', 'DM-', 'DMB-', 'DMC-', 'DMCI-', 'DMCO-', 'DMPS3 ', 'DMPS3 Ethernet Devices', 'DMPS3-', 'DMS-', 'DSP VOIP Reserved Joins', 'DSP-', 'DSP-128', 'DVPHD (Cr', 'FT-', 'GL-', 'GLI-', 'GLPAC', 'GLPAC-', 'GLPP-', 'GLS-', 'GLX-', 'GLXP-', 'GLXX-', 'HD-', 'HD-XSPA', 'HDMI-', 'HOME-', 'HOME-CONNECT-', 'HR-', 'HR-100', 'HR-150', 'HTT-', 'IM-', 'INET-', 'INETI-', 'INETS-', 'IP-', 'Internal CNCOMH-2', 'LC-', 'MC3 ', 'ML-', 'MLX-', 'MMS-', 'MP-', 'MPS-', 'MT-', 'MTX-', 'PA-', 'PAMP-', 'PC-', 'PC200-', 'PC300-', 'PROAMP-', 'PT-', 'QM-', 'QM-RMC', 'RFGW-', 'RMC3 ', 'RS-', 'RoomView Connected', 'SMWMACRO', 'ST-', 'ST-COM', 'ST-IO', 'STI-', 'STRFGWX', 'STX-', 'SW-', 'SWAMP ', 'SWAMP-', 'SWAMPE-', 'SWE', 'SWE-', 'TPCS-', 'TPMC-', 'TPS-', 'TS-', 'TSCW-', 'TSR-', 'TSS-', 'TST-', 'TSTAT', 'TSW-', 'TT-', 'TVAVCOM-', 'UFO-', 'UPX-', 'VMK-', 'VPG-', 'VT-3500', 'WPR-', 'XPanel', 'iPhone/iPod Touch interfac']
                                        for devicePrefix in devicesToExcludeBeginWith:
                                            excludeDevice = False
                                            if nameex.startswith(devicePrefix):
                                                excludeDevice = True
                                                break
                                                
                                        if ((self.includemodules) or ((not self.includemodules) and (not nameex.lower().endswith((".cmc", ".umc", ".csp", ".ced", ".usp"))))):
                                            if not excludeDevice:
                                                self.symbolsfound.append(nameex)
                                                if len(nameex) > self.longestsymname:
                                                    self.longestsymname = len(nameex)



    def showSymbolCounts(self):
        print
        counted = Counter(self.symbolsfound)
        od = OrderedDict()
        # Build the ordered dict
        for w in sorted(counted, key=counted.get, reverse=True):
            od[w]=counted[w]
        # Now loop through and get a total symbol count
        totalSymbols = 0
        for item in od:
            totalSymbols += od[item]
        print "Total symbols found in SMW, UMC and CMC files in project directory", totalSymbols
        # Now show the symbol info
        print "-" * (self.longestsymname + 16)
        with open("symbol_count.csv", 'w') as csv_file:
            for item in od:
                pctUsed = "{0:.1f}%".format((od[item]*100.0) / totalSymbols) 
                print "|" + item.ljust(self.longestsymname) + "|" + str(od[item]).rjust(6) + "|" + pctUsed.rjust(6)+"|"
                # write to the CSV file
                csv_file.write(item + "," + str(od[item])+ "," + pctUsed + "\n")
        print "-" * (self.longestsymname + 16)

    
def main():
    print "Symbol Counter - By Stephen Genusa - v1.0"
    parser = argparse.ArgumentParser(description="Symbol Counter - By Stephen Genusa - v1.0")
    parser.add_argument("-i", "--inputpath", dest="inputpath", default = ".", help="Input path", required=True)
    parser.add_argument("-m", "--includemodules", dest="includemodules", action='store_true', default = False, help="Include in symbol listing external CMCs, UMCs and USPs")
    parser.add_argument("-s", "--showfilenames", dest="showfilenames", action='store_true', default = False, help="Show filenames as they are parsed")
    args = parser.parse_args()
    counter = CountUniqueCrestronSymbols(args.includemodules, args.showfilenames, args.inputpath)
    
    print " " * 4 + "Getting filenames for path", args.inputpath
    dirmatches = []
    for root, dirnames, filenames in os.walk(args.inputpath):
        for filename in fnmatch.filter(filenames, '*.smw'):
            dirmatches.append(os.path.join(root, filename))    
        for filename in fnmatch.filter(filenames, '*.umc'):
            dirmatches.append(os.path.join(root, filename))    
        for filename in fnmatch.filter(filenames, '*.cmc'):
            dirmatches.append(os.path.join(root, filename))   
    counter.countSymbols(dirmatches)
    counter.showSymbolCounts()

if __name__ == "__main__":
    main()