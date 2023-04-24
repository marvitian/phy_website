import sys

full_key_list = ['Path', 'Phy_Cfg', 'Baud_Rate', 'MajorSystemMode', 'MajorMode', 'dfi2ckratio', 'SimMode_iDisableDebugPrint', 'dfiperiod', 'wck2ckratio', 'latencyMode', 'EffectiveRL', 'EffectiveWL', 'csr_WL', 'csr_nWR', 'csr_RL', 'csr_WLS', 'csr_DbiWr', 'csr_DbiRd', 'csr_DMD', 'tWDQS_on', 'tWDQS_off', 'csr_BL', 'csr_PDDS', 'csr_RPST', 'csr_DQSIntervalTimerRunTime', 'csr_DQODT', 'csr_CAODT', 'csr_CSODT', 'MinorMode_iActiveRanks', 'MinorMode_iRetrainMode', 'MinorMode_iWdqsDriveMode', 'MinorMode_iPLLCalMode', 'PLL_DisableHwCal', 'PLL_NumCalClkCycles', 'MinorMode_iDLLCalibrationMode', 'DLL_EnablePeriodicCal', 'DLL_Period', 'DLL_OverSampleRate', 'DLL_CodeChangeDelay', 'DLL_CommandWait', 'DLL_DcdlStart', 'DLL_DcdlStep', 'DLL_EnableUpdateLimit', 'DLL_UpdateLimit', 'MinorMode_iDFTProgram', 'MinorMode_iBumpReMap_En', 'BumpReMapCS_0', 'BumpReMapCS_1', 'BumpReMapCS_2', 'BumpReMapCS_3', 'BumpReMapCA_0', 'BumpReMapCA_1', 'BumpReMapCA_2', 'BumpReMapCA_3', 'BumpReMapCA_4', 'BumpReMapCA_5', 'BumpReMapCK', 'BumpReMapDBYTE_0', 'BumpReMapDQ0_0', 'BumpReMapDQ0_1', 'BumpReMapDQ0_2', 'BumpReMapDQ0_3', 'BumpReMapDQ0_4', 'BumpReMapDQ0_5', 'BumpReMapDQ0_6', 'BumpReMapDQ0_7', 'BumpReMapDMI_0', 'BumpReMapDQS_0', 'BumpReMapWCK_0', 'BumpReMapDBYTE_1', 'BumpReMapDQ1_0', 'BumpReMapDQ1_1', 'BumpReMapDQ1_2', 'BumpReMapDQ1_3', 'BumpReMapDQ1_4', 'BumpReMapDQ1_5', 'BumpReMapDQ1_6', 'BumpReMapDQ1_7', 'BumpReMapDMI_1', 'BumpReMapDQS_1', 'BumpReMapWCK_1', 'MinorMode_iClkEnMode', 'MinorMode_iRxTCTrain', 'MinorMode_iRetrainGateMode', 'MinorMode_iCSTEn', 'MinorMode_iRxEnhancedTrainMode', 'MinorMode_iPhyMstr_DRAM_Mode', 'MinorMode_iRxReadGateScheme', 'MinorMode_iDMITrainMode', 'MinorMode_iSARLogicMode', 'MinorMode_iProductionTestMode', 'MinorMode_iFWModeDebug', 'MinorMode_iTxDQVrefTrain', 'MinorMode_iRxDQVrefTrain', 'MinorMode_iCBTVrefTrain', 'MinorMode_iClkGatingMode', 'csr_RdqsPre', 'csr_WCKMode', 'tWCKENL_FS', 'tWCKPRE_Toggle_WR', 'csr_RpstMode', 'csr_RECC', 'csr_CKR', 'csr_BkOrg', 'csr_WCK_FM', 'tWCKENL_RD', 'csr_WECC', 'csr_CkMode', 'csr_WCK2DQIIntervalTimerRunTimeSetting', 'tWCKPST', 'tWCKPRE_Static', 'csr_RdqsPst', 'tWCKENL_WR', 'BumpReMapCA_6', 'tWCKPRE_Toggle_FS', 'csr_WCK2DQOIntervalTimerRunTimeSetting', 'tWCKPRE_Toggle_RD', 'csr_WckPst', 'csr_DVFSC', 'MinorMode_iCalibrationMode', 'csr_WCK_ON', 'MinorMode_iPhyMstr_Type3_Disable', 'MinorMode_iPhyMstr_Type2_Disable', 'SimMode_vArbitrerTest']
full_label_list = ['LABELS', 'exta', 'extra', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_TEST', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_TEST', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_MODE', 'FUNCTIONAL_MODE', 'FUNCTIONAL_MODE', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_TEST', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_MODE', 'FUNCTIONAL_MODE', 'FUNCTIONAL_TEST', 'FUNCTIONAL_MODE', 'FUNCTIONAL_MODE', 'FUNCTIONAL_MODE', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_SPEC', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST', 'FUNCTIONAL_TEST']

freq_bins_lp4 = [(10, 266), (267, 533), (534, 800), (801, 1066), (1067, 1333), (1334, 1600), (1601, 1866), (1867, 2133)]
freq_bins_lp5 = [(5, 67), (68, 133), (134, 200), (201, 267), (268, 344), (345, 400), (401, 467), (468, 533), (534, 600), (601, 688), (689, 750), (751, 800), (801, 850), (851, 900), (901, 950), (951, 1000), (1001, 1050), (1051, 1100)]



if __name__ == '__main__':
    
    ################### Self-Writing Code ###################
    # csv_path = "/home/mohamed/dbWeb/regrDB/old_csv/CONFIG_8303.csv"
    # with open(csv_path, "r") as csv_file:
    #     _key_list = csv_file.readline().strip().split(",")
    #     _label_list = csv_file.readline().strip().split(",")
    #     key_list = []
    #     label_list = []
    #     for index, key in enumerate(full_key_list):
    #         if key not in _key_list:
    #             key_list.append(key)
    #             label_list.append(full_label_list[index])
                
        
    #     print(key_list)
    #     print(label_list)
        
    #     print(len(key_list))
    #     print(len(label_list))
        
    #     print_flag = "FUNCTIONAL_SPEC"
        
    #     extra_keys = []
    #     functional_spec = []
    #     functional_mode = []
    #     functional_test = []
        
    #     # declaration
    #     for index, key_name in enumerate(key_list):
    #         # print(f"{index}\t{key_name}\t{key_list[index]}\t{label_list[index]}")
    #         if label_list[index] == "FUNCTIONAL_SPEC":
    #             functional_spec.append(key_name)
    #             # print(f"{key_name} \t\tspec \t\t {index}")
    #         elif label_list[index] == "FUNCTIONAL_MODE":
    #             functional_mode.append(key_name)                
    #             # print(f"{key_name} \t\tmode \t\t {index}")
    #         elif label_list[index] == "FUNCTIONAL_TEST":
    #             functional_test.append(key_name)
    #             # print(f"{key_name} \t\ttest \t\t {index}")
    #         else:
    #             extra_keys.append(key_name)
    #             # print(f"{key_name} \t\textra \t\t {index}")
                
        
    #     # declaration and init
    #     if print_flag == "FUNCTIONAL_SPEC":
    #         [ print(f"\t{key_name} = Column(\"{key_name}\", SmallInteger)") for key_name in functional_spec ]
    #         print(", ".join(functional_spec))
    #         [ print(f"\t\tself.{key_name} = {key_name}") for key_name in functional_spec ]
    #     if print_flag == "FUNCTIONAL_MODE":
    #         [ print(f"\t{key_name} = Column(\"{key_name}\", SmallInteger)") for key_name in functional_mode ]
    #         print(", ".join(functional_mode))
    #         [ print(f"\t\tself.{key_name} = {key_name}") for key_name in functional_mode ]
    #     if print_flag == "FUNCTIONAL_TEST":
    #         [ print(f"\t{key_name} = Column(\"{key_name}\", SmallInteger)") for key_name in functional_test ]
    #         print(", ".join(functional_test))
    #         [ print(f"\t\tself.{key_name} = {key_name}") for key_name in functional_test ]
        
    #     print(", ".join(extra_keys))
    ################### Self-Writing Code END ###################

    ################### Updating DB OLD ###################
    # from sqlalchemy import MetaData, create_engine, func
    # from sqlalchemy.orm import sessionmaker
    # from model import Base, CFG3_LP4_x8, CFG3_LP4_x16, CFG3_LP5_x16, CFG3_LP5_x8, CFG8_LP4_x16, CFG8_LP5_x16, CFG8_LP4_x8, CFG8_LP5_x8
    # from handlers import DB_Handler
    # import time, os, sys
    # import pandas as pd
       
       
    # # DB = "sqlite:///regressDB.db"
    
    # engine = create_engine("sqlite:///regressDB.db", echo=False)
    # # conn = engine.connect()
    # # db_handler = DB_Handler()
    
    # # TODO: Metadata says no tables
    # # https://stackoverflow.com/questions/38883256/with-sqlalchemy-metadata-reflect-how-do-you-get-an-actual-table-object
    
    # # Base.metadata.create_all(bind=engine)
    # print(Base.metadata.tables['CFG8_LP5_x16'].c.Baud_Rate)
    # print(type(Base.metadata.tables['CFG8_LP5_x16']))
    
    # filenames = [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk("./some_csv") for f in filenames]
    # col_list = []
    # label_list = []
    # for filename in filenames:
    #     print(filename)
    #     file_stats = os.stat(filename)
    #     print(f'File Size is {file_stats.st_size / (1024 * 1024)} Mb')
    #     start = time.time()
    #     # TODO: Create global var in __init__ for new csv tables and save this path in there
    #     csv_df = db_handler.import_csv(filename, engine, "/home/mohamed/dbWeb/regrDB/new_csv")
    #     end = time.time()
    #     print(f"Insert Time is {end - start}")
    #     print("# -------------- #")
    #     break
        
    #     # read csv headers
    #     # df = pd.read_csv(filename, header=0, index_col=False)
    #     # col_list.append(df.columns.to_list())
    #     # label_list.append(df.iloc[0].to_list())
    
    # Get number of rows in a table
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # rows = session.query(func.count(CFG_1_Run.tid)).scalar()
    # print(f" rows = {rows}")
    
    # db_handler.save_csv()
    
    # std = col_list[0]
    # std_label = label_list[0]
    # print(std)
    # print(std_label)
    # for index, clist in enumerate(col_list):
    #     if clist != std:
    #         print(filenames[index])
    #         # print(clist)
    #         # Keys in new table that are not in std
    #         for key_index, key in enumerate(std):
    #             if key not in clist:
    #                 print(f"Missing Key: {key}")
    #         # Extra keys in new table
    #         for key_index, key in enumerate(clist):
    #             if key not in std:
    #                 print(f"Extra Key: {key} {label_list[index][key_index]}")
    #                 std.append(key)
    #                 std_label.append(label_list[index][key_index])
    #         print("# ----------------- #")
    
    # print(std)
    # print(std_label)
    ######################################
    
    
    ########## QUERY ###############
    from queryDB import query_csr_db
    my_dict = {'MajorSystemMode': 'LP4', 'MinorMode': '16', 'DFI2CKRatio': '4', 'baud': '1800'}
    out_dir = 'TEMP_DIR'
    print(**my_dict)
    query_csr_db(out_path=out_dir, args=my_dict)
    
    ################################
    
    ########## Post-Processing ###############
    # from csrInit_pstprcs import CSRInit_PP
    # paths = ['/home/mohamed/dbWeb/regrDB/csrInits/csrInitStruct_cfg3_LP5_x16_3184Mbps.txt']
    # csrinit_pp = CSRInit_PP(paths)
    # csrinit_pp.post_process()
    ####################################