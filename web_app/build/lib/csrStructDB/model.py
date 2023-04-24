from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, SmallInteger, ARRAY, Boolean, JSON, DateTime, func

# Base class that we will extent/ inheret from
from sqlalchemy.ext.declarative import declarative_base, declared_attr

# session maker will create a session --> we can then do things with our database
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


### ASK:
# Which can be boolean or not?

# This stays: we can use this to do something like .filter("regression_path") or date added

# this will have,
# regression_path
# which  cfg the
# table that has the runs
# baud range
# system modes
# you can have regression path repeated if there's multiple cfgs in the same path
#   e.g. if path has runs for cfg3 and runs for cfg4
#       X_path cfg3 CFG3_Table {baud range} {system modes}

# class Regression_Folder(Base):
#     __tablename__ = "Regression_Folders"
    
#     # baud rate ranges
#     # regression date - date added to regression
#     #  https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
#     # phy cfgs in regression
#     # system modes in regression 
#     Regression_Path = Column("Regression_Path", String, primary_key=True)
#     # Baud_Rate_Range = Column("Baud_Rate_Range", JSON, nullable=False)
#     Baud_Rate_Max = Column("Baud_Rate_Max", SmallInteger, nullable=False)
#     Baud_Rate_Min  = Column("Baud_Rate_Min", SmallInteger, nullable=False)
#     Phy_Cfg = Column("Phy_Cfg", SmallInteger, nullable=False)    
#     System_Mode = Column("System_Mode", SmallInteger, nullable=False)
#     cfg_table_log_runs = relationship("", back_populates="parent")
#     # cfg_table = relationship('')
#     # CFG_Table id
    
#     # Array type only in postgresql
#     # Baud_Rate_Range = Column("Baud_Rate_Range", ARRAY(Integer), nullable=False)
#     # Phy_Cfgs = Column("Phy_Cfgs", ARRAY(SmallInteger), nullable=False)
#     # System_Modes = Column("System_Modes", ARRAY(SmallInteger), nullable=False)
    
#     def __init__(self, regr_path, baud_rate_min, baud_rate_max, phy_cfg, system_mode) -> None:
#         self.Regression_Path = regr_path
#         self.Baud_Rate_Min = baud_rate_min        
#         self.Baud_Rate_Max = baud_rate_max
#         self.Phy_Cfg = phy_cfg
#         self.System_Mode = system_mode
        
#     def __repr__(self) -> str:
#         return f"self.Regression_Path = {self.Regression_Path}\nself.Baud_Rate_Range = {self.Baud_Rate_Range}\nself.Phy_Cfgs = {self.Phy_Cfgs}\nself.System_Modes = {self.System_Modes}\n"


class Regression_Folder(Base):
    __tablename__ = "regression_folder"
    fid = Column("Fid", SmallInteger, primary_key=True)
    config_num = Column("Config_Num", SmallInteger, nullable=False)
    folder_path = Column("Folder_Path", String, nullable=False)   # full run path
    date = Column("Date", DateTime(timezone=True), default=func.now())
    # first_tid = Column("First_Tid", Integer, nullable=False)
    # baud_min = Column("Baud_Min", SmallInteger, nullable=False)
    # baud_max = Column("Baud_Max", SmallInteger, nullable=False)
    
    
    protocol = Column("Protocol", SmallInteger, nullable=False)    
    mode = Column("Mode", SmallInteger, nullable=False)
    phy_cfg = Column("Phy_Cfg", SmallInteger, nullable=False)
    cfg_table = Column("Cfg_Table", String, nullable=False)

    # cfg_table_id = relationshup(CFG_X_)
    


# class CFG_RUN()

