import os

class CSRInit_PP():
    
    def __init__(self, paths) -> None:
        self.paths = paths
    
    def post_process(self):
        for path in self.paths:
            if os.path.exists(path):
                print('Exists')
                
        # add ch0_fsp0
        # if the file is single speed, duplicate on fsp 0 and 1
        
                with open(path, "r+") as csr_file:
                    line = csr_file.readline()
                    
                    while line != '':
                        if ('Major' not in line) and ('Minor' not in line) and ('SimMode' not in line) and ('#' not in line):
                            ln_prt = line.strip().split("=")
                            # print(ln_prt)
                            print(f"{ln_prt[0]}ch0_fsp0 = {ln_prt[1]}")
                        else:
                            print(line)
                        line = csr_file.readline()



# Example
#  MajorSystemMode = LP5            X
#  MajorMode = x16                  X
#  dfi2ckratio_ch0_fsp0 = 0 
#  SimMode_iDisableDebugPrint = 0   X
#  dfiperiod_ch0_fsp0 = 2508 
#  wck2ckratio_ch0_fsp0 = 4 
#  latencyMode_ch0_fsp0 = 1 
#  EffectiveRL_ch0_fsp0 = 9 
#  EffectiveWL_ch0_fsp0 = 5 
#  csr_WL_ch0_fsp0 = 5 
#  csr_nWR_ch0_fsp0 = 5 
#  csr_RL_ch0_fsp0 = 5 
#  csr_WLS_ch0_fsp0 = 0 
#  csr_DbiWr_ch0_fsp0 = 0 
#  csr_DbiRd_ch0_fsp0 = 0 
#  csr_DMD_ch0_fsp0 = 1 
#  tWCKENL_WR_ch0_fsp0 = 2 
#  tWCKENL_RD_ch0_fsp0 = 3 
#  tWCKENL_FS_ch0_fsp0 = 1 
#  tWCKPRE_Static_ch0_fsp0 = 2 
#  tWCKPRE_Toggle_WR_ch0_fsp0 = 2 
#  tWCKPRE_Toggle_RD_ch0_fsp0 = 5 
#  tWCKPRE_Toggle_FS_ch0_fsp0 = 7 
#  tWCKPST_ch0_fsp0 = 5 
#  csr_CkMode_ch0_fsp0 = 0 
#  csr_BkOrg_ch0_fsp0 = 2 
#  csr_RdqsPst_ch0_fsp0 = 1 
#  csr_RdqsPre_ch0_fsp0 = 1 
#  csr_WckPst_ch0_fsp0 = 1 
#  csr_RpstMode_ch0_fsp0 = 0 
#  csr_WCK_FM_ch0_fsp0 = 0 
#  csr_CKR_ch0_fsp0 = 0 
#  csr_WCKMode_ch0_fsp0 = 0 
#  csr_RECC_ch0_fsp0 = 0 
#  csr_WECC_ch0_fsp0 = 0 
#  csr_WCK2DQIIntervalTimerRunTimeSetting_ch0_fsp0 = 111 
#  csr_WCK2DQOIntervalTimerRunTimeSetting_ch0_fsp0 = 199 
#  csr_DQODT_ch0_fsp0 = 4 
#  csr_CAODT_ch0_fsp0 = 6 
#  csr_CSODT_ch0_fsp0 = 2 
#  MinorMode_iActiveRanks = 1           X
#  MinorMode_iRetrainMode = 1           X
#  MinorMode_iWdqsDriveMode = 0         X
#  MinorMode_iPLLCalMode = 0            X
#  PLL_DisableHwCal_ch0_fsp0 = 0 
#  PLL_NumCalClkCycles_ch0_fsp0 = 16 
#  MinorMode_iDLLCalibrationMode = 0    X
#  DLL_EnablePeriodicCal_ch0_fsp0 = 0 
#  DLL_Period_ch0_fsp0 = 445 
#  DLL_OverSampleRate_ch0_fsp0 = 15 
#  DLL_CodeChangeDelay_ch0_fsp0 = 15 
#  DLL_CommandWait_ch0_fsp0 = 3 
#  DLL_DcdlStart_ch0_fsp0 = 0 
#  DLL_DcdlStep_ch0_fsp0 = 8 
#  DLL_EnableUpdateLimit_ch0_fsp0 = 1 
#  DLL_UpdateLimit_ch0_fsp0 = 4 
#  MinorMode_iDFTProgram = 0            X
#  MinorMode_iClkEnMode = 0             X
#  MinorMode_iRxTCTrain = 0             X
#  MinorMode_iRetrainGateMode = 1       X
#  MinorMode_iCSTEn = 0                 X
#  MinorMode_iRxEnhancedTrainMode = 0   X
#  MinorMode_iPhyMstr_DRAM_Mode = 0     X
#  MinorMode_iRxReadGateScheme = 0      X

