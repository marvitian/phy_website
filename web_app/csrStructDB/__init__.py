
from sqlalchemy import create_engine
import os, logging
# import updateDB
# import queryDB
# import model

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = 'regressDB.db'
DB = "sqlite:///" + os.path.join(DB_DIR,DB_NAME) + '?check_same_thread=False'
TABLES_DIR = DB_DIR + "/Tables"

freq_bins_lp4 = [(10, 266), (267, 533), (534, 800), (801, 1066), (1067, 1333), (1334, 1600), (1601, 1866), (1867, 2133)]
freq_bins_lp5 = [(5, 67), (68, 133), (134, 200), (201, 267), (268, 344), (345, 400), (401, 467), (468, 533), (534, 600), (601, 688), (689, 750), (751, 800), (801, 850), (851, 900), (901, 950), (951, 1000), (1001, 1050), (1051, 1100)]

__all__ = ['model', 'queryDB', 'updateDB']
# from . import queryDB

# Create db engine 
def db_create_engine():
    return create_engine(DB, echo=False)

# NOTE: UNTESTED
def get_key_label(key):
    return get_lable_list()[get_key_list().index(key)]
    
def get_key_list():
        return ['Path', 'Phy_Cfg', 'Baud_Rate', 'MajorSystemMode', 'MajorMode', 'dfi2ckratio', 'SimMode_iDisableDebugPrint', 'dfiperiod', 'wck2ckratio', 'latencyMode', 'EffectiveRL', 'EffectiveWL', 'csr_WL', 'csr_nWR', 'csr_RL', 'csr_WLS', 'csr_DbiWr', 'csr_DbiRd', 'csr_DMD', 'tWDQS_on', 'tWDQS_off', 'csr_BL', 'csr_PDDS', 'csr_RPST', 'csr_DQSIntervalTimerRunTime', 'csr_DQODT', 'csr_CAODT', 'csr_CSODT', 'MinorMode_iActiveRanks', 'MinorMode_iRetrainMode', 'MinorMode_iWdqsDriveMode', 'MinorMode_iPLLCalMode', 'PLL_DisableHwCal', 'PLL_NumCalClkCycles', 'MinorMode_iDLLCalibrationMode', 'DLL_EnablePeriodicCal', 'DLL_Period', 'DLL_OverSampleRate', 'DLL_CodeChangeDelay', 'DLL_CommandWait', 'DLL_DcdlStart', 'DLL_DcdlStep', 'DLL_EnableUpdateLimit', 'DLL_UpdateLimit', 'MinorMode_iDFTProgram', 'MinorMode_iBumpReMap_En', 'BumpReMapCS_0', 'BumpReMapCS_1', 'BumpReMapCS_2', 'BumpReMapCS_3', 'BumpReMapCA_0', 'BumpReMapCA_1', 'BumpReMapCA_2', 'BumpReMapCA_3', 'BumpReMapCA_4', 'BumpReMapCA_5', 'BumpReMapCK', 'BumpReMapDBYTE_0', 'BumpReMapDQ0_0', 'BumpReMapDQ0_1', 'BumpReMapDQ0_2', 'BumpReMapDQ0_3', 'BumpReMapDQ0_4', 'BumpReMapDQ0_5', 'BumpReMapDQ0_6', 'BumpReMapDQ0_7', 'BumpReMapDMI_0', 'BumpReMapDQS_0', 'BumpReMapWCK_0', 'BumpReMapDBYTE_1', 'BumpReMapDQ1_0', 'BumpReMapDQ1_1', 'BumpReMapDQ1_2', 'BumpReMapDQ1_3', 'BumpReMapDQ1_4', 'BumpReMapDQ1_5', 'BumpReMapDQ1_6', 'BumpReMapDQ1_7', 'BumpReMapDMI_1', 'BumpReMapDQS_1', 'BumpReMapWCK_1', 'MinorMode_iClkEnMode', 'MinorMode_iRxTCTrain', 'MinorMode_iRetrainGateMode', 'MinorMode_iCSTEn', 'MinorMode_iRxEnhancedTrainMode', 'MinorMode_iPhyMstr_DRAM_Mode', 'MinorMode_iRxReadGateScheme', 'MinorMode_iDMITrainMode', 'MinorMode_iSARLogicMode', 'MinorMode_iProductionTestMode', 'MinorMode_iFWModeDebug', 'MinorMode_iTxDQVrefTrain', 'MinorMode_iRxDQVrefTrain', 'MinorMode_iCBTVrefTrain', 'MinorMode_iClkGatingMode', 'csr_RdqsPre', 'csr_WCKMode', 'tWCKENL_FS', 'tWCKPRE_Toggle_WR', 'csr_RpstMode', 'csr_RECC', 'csr_CKR', 'csr_BkOrg', 'csr_WCK_FM', 'tWCKENL_RD', 'csr_WECC', 'csr_CkMode', 'csr_WCK2DQIIntervalTimerRunTimeSetting', 'tWCKPST', 'tWCKPRE_Static', 'csr_RdqsPst', 'tWCKENL_WR', 'BumpReMapCA_6', 'tWCKPRE_Toggle_FS', 'csr_WCK2DQOIntervalTimerRunTimeSetting', 'tWCKPRE_Toggle_RD', 'csr_WckPst', 'csr_DVFSC', 'MinorMode_iCalibrationMode', 'csr_WCK_ON', 'MinorMode_iPhyMstr_Type3_Disable', 'MinorMode_iPhyMstr_Type2_Disable', 'SimMode_vArbitrerTest']
    
# TODO: Fix "Extra" and make first 3 the same
## For inserting into db
def get_lable_list():
    return ['LABELS', 'exta', 'extra', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_TEST', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_TEST', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_MODE', 'FUNCTIONAL_MODE', 'FUNCTIONAL_MODE', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_TEST', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_MODE', 'FUNCTIONAL_MODE', 'FUNCTIONAL_TEST', 'FUNCTIONAL_MODE', 'FUNCTIONAL_MODE', 'FUNCTIONAL_MODE', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST']

def get_functional_spec():
    functional_spec = []
    for label, key in zip(get_lable_list(), get_key_list()):
        
        if label == 'FUNCTIONAL_SPEC' and (key not in ('MajorSystemMode', 'MajorMode', 'dfi2ckratio')) :
            functional_spec.append(key)
    # print(functional_spec)
    return functional_spec

def get_functional_mode():
    functional_mode = []
    for label, key in zip(get_lable_list(), get_key_list()):
        if label == 'FUNCTIONAL_MODE':
            functional_mode.append(key)
    # print(functional_mode)
    return functional_mode


def get_functional_test():
    functional_test = []
    for label, key in zip(get_lable_list(), get_key_list()):
        if label == 'FUNCTIONAL_TEST':
            functional_test.append(key)
    # print(functional_test)
    return functional_test