#     ...
#     regression_folder = column(db.ForeignKey('Regression_Folder.fid'))
#     regr_folder_id = Column(db.Integer, db.ForeignKey('regression_folder.fid'))
    
    
class CFG_Run():
    
    # Relational Variables
    tid = Column("tid", Integer, primary_key=True) # SQLAlchemy will automatically set the first Integer PK column that's not marked as a FK as autoincrement=True
    Path = Column("Path", String)   # full run path
    # Phy_Cfg = Column("Phy_Cfg", SmallInteger)
    Baud_Rate = Column("Baud_Rate", Integer)
    # @declared_attr
    # def regression_folder(cls): #TODO: CLS?
    #     return Column("regression_folder", ForeignKey("Regression_Folders.Regression_Path"))
    
    # Functional Spec Keys
    MajorSystemMode = Column("MajorSystemMode", SmallInteger, nullable=False)
    MajorMode = Column("MajorMode", SmallInteger, nullable=False)
    dfi2ckratio = Column("dfi2ckratio", SmallInteger, nullable=False)
    dfiperiod = Column("dfiperiod", Integer)
    wck2ckratio = Column("wck2ckratio", SmallInteger)
    EffectiveRL = Column("EffectiveRL", SmallInteger)
    EffectiveWL = Column("EffectiveWL", SmallInteger)
    csr_WL = Column("csr_WL", SmallInteger)
    csr_nWR = Column("csr_nWR", SmallInteger)
    csr_RL = Column("csr_RL", SmallInteger)
    csr_WLS = Column("csr_WLS", SmallInteger)
    tWDQS_on = Column("tWDQS_on", SmallInteger)    
    tWDQS_off = Column("tWDQS_off", SmallInteger)
    csr_BL = Column("csr_BL", SmallInteger)
    csr_RPST = Column("csr_RPST", SmallInteger)
    MinorMode_iActiveRanks = Column("MinorMode_iActiveRanks", SmallInteger)
    #
    csr_DVFSC = Column("csr_DVFSC", SmallInteger)
    
    # Functional Mode Keys
    csr_DbiWr = Column("csr_DbiWr", SmallInteger)                   
    csr_DbiRd = Column("csr_DbiRd", SmallInteger)                  
    csr_DMD = Column("csr_DMD", SmallInteger)                    
    MinorMode_iClkEnMode = Column("MinorMode_iClkEnMode", SmallInteger)             
    MinorMode_iRxTCTrain = Column("MinorMode_iRxTCTrain", SmallInteger)            
    MinorMode_iCSTEn = Column("MinorMode_iCSTEn", SmallInteger)               
    MinorMode_iRxEnhancedTrainMode = Column("MinorMode_iRxEnhancedTrainMode", SmallInteger)          
    MinorMode_iPhyMstr_DRAM_Mode = Column("MinorMode_iPhyMstr_DRAM_Mode", SmallInteger) 
    
    # Functional Test Keys
    SimMode_iDisableDebugPrint = Column("SimMode_iDisableDebugPrint", SmallInteger)
    latencyMode = Column("latencyMode", SmallInteger)
    csr_PDDS = Column("csr_PDDS", SmallInteger)
    csr_DQSIntervalTimerRunTime = Column("csr_DQSIntervalTimerRunTime", SmallInteger)
    csr_DQODT = Column("csr_DQODT", SmallInteger)
    csr_CAODT = Column("csr_CAODT", SmallInteger)
    csr_CSODT = Column("csr_CSODT", SmallInteger)
    MinorMode_iRetrainMode = Column("MinorMode_iRetrainMode", SmallInteger)
    MinorMode_iWdqsDriveMode = Column("MinorMode_iWdqsDriveMode", SmallInteger)
    MinorMode_iPLLCalMode = Column("MinorMode_iPLLCalMode", SmallInteger)
    PLL_DisableHwCal = Column("PLL_DisableHwCal", SmallInteger)
    PLL_NumCalClkCycles = Column("PLL_NumCalClkCycles", SmallInteger)
    MinorMode_iDLLCalibrationMode = Column("MinorMode_iDLLCalibrationMode", SmallInteger)
    DLL_EnablePeriodicCal = Column("DLL_EnablePeriodicCal", SmallInteger)
    DLL_Period = Column("DLL_Period", SmallInteger)
    DLL_OverSampleRate = Column("DLL_OverSampleRate", SmallInteger)
    DLL_CodeChangeDelay = Column("DLL_CodeChangeDelay", SmallInteger)
    DLL_CommandWait = Column("DLL_CommandWait", SmallInteger)
    DLL_DcdlStart = Column("DLL_DcdlStart", SmallInteger)
    DLL_DcdlStep = Column("DLL_DcdlStep", SmallInteger)
    DLL_EnableUpdateLimit = Column("DLL_EnableUpdateLimit", SmallInteger)
    DLL_UpdateLimit = Column("DLL_UpdateLimit", SmallInteger)
    MinorMode_iDFTProgram = Column("MinorMode_iDFTProgram", SmallInteger)
    MinorMode_iBumpReMap_En = Column("MinorMode_iBumpReMap_En", SmallInteger)
    BumpReMapCS_0 = Column("BumpReMapCS_0", SmallInteger)
    BumpReMapCS_1 = Column("BumpReMapCS_1", SmallInteger)
    BumpReMapCS_2 = Column("BumpReMapCS_2", SmallInteger)
    BumpReMapCS_3 = Column("BumpReMapCS_3", SmallInteger)
    BumpReMapCA_0 = Column("BumpReMapCA_0", SmallInteger)
    BumpReMapCA_1 = Column("BumpReMapCA_1", SmallInteger)
    BumpReMapCA_2 = Column("BumpReMapCA_2", SmallInteger)
    BumpReMapCA_3 = Column("BumpReMapCA_3", SmallInteger)
    BumpReMapCA_4 = Column("BumpReMapCA_4", SmallInteger)
    BumpReMapCA_5 = Column("BumpReMapCA_5", SmallInteger)
    BumpReMapCK = Column("BumpReMapCK", SmallInteger)
    BumpReMapDBYTE_0 = Column("BumpReMapDBYTE_0", SmallInteger)
    BumpReMapDQ0_0 = Column("BumpReMapDQ0_0", SmallInteger)
    BumpReMapDQ0_1 = Column("BumpReMapDQ0_1", SmallInteger)
    BumpReMapDQ0_2 = Column("BumpReMapDQ0_2", SmallInteger)
    BumpReMapDQ0_3 = Column("BumpReMapDQ0_3", SmallInteger)
    BumpReMapDQ0_4 = Column("BumpReMapDQ0_4", SmallInteger)
    BumpReMapDQ0_5 = Column("BumpReMapDQ0_5", SmallInteger)
    BumpReMapDQ0_6 = Column("BumpReMapDQ0_6", SmallInteger)
    BumpReMapDQ0_7 = Column("BumpReMapDQ0_7", SmallInteger)
    BumpReMapDMI_0 = Column("BumpReMapDMI_0", SmallInteger)
    BumpReMapDQS_0 = Column("BumpReMapDQS_0", SmallInteger)
    BumpReMapWCK_0 = Column("BumpReMapWCK_0", SmallInteger)
    BumpReMapDBYTE_1 = Column("BumpReMapDBYTE_1", SmallInteger)
    BumpReMapDQ1_0 = Column("BumpReMapDQ1_0", SmallInteger)
    BumpReMapDQ1_1 = Column("BumpReMapDQ1_1", SmallInteger)
    BumpReMapDQ1_2 = Column("BumpReMapDQ1_2", SmallInteger)
    BumpReMapDQ1_3 = Column("BumpReMapDQ1_3", SmallInteger)
    BumpReMapDQ1_4 = Column("BumpReMapDQ1_4", SmallInteger)
    BumpReMapDQ1_5 = Column("BumpReMapDQ1_5", SmallInteger)
    BumpReMapDQ1_6 = Column("BumpReMapDQ1_6", SmallInteger)
    BumpReMapDQ1_7 = Column("BumpReMapDQ1_7", SmallInteger)
    BumpReMapDMI_1 = Column("BumpReMapDMI_1", SmallInteger)
    BumpReMapDQS_1 = Column("BumpReMapDQS_1", SmallInteger)
    BumpReMapWCK_1 = Column("BumpReMapWCK_1", SmallInteger)
    MinorMode_iRetrainGateMode = Column("MinorMode_iRetrainGateMode", SmallInteger)
    MinorMode_iRxReadGateScheme = Column("MinorMode_iRxReadGateScheme", SmallInteger)
    MinorMode_iDMITrainMode = Column("MinorMode_iDMITrainMode", SmallInteger)
    MinorMode_iSARLogicMode = Column("MinorMode_iSARLogicMode", SmallInteger)
    MinorMode_iProductionTestMode = Column("MinorMode_iProductionTestMode", SmallInteger)
    MinorMode_iFWModeDebug = Column("MinorMode_iFWModeDebug", SmallInteger)
    MinorMode_iTxDQVrefTrain = Column("MinorMode_iTxDQVrefTrain", SmallInteger)
    MinorMode_iRxDQVrefTrain = Column("MinorMode_iRxDQVrefTrain", SmallInteger)
    MinorMode_iCBTVrefTrain = Column("MinorMode_iCBTVrefTrain", SmallInteger)
    MinorMode_iClkGatingMode = Column("MinorMode_iClkGatingMode", SmallInteger)
    csr_RdqsPre = Column("csr_RdqsPre", SmallInteger)
    csr_WCKMode = Column("csr_WCKMode", SmallInteger)
    tWCKENL_FS = Column("tWCKENL_FS", SmallInteger)
    tWCKPRE_Toggle_WR = Column("tWCKPRE_Toggle_WR", SmallInteger)
    csr_RpstMode = Column("csr_RpstMode", SmallInteger)
    csr_RECC = Column("csr_RECC", SmallInteger)
    csr_CKR = Column("csr_CKR", SmallInteger)
    csr_BkOrg = Column("csr_BkOrg", SmallInteger)
    csr_WCK_FM = Column("csr_WCK_FM", SmallInteger)
    tWCKENL_RD = Column("tWCKENL_RD", SmallInteger)
    csr_WECC = Column("csr_WECC", SmallInteger)
    csr_CkMode = Column("csr_CkMode", SmallInteger)
    csr_WCK2DQIIntervalTimerRunTimeSetting = Column("csr_WCK2DQIIntervalTimerRunTimeSetting", SmallInteger)
    tWCKPST = Column("tWCKPST", SmallInteger)
    tWCKPRE_Static = Column("tWCKPRE_Static", SmallInteger)
    csr_RdqsPst = Column("csr_RdqsPst", SmallInteger)
    tWCKENL_WR = Column("tWCKENL_WR", SmallInteger)
    BumpReMapCA_6 = Column("BumpReMapCA_6", SmallInteger)
    tWCKPRE_Toggle_FS = Column("tWCKPRE_Toggle_FS", SmallInteger)
    csr_WCK2DQOIntervalTimerRunTimeSetting = Column("csr_WCK2DQOIntervalTimerRunTimeSetting", SmallInteger)
    tWCKPRE_Toggle_RD = Column("tWCKPRE_Toggle_RD", SmallInteger)
    csr_WckPst = Column("csr_WckPst", SmallInteger)
    #
    MinorMode_iCalibrationMode = Column("MinorMode_iCalibrationMode", SmallInteger)
    csr_WCK_ON = Column("csr_WCK_ON", SmallInteger)
    MinorMode_iPhyMstr_Type3_Disable = Column("MinorMode_iPhyMstr_Type3_Disable", SmallInteger)
    MinorMode_iPhyMstr_Type2_Disable = Column("MinorMode_iPhyMstr_Type2_Disable", SmallInteger)
    SimMode_vArbitrerTest = Column("SimMode_vArbitrerTest", SmallInteger)
    
    def __init__(self, Path, phy_cfg, baud_rate, MajorSystemMode, MajorMode, dfi2ckratio, dfiperiod, wck2ckratio, EffectiveRL, EffectiveWL, csr_WL, csr_nWR, csr_RL, csr_WLS, tWDQS_on, tWDQS_off, csr_BL, csr_RPST, MinorMode_iActiveRanks, csr_DVFSC, \
    csr_DbiWr, csr_DbiRd, csr_DMD, MinorMode_iClkEnMode, MinorMode_iRxTCTrain, MinorMode_iCSTEn, MinorMode_iRxEnhancedTrainMode, MinorMode_iPhyMstr_DRAM_Mode, \
    SimMode_iDisableDebugPrint, latencyMode, csr_PDDS, csr_DQSIntervalTimerRunTime, csr_DQODT, csr_CAODT, csr_CSODT, MinorMode_iRetrainMode, MinorMode_iWdqsDriveMode, MinorMode_iPLLCalMode, PLL_DisableHwCal, PLL_NumCalClkCycles, MinorMode_iDLLCalibrationMode, DLL_EnablePeriodicCal, DLL_Period, DLL_OverSampleRate, DLL_CodeChangeDelay, DLL_CommandWait, DLL_DcdlStart, DLL_DcdlStep, DLL_EnableUpdateLimit, DLL_UpdateLimit, MinorMode_iDFTProgram, MinorMode_iBumpReMap_En, BumpReMapCS_0, BumpReMapCS_1, BumpReMapCS_2, BumpReMapCS_3, BumpReMapCA_0, BumpReMapCA_1, BumpReMapCA_2, BumpReMapCA_3, BumpReMapCA_4, BumpReMapCA_5, BumpReMapCK, BumpReMapDBYTE_0, BumpReMapDQ0_0, BumpReMapDQ0_1, BumpReMapDQ0_2, BumpReMapDQ0_3, BumpReMapDQ0_4, BumpReMapDQ0_5, BumpReMapDQ0_6, BumpReMapDQ0_7, BumpReMapDMI_0, BumpReMapDQS_0, BumpReMapWCK_0, BumpReMapDBYTE_1, BumpReMapDQ1_0, BumpReMapDQ1_1, BumpReMapDQ1_2, BumpReMapDQ1_3, BumpReMapDQ1_4, BumpReMapDQ1_5, BumpReMapDQ1_6, BumpReMapDQ1_7, BumpReMapDMI_1, BumpReMapDQS_1, BumpReMapWCK_1, MinorMode_iRetrainGateMode, MinorMode_iRxReadGateScheme, MinorMode_iDMITrainMode, MinorMode_iSARLogicMode, MinorMode_iProductionTestMode, MinorMode_iFWModeDebug, MinorMode_iTxDQVrefTrain, MinorMode_iRxDQVrefTrain, MinorMode_iCBTVrefTrain, MinorMode_iClkGatingMode, csr_RdqsPre, csr_WCKMode, tWCKENL_FS, tWCKPRE_Toggle_WR, csr_RpstMode, csr_RECC, csr_CKR, csr_BkOrg, csr_WCK_FM, tWCKENL_RD, csr_WECC, csr_CkMode, csr_WCK2DQIIntervalTimerRunTimeSetting, tWCKPST, tWCKPRE_Static, csr_RdqsPst, tWCKENL_WR, BumpReMapCA_6, tWCKPRE_Toggle_FS, csr_WCK2DQOIntervalTimerRunTimeSetting, tWCKPRE_Toggle_RD, csr_WckPst, MinorMode_iCalibrationMode, csr_WCK_ON, MinorMode_iPhyMstr_Type3_Disable, MinorMode_iPhyMstr_Type2_Disable, SimMode_vArbitrerTest) -> None:
        # self.regression_folder = regression_folder
        self.Path = Path
        self.Phy_Cfg = phy_cfg
        self.Baud_Rate = baud_rate
    
        # Functional Spec Keys
        self.MajorSystemMode = MajorSystemMode
        self.MajorMode = MajorMode
        self.dfi2ckratio = dfi2ckratio
        self.dfiperiod = dfiperiod
        self.wck2ckratio = wck2ckratio
        self.EffectiveRL = EffectiveRL
        self.EffectiveWL = EffectiveWL
        self.csr_WL = csr_WL
        self.csr_nWR = csr_nWR
        self.csr_RL = csr_RL
        self.csr_WLS = csr_WLS
        self.tWDQS_on = tWDQS_on
        self.tWDQS_off = tWDQS_off
        self.csr_BL = csr_BL
        self.csr_RPST = csr_RPST
        self.MinorMode_iActiveRanks = MinorMode_iActiveRanks
        #
        self.csr_DVFSC = csr_DVFSC
        
        # Functional Mode Keys
        self.csr_DbiWr = csr_DbiWr
        self.csr_DbiRd = csr_DbiRd
        self.csr_DMD = csr_DMD
        self.MinorMode_iClkEnMode = MinorMode_iClkEnMode
        self.MinorMode_iRxTCTrain = MinorMode_iRxTCTrain
        self.MinorMode_iCSTEn = MinorMode_iCSTEn
        self.MinorMode_iRxEnhancedTrainMode = MinorMode_iRxEnhancedTrainMode
        self.MinorMode_iPhyMstr_DRAM_Mode = MinorMode_iPhyMstr_DRAM_Mode
        
        # Functional Test Keys
        self.SimMode_iDisableDebugPrint = SimMode_iDisableDebugPrint
        self.latencyMode = latencyMode
        self.csr_PDDS = csr_PDDS
        self.csr_DQSIntervalTimerRunTime = csr_DQSIntervalTimerRunTime
        self.csr_DQODT = csr_DQODT
        self.csr_CAODT = csr_CAODT
        self.csr_CSODT = csr_CSODT
        self.MinorMode_iRetrainMode = MinorMode_iRetrainMode
        self.MinorMode_iWdqsDriveMode = MinorMode_iWdqsDriveMode
        self.MinorMode_iPLLCalMode = MinorMode_iPLLCalMode
        self.PLL_DisableHwCal = PLL_DisableHwCal
        self.PLL_NumCalClkCycles = PLL_NumCalClkCycles
        self.MinorMode_iDLLCalibrationMode = MinorMode_iDLLCalibrationMode
        self.DLL_EnablePeriodicCal = DLL_EnablePeriodicCal
        self.DLL_Period = DLL_Period
        self.DLL_OverSampleRate = DLL_OverSampleRate
        self.DLL_CodeChangeDelay = DLL_CodeChangeDelay
        self.DLL_CommandWait = DLL_CommandWait
        self.DLL_DcdlStart = DLL_DcdlStart
        self.DLL_DcdlStep = DLL_DcdlStep
        self.DLL_EnableUpdateLimit = DLL_EnableUpdateLimit
        self.DLL_UpdateLimit = DLL_UpdateLimit
        self.MinorMode_iDFTProgram = MinorMode_iDFTProgram
        self.MinorMode_iBumpReMap_En = MinorMode_iBumpReMap_En
        self.BumpReMapCS_0 = BumpReMapCS_0
        self.BumpReMapCS_1 = BumpReMapCS_1
        self.BumpReMapCS_2 = BumpReMapCS_2
        self.BumpReMapCS_3 = BumpReMapCS_3
        self.BumpReMapCA_0 = BumpReMapCA_0
        self.BumpReMapCA_1 = BumpReMapCA_1
        self.BumpReMapCA_2 = BumpReMapCA_2
        self.BumpReMapCA_3 = BumpReMapCA_3
        self.BumpReMapCA_4 = BumpReMapCA_4
        self.BumpReMapCA_5 = BumpReMapCA_5
        self.BumpReMapCK = BumpReMapCK
        self.BumpReMapDBYTE_0 = BumpReMapDBYTE_0
        self.BumpReMapDQ0_0 = BumpReMapDQ0_0
        self.BumpReMapDQ0_1 = BumpReMapDQ0_1
        self.BumpReMapDQ0_2 = BumpReMapDQ0_2
        self.BumpReMapDQ0_3 = BumpReMapDQ0_3
        self.BumpReMapDQ0_4 = BumpReMapDQ0_4
        self.BumpReMapDQ0_5 = BumpReMapDQ0_5
        self.BumpReMapDQ0_6 = BumpReMapDQ0_6
        self.BumpReMapDQ0_7 = BumpReMapDQ0_7
        self.BumpReMapDMI_0 = BumpReMapDMI_0
        self.BumpReMapDQS_0 = BumpReMapDQS_0
        self.BumpReMapWCK_0 = BumpReMapWCK_0
        self.BumpReMapDBYTE_1 = BumpReMapDBYTE_1
        self.BumpReMapDQ1_0 = BumpReMapDQ1_0
        self.BumpReMapDQ1_1 = BumpReMapDQ1_1
        self.BumpReMapDQ1_2 = BumpReMapDQ1_2
        self.BumpReMapDQ1_3 = BumpReMapDQ1_3
        self.BumpReMapDQ1_4 = BumpReMapDQ1_4
        self.BumpReMapDQ1_5 = BumpReMapDQ1_5
        self.BumpReMapDQ1_6 = BumpReMapDQ1_6
        self.BumpReMapDQ1_7 = BumpReMapDQ1_7
        self.BumpReMapDMI_1 = BumpReMapDMI_1
        self.BumpReMapDQS_1 = BumpReMapDQS_1
        self.BumpReMapWCK_1 = BumpReMapWCK_1
        self.MinorMode_iRetrainGateMode = MinorMode_iRetrainGateMode
        self.MinorMode_iRxReadGateScheme = MinorMode_iRxReadGateScheme
        self.MinorMode_iDMITrainMode = MinorMode_iDMITrainMode
        self.MinorMode_iSARLogicMode = MinorMode_iSARLogicMode
        self.MinorMode_iProductionTestMode = MinorMode_iProductionTestMode
        self.MinorMode_iFWModeDebug = MinorMode_iFWModeDebug
        self.MinorMode_iTxDQVrefTrain = MinorMode_iTxDQVrefTrain
        self.MinorMode_iRxDQVrefTrain = MinorMode_iRxDQVrefTrain
        self.MinorMode_iCBTVrefTrain = MinorMode_iCBTVrefTrain
        self.MinorMode_iClkGatingMode = MinorMode_iClkGatingMode
        self.csr_RdqsPre = csr_RdqsPre
        self.csr_WCKMode = csr_WCKMode
        self.tWCKENL_FS = tWCKENL_FS
        self.tWCKPRE_Toggle_WR = tWCKPRE_Toggle_WR
        self.csr_RpstMode = csr_RpstMode
        self.csr_RECC = csr_RECC
        self.csr_CKR = csr_CKR
        self.csr_BkOrg = csr_BkOrg
        self.csr_WCK_FM = csr_WCK_FM
        self.tWCKENL_RD = tWCKENL_RD
        self.csr_WECC = csr_WECC
        self.csr_CkMode = csr_CkMode
        self.csr_WCK2DQIIntervalTimerRunTimeSetting = csr_WCK2DQIIntervalTimerRunTimeSetting
        self.tWCKPST = tWCKPST
        self.tWCKPRE_Static = tWCKPRE_Static
        self.csr_RdqsPst = csr_RdqsPst
        self.tWCKENL_WR = tWCKENL_WR
        self.BumpReMapCA_6 = BumpReMapCA_6
        self.tWCKPRE_Toggle_FS = tWCKPRE_Toggle_FS
        self.csr_WCK2DQOIntervalTimerRunTimeSetting = csr_WCK2DQOIntervalTimerRunTimeSetting
        self.tWCKPRE_Toggle_RD = tWCKPRE_Toggle_RD
        self.csr_WckPst = csr_WckPst
        #
        self.MinorMode_iCalibrationMode = MinorMode_iCalibrationMode
        self.csr_WCK_ON = csr_WCK_ON
        self.MinorMode_iPhyMstr_Type3_Disable = MinorMode_iPhyMstr_Type3_Disable
        self.MinorMode_iPhyMstr_Type2_Disable = MinorMode_iPhyMstr_Type2_Disable
        self.SimMode_vArbitrerTest = SimMode_vArbitrerTest
        
        
        
    
    def __repr__(self) -> str:
        # return f"self.Baud_Rate = {self.Baud_Rate}\nself.Phy_Cfg = {self.Phy_Cfg}\nself.Path = {self.Path}\nself.regression_folder = {self.regression_folder}\nself.tid = {self.tid}\n self._MajorSystemMode = {self._MajorSystemMode}\nself._MajorMode = {self._MajorMode}\nself._dfi2ckratio = {self._dfi2ckratio}\nself._dfiperiod = {self._dfiperiod}\nself._wck2ckratio = {self._wck2ckratio}\nself._EffectiveRL = {self._EffectiveRL}\nself._EffectiveWL = {self._EffectiveWL}\nself._csr_WL = {self._csr_WL}\nself._csr_nWR = {self._csr_nWR}\nself._csr_RL = {self._csr_RL}\nself._csr_WLS = {self._csr_WLS}\nself._tWDQS_on = {self._tWDQS_on}\nself._tWDQS_off = {self._tWDQS_off}\nself._csr_BL = {self._csr_BL}\nself._csr_RPST = {self._csr_RPST}\nself._csr_DQSIntervalTimerRunTimeSmallInteger = {self._csr_DQSIntervalTimerRunTimeSmallInteger}\n"
        return f"tid = {self.tid}\tbd = {self.Baud_Rate}\tsys = {self.MajorSystemMode}\tmode = {self.MajorMode}\tdfi = {self.dfi2ckratio}\twck2ck = {self.wck2ckratio}\tEffRL = {self.EffectiveRL}\tEffWL = {self.EffectiveWL}\n"