#  dfi2ckratio_ch0_fsp1 = 0 
#  dfiperiod_ch0_fsp1 = 2508 
#  wck2ckratio_ch0_fsp1 = 4 
#  latencyMode_ch0_fsp1 = 1 
#  EffectiveRL_ch0_fsp1 = 9 
#  EffectiveWL_ch0_fsp1 = 5 
#  csr_WL_ch0_fsp1 = 5 
#  csr_nWR_ch0_fsp1 = 5 
#  csr_RL_ch0_fsp1 = 5 
#  csr_WLS_ch0_fsp1 = 0 
#  csr_DbiWr_ch0_fsp1 = 0 
#  csr_DbiRd_ch0_fsp1 = 0 
#  csr_DMD_ch0_fsp1 = 1 
#  tWCKENL_WR_ch0_fsp1 = 2 
#  tWCKENL_RD_ch0_fsp1 = 3 
#  tWCKENL_FS_ch0_fsp1 = 1 
#  tWCKPRE_Static_ch0_fsp1 = 2 
#  tWCKPRE_Toggle_WR_ch0_fsp1 = 2 
#  tWCKPRE_Toggle_RD_ch0_fsp1 = 5 
#  tWCKPRE_Toggle_FS_ch0_fsp1 = 7 
#  tWCKPST_ch0_fsp1 = 5 
#  csr_CkMode_ch0_fsp1 = 0 
#  csr_BkOrg_ch0_fsp1 = 2 
#  csr_RdqsPst_ch0_fsp1 = 1 
#  csr_RdqsPre_ch0_fsp1 = 1 
#  csr_WckPst_ch0_fsp1 = 1 
#  csr_RpstMode_ch0_fsp1 = 0 
#  csr_WCK_FM_ch0_fsp1 = 0 
#  csr_CKR_ch0_fsp1 = 0 
#  csr_WCKMode_ch0_fsp1 = 0 
#  csr_RECC_ch0_fsp1 = 0 
#  csr_WECC_ch0_fsp1 = 0 
#  csr_WCK2DQIIntervalTimerRunTimeSetting_ch0_fsp1 = 111 
#  csr_WCK2DQOIntervalTimerRunTimeSetting_ch0_fsp1 = 199 
#  csr_DQODT_ch0_fsp1 = 4 
#  csr_CAODT_ch0_fsp1 = 6 
#  csr_CSODT_ch0_fsp1 = 2 
#  PLL_DisableHwCal_ch0_fsp1 = 0 
#  PLL_NumCalClkCycles_ch0_fsp1 = 16 
#  DLL_EnablePeriodicCal_ch0_fsp1 = 0 
#  DLL_Period_ch0_fsp1 = 445 
#  DLL_OverSampleRate_ch0_fsp1 = 15 
#  DLL_CodeChangeDelay_ch0_fsp1 = 15 
#  DLL_CommandWait_ch0_fsp1 = 3 
#  DLL_DcdlStart_ch0_fsp1 = 0 
#  DLL_DcdlStep_ch0_fsp1 = 8 
#  DLL_EnableUpdateLimit_ch0_fsp1 = 1 
#  DLL_UpdateLimit_ch0_fsp1 = 4