# class CFG_Run_FUNC():
#     spec_id = Column("SPEC_ID", ForeignKey("CFG_Run.id"))

# class CFG_Run_FUNC_MODE(CFG_Run_FUNC):
#     # common functional mode keys across all configurations

    
# class CFG_Run_FUNC_TEST(CFG_Run_FUNC):
#     # common functional test keys across all configurations


# ------------------------ Tables ------------------------ # 
# CFG 3
class CFG3_LP4_x8(CFG_Run, Base):
    __tablename__ = "CFG3_LP4_x8"
    
# ##
class CFG3_LP4_x16(CFG_Run, Base):
    __tablename__ = "CFG3_LP4_x16"
    
# class CFG3_LP4_x16_FUNC_MODE(CFG_Run_FUNC_MODE, Base):
#     __tablename__ = "CFG3_LP4_x16_FUNC_MODE"
    

# class CFG3_LP4_x16_FUNC_TEST(CFG_Run_FUNC, Base):
#     __tablename__ = "CFG3_LP4_x16_FUNC_TEST"
##
class CFG3_LP5_x8(CFG_Run, Base):
    __tablename__ = "CFG3_LP5_x8"
##
class CFG3_LP5_x16(CFG_Run, Base):
    __tablename__ = "CFG3_LP5_x16"
    
# CFG 8
class CFG8_LP4_x8(CFG_Run, Base):
    __tablename__ = "CFG8_LP4_x8"

class CFG8_LP4_x16(CFG_Run, Base):
    __tablename__ = "CFG8_LP4_x16"

class CFG8_LP5_x8(CFG_Run, Base):
    __tablename__ = "CFG8_LP5_x8"

class CFG8_LP5_x16(CFG_Run, Base):
    __tablename__ = "CFG8_LP5_x16"



# class CFG8_LP4_x8
# class CFG8_LP4_x16


# class CFG8_LP4_x8_Functional_Test(Functional_Test, Base)

# Regression_Run_CFG_0
#   run path
#   baud rate
#   either: 1) all keys or 2) FUNCTIONAL_SPEC, FUNCTION_MODE, FUNCTION_TEST objects and relationship in o
# class Regression_Run(Base):
#     # __tablename__ = "Regression_Runs"  
#     # Relational Variables
#     tid = Column("tid", Integer, primary_key=True)
#     regression_folder = Column("regression_folder", ForeignKey("Regression_Folders.Regression_Path"))
#     Path = Column("Path", String)
#     Phy_Cfg = Column("Phy_Cfg", SmallInteger)
#     Baud_Rate = Column("Baud_Rate", Integer)
    
#     # Functional Spec Keys
#     _MajorSystemMode = Column("MajorSystemMode", SmallInteger, nullable=False)
#     _MajorMode = Column("MajorMode", SmallInteger, nullable=False)
#     _dfi2ckratio = Column("dfi2ckratio", SmallInteger, nullable=False)
#     _dfiperiod = Column("dfiperiod", Integer)
#     _wck2ckratio = Column("wck2ckratio", SmallInteger)
#     _EffectiveRL = Column("EffectiveRL", SmallInteger)
#     _EffectiveWL = Column("EffectiveWL", SmallInteger)
#     _csr_WL = Column("csr_WL", SmallInteger)
#     _csr_nWR = Column("csr_nWR", SmallInteger)
#     _csr_RL = Column("csr_RL", SmallInteger)
#     _csr_WLS = Column("csr_WLS", SmallInteger)
#     _tWDQS_on = Column("tWDQS_on", SmallInteger)    
#     _tWDQS_off = Column("tWDQS_off", SmallInteger)
#     _csr_BL = Column("csr_BL", SmallInteger)
#     _csr_RPST = Column("csr_RPST", SmallInteger)
#     _csr_DQSIntervalTimerRunTime = Column("csr_DQSIntervalTimerRunTime", SmallInteger)
    
#     def __init__(self, regression_folder, path, phy_cfg, baud_rate, MajorSystemMode, MajorMode, dfi2ckratio, dfiperiod, wck2ckratio, EffectiveRL, EffectiveWL, csr_WL, csr_nWR, csr_RL, csr_WLS, tWDQS_on, tWDQS_off, csr_BL, csr_RPST, csr_DQSIntervalTimerRunTimeSmallInteger) -> None:
#         Regression_Run.__tablename__ = path
#         self.regression_folder = regression_folder
#         self.Path = path
#         self.Phy_Cfg = phy_cfg
#         self.Baud_Rate = baud_rate
    
#         # Functional Spec Keys
#         self._MajorSystemMode = MajorSystemMode
#         self._MajorMode = MajorMode
#         self._dfi2ckratio = dfi2ckratio
#         self._dfiperiod = dfiperiod
#         self._wck2ckratio = wck2ckratio
#         self._EffectiveRL = EffectiveRL
#         self._EffectiveWL = EffectiveWL
#         self._csr_WL = csr_WL
#         self._csr_nWR = csr_nWR
#         self._csr_RL = csr_RL
#         self._csr_WLS = csr_WLS
#         self._tWDQS_on = tWDQS_on
#         self._tWDQS_off = tWDQS_off
#         self._csr_BL = csr_BL
#         self._csr_RPST = csr_RPST
#         self._csr_DQSIntervalTimerRunTimeSmallInteger = csr_DQSIntervalTimerRunTimeSmallInteger
    
    
#     def __repr__(self) -> str:
#         return f"self.Baud_Rate = {self.Baud_Rate}\nself.Phy_Cfg = {self.Phy_Cfg}\nself.Path = {self.Path}\nself.regression_folder = {self.regression_folder}\nself.tid = {self.tid}\n self._MajorSystemMode = {self._MajorSystemMode}\nself._MajorMode = {self._MajorMode}\nself._dfi2ckratio = {self._dfi2ckratio}\nself._dfiperiod = {self._dfiperiod}\nself._wck2ckratio = {self._wck2ckratio}\nself._EffectiveRL = {self._EffectiveRL}\nself._EffectiveWL = {self._EffectiveWL}\nself._csr_WL = {self._csr_WL}\nself._csr_nWR = {self._csr_nWR}\nself._csr_RL = {self._csr_RL}\nself._csr_WLS = {self._csr_WLS}\nself._tWDQS_on = {self._tWDQS_on}\nself._tWDQS_off = {self._tWDQS_off}\nself._csr_BL = {self._csr_BL}\nself._csr_RPST = {self._csr_RPST}\nself._csr_DQSIntervalTimerRunTimeSmallInteger = {self._csr_DQSIntervalTimerRunTimeSmallInteger}\n"
        


    

 # To seperate keys by label and speed up
# class Functional_Mode(Base):
#     __tablename__ = "Regression_Runs" 
#     # functional mode keys
#     # related to regr run class by id?
    
#     # Functional Mode Keys
#     csr_DbiWr = Column("csr_DbiWr", SmallInteger)                   
#     csr_DbiRd = Column("csr_DbiRd", SmallInteger)                  
#     csr_DMD = Column("csr_DMD", SmallInteger)                    
#     MinorMode_iClkEnMode = Column("MinorMode_iClkEnMode", SmallInteger)             
#     MinorMode_iRxTCTrain = Column("MinorMode_iRxTCTrain", SmallInteger)            
#     MinorMode_iCSTEn = Column("MinorMode_iCSTEn", SmallInteger)               
#     MinorMode_iRxEnhancedTrainMode = Column("MinorMode_iRxEnhancedTrainMode", SmallInteger)          
#     MinorMode_iPhyMstr_DRAM_Mode = Column("MinorMode_iPhyMstr_DRAM_Mode", SmallInteger) 
    
# class Functional_Test(Base):
#     # functional mode keys
#     # related to regr run class by id?
    
#     # Functional Test Keys
#     SimMode_iDisableDebugPrint = Column("SimMode_iDisableDebugPrint", SmallInteger)
#     latencyMode = Column("latencyMode", SmallInteger)
#     csr_PDDS = Column("csr_PDDS", SmallInteger)
#     csr_DQSIntervalTimerRunTime = Column("csr_DQSIntervalTimerRunTime", SmallInteger)
#     csr_DQODT = Column("csr_DQODT", SmallInteger)
#     csr_CAODT = Column("csr_CAODT", SmallInteger)
#     csr_CSODT = Column("csr_CSODT", SmallInteger)
#     MinorMode_iRetrainMode = Column("MinorMode_iRetrainMode", SmallInteger)
#     MinorMode_iWdqsDriveMode = Column("MinorMode_iWdqsDriveMode", SmallInteger)
#     MinorMode_iPLLCalMode = Column("MinorMode_iPLLCalMode", SmallInteger)
#     PLL_DisableHwCal = Column("PLL_DisableHwCal", SmallInteger)
#     PLL_NumCalClkCycles = Column("PLL_NumCalClkCycles", SmallInteger)
#     MinorMode_iDLLCalibrationMode = Column("MinorMode_iDLLCalibrationMode", SmallInteger)
#     DLL_EnablePeriodicCal = Column("DLL_EnablePeriodicCal", SmallInteger)
#     DLL_Period = Column("DLL_Period", SmallInteger)
#     DLL_OverSampleRate = Column("DLL_OverSampleRate", SmallInteger)
#     DLL_CodeChangeDelay = Column("DLL_CodeChangeDelay", SmallInteger)
#     DLL_CommandWait = Column("DLL_CommandWait", SmallInteger)
#     DLL_DcdlStart = Column("DLL_DcdlStart", SmallInteger)
#     DLL_DcdlStep = Column("DLL_DcdlStep", SmallInteger)
#     DLL_EnableUpdateLimit = Column("DLL_EnableUpdateLimit", SmallInteger)
#     DLL_UpdateLimit = Column("DLL_UpdateLimit", SmallInteger)
#     MinorMode_iDFTProgram = Column("MinorMode_iDFTProgram", SmallInteger)
#     MinorMode_iBumpReMap_En = Column("MinorMode_iBumpReMap_En", SmallInteger)
#     BumpReMapCS_0 = Column("BumpReMapCS_0", SmallInteger)
#     BumpReMapCS_1 = Column("BumpReMapCS_1", SmallInteger)
#     BumpReMapCS_2 = Column("BumpReMapCS_2", SmallInteger)
#     BumpReMapCS_3 = Column("BumpReMapCS_3", SmallInteger)
#     BumpReMapCA_0 = Column("BumpReMapCA_0", SmallInteger)
#     BumpReMapCA_1 = Column("BumpReMapCA_1", SmallInteger)
#     BumpReMapCA_2 = Column("BumpReMapCA_2", SmallInteger)
#     BumpReMapCA_3 = Column("BumpReMapCA_3", SmallInteger)
#     BumpReMapCA_4 = Column("BumpReMapCA_4", SmallInteger)
#     BumpReMapCA_5 = Column("BumpReMapCA_5", SmallInteger)
#     BumpReMapCK = Column("BumpReMapCK", SmallInteger)
#     BumpReMapDBYTE_0 = Column("BumpReMapDBYTE_0", SmallInteger)
#     BumpReMapDQ0_0 = Column("BumpReMapDQ0_0", SmallInteger)
#     BumpReMapDQ0_1 = Column("BumpReMapDQ0_1", SmallInteger)
#     BumpReMapDQ0_2 = Column("BumpReMapDQ0_2", SmallInteger)
#     BumpReMapDQ0_3 = Column("BumpReMapDQ0_3", SmallInteger)
#     BumpReMapDQ0_4 = Column("BumpReMapDQ0_4", SmallInteger)
#     BumpReMapDQ0_5 = Column("BumpReMapDQ0_5", SmallInteger)
#     BumpReMapDQ0_6 = Column("BumpReMapDQ0_6", SmallInteger)
#     BumpReMapDQ0_7 = Column("BumpReMapDQ0_7", SmallInteger)
#     BumpReMapDMI_0 = Column("BumpReMapDMI_0", SmallInteger)
#     BumpReMapDQS_0 = Column("BumpReMapDQS_0", SmallInteger)
#     BumpReMapWCK_0 = Column("BumpReMapWCK_0", SmallInteger)
#     BumpReMapDBYTE_1 = Column("BumpReMapDBYTE_1", SmallInteger)
#     BumpReMapDQ1_0 = Column("BumpReMapDQ1_0", SmallInteger)
#     BumpReMapDQ1_1 = Column("BumpReMapDQ1_1", SmallInteger)
#     BumpReMapDQ1_2 = Column("BumpReMapDQ1_2", SmallInteger)
#     BumpReMapDQ1_3 = Column("BumpReMapDQ1_3", SmallInteger)
#     BumpReMapDQ1_4 = Column("BumpReMapDQ1_4", SmallInteger)
#     BumpReMapDQ1_5 = Column("BumpReMapDQ1_5", SmallInteger)
#     BumpReMapDQ1_6 = Column("BumpReMapDQ1_6", SmallInteger)
#     BumpReMapDQ1_7 = Column("BumpReMapDQ1_7", SmallInteger)
#     BumpReMapDMI_1 = Column("BumpReMapDMI_1", SmallInteger)
#     BumpReMapDQS_1 = Column("BumpReMapDQS_1", SmallInteger)
#     BumpReMapWCK_1 = Column("BumpReMapWCK_1", SmallInteger)
#     MinorMode_iRetrainGateMode = Column("MinorMode_iRetrainGateMode", SmallInteger)
#     MinorMode_iRxReadGateScheme = Column("MinorMode_iRxReadGateScheme", SmallInteger)
#     MinorMode_iDMITrainMode = Column("MinorMode_iDMITrainMode", SmallInteger)
#     MinorMode_iSARLogicMode = Column("MinorMode_iSARLogicMode", SmallInteger)
#     MinorMode_iProductionTestMode = Column("MinorMode_iProductionTestMode", SmallInteger)
#     MinorMode_iFWModeDebug = Column("MinorMode_iFWModeDebug", SmallInteger)
#     MinorMode_iTxDQVrefTrain = Column("MinorMode_iTxDQVrefTrain", SmallInteger)
#     MinorMode_iRxDQVrefTrain = Column("MinorMode_iRxDQVrefTrain", SmallInteger)
#     MinorMode_iCBTVrefTrain = Column("MinorMode_iCBTVrefTrain", SmallInteger)
#     MinorMode_iClkGatingMode = Column("MinorMode_iClkGatingMode", SmallInteger)
#     csr_RdqsPre = Column("csr_RdqsPre", SmallInteger)
#     csr_WCKMode = Column("csr_WCKMode", SmallInteger)
#     tWCKENL_FS = Column("tWCKENL_FS", SmallInteger)
#     tWCKPRE_Toggle_WR = Column("tWCKPRE_Toggle_WR", SmallInteger)
#     csr_RpstMode = Column("csr_RpstMode", SmallInteger)
#     csr_RECC = Column("csr_RECC", SmallInteger)
#     csr_CKR = Column("csr_CKR", SmallInteger)
#     csr_BkOrg = Column("csr_BkOrg", SmallInteger)
#     csr_WCK_FM = Column("csr_WCK_FM", SmallInteger)
#     tWCKENL_RD = Column("tWCKENL_RD", SmallInteger)
#     csr_WECC = Column("csr_WECC", SmallInteger)
#     csr_CkMode = Column("csr_CkMode", SmallInteger)
#     csr_WCK2DQIIntervalTimerRunTimeSetting = Column("csr_WCK2DQIIntervalTimerRunTimeSetting", SmallInteger)
#     tWCKPST = Column("tWCKPST", SmallInteger)
#     tWCKPRE_Static = Column("tWCKPRE_Static", SmallInteger)
#     csr_RdqsPst = Column("csr_RdqsPst", SmallInteger)
#     tWCKENL_WR = Column("tWCKENL_WR", SmallInteger)
#     BumpReMapCA_6 = Column("BumpReMapCA_6", SmallInteger)
#     tWCKPRE_Toggle_FS = Column("tWCKPRE_Toggle_FS", SmallInteger)
#     csr_WCK2DQOIntervalTimerRunTimeSetting = Column("csr_WCK2DQOIntervalTimerRunTimeSetting", SmallInteger)
#     tWCKPRE_Toggle_RD = Column("tWCKPRE_Toggle_RD", SmallInteger)
#     csr_WckPst = Column("csr_WckPst", SmallInteger)




