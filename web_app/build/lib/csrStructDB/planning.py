'''
WEBSITE

Flask:
https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask
Streaming content: https://stackoverflow.com/questions/31830663/how-to-render-template-in-flask-without-using-request-context

JS:


'''




'''
CSR STRUCT DB
'''


# TODO:
# Forbidden baud rates? 2755 --> convertion from freq bin to baud rate range
# Condition to add, user can specify that some keys not be null
# Different phy_cfgs have different keys, different customers have different keys sent/ommitted from them? if so should we then include with each customer a key list
# DB doesn't factor in ch/fsp of data being read

    
# Explore:
# Repitions, first baud, then other params
# For the top level table, would I want the number of entries available within an fsp range for a specified cfg
# Split into tables based on 
    # protocol = Column("Protocol", SmallInteger, nullable=False)    
    # mode = Column("Mode", SmallInteger, nullable=False)
    # phy_cfg = Column("Phy_Cfg", SmallInteger, nullable=False)
    # dfi2ckratio



## NOTE:
# Top level table has the DATE added of top level folder
# We can use select join to join the two tables and query
# Achieve the same result by abstracting out FUNCTIONAL_MODE and FUNCTIONAL_TEST and doing join
# If functional_mode and functional_test not included, we don't join


#post processing













# # Adds to query
#     def _build_subquery(self, query, table, wck2ckratio=None, EffectiveRL=None, EffectiveWL=None, csr_WL=None, csr_nWR=None, csr_RL=None, csr_WLS=None, tWDQS_on=None, tWDQS_off=None, csr_BL=None, csr_RPST=None, MinorMode_iActiveRanks=None, csr_DVFSC=None, \
#     csr_DbiWr=None, csr_DbiRd=None, csr_DMD=None, MinorMode_iClkEnMode=None, MinorMode_iRxTCTrain=None, MinorMode_iCSTEn=None, MinorMode_iRxEnhancedTrainMode=None, MinorMode_iPhyMstr_DRAM_Mode=None):
#         if wck2ckratio:
#             query = query.filter(table.c.wck2ckratio == wck2ckratio)
#         if EffectiveRL:
#             query = query.filter(table.c.EffectiveRL == EffectiveRL)
#         if EffectiveWL:
#             query = query.filter(table.c.EffectiveWL == EffectiveWL)
#         if csr_WL: 
#             query = query.filter(table.c.csr_WL == csr_WL)
#         if csr_nWR: 
#             query = query.filter(table.c.csr_nWR == csr_nWR)
#         if csr_RL: 
#             query = query.filter(table.c.csr_RL == csr_RL)
#         if csr_WLS: 
#             query = query.filter(table.c.csr_WLS == csr_WLS)
#         if tWDQS_on: 
#             query = query.filter(table.c.tWDQS_on == tWDQS_on)
#         if tWDQS_off: 
#             query = query.filter(table.c.tWDQS_off == tWDQS_off)
#         if csr_BL: 
#             query = query.filter(table.c.csr_BL == csr_BL)
#         if csr_RPST: 
#             query = query.filter(table.c.csr_RPST == csr_RPST)
#         if MinorMode_iActiveRanks: 
#             query = query.filter(table.c.MinorMode_iActiveRanks == MinorMode_iActiveRanks)
#         if csr_DVFSC: 
#             query = query.filter(table.c.csr_DVFSC == csr_DVFSC)
#         # Functional Mode
#         if csr_DbiWr: 
#             query = query.filter(table.c.csr_DbiWr == csr_DbiWr)
#         if csr_DbiRd: 
#             query = query.filter(table.c.csr_DbiRd == csr_DbiRd)
#         if csr_DMD: 
#             query = query.filter(table.c.csr_DMD == csr_DMD)
#         if MinorMode_iClkEnMode: 
#             query = query.filter(table.c.MinorMode_iClkEnMode == MinorMode_iClkEnMode)
#         if MinorMode_iRxTCTrain: 
#             query = query.filter(table.c.MinorMode_iRxTCTrain == MinorMode_iRxTCTrain)
#         if MinorMode_iCSTEn: 
#             query = query.filter(table.c.MinorMode_iCSTEn == MinorMode_iCSTEn)
#         if MinorMode_iRxEnhancedTrainMode: 
#             query = query.filter(table.c.MinorMode_iRxEnhancedTrainMode == MinorMode_iRxEnhancedTrainMode)
#         if MinorMode_iPhyMstr_DRAM_Mode: 
#             query = query.filter(table.c.MinorMode_iPhyMstr_DRAM_Mode == MinorMode_iPhyMstr_DRAM_Mode)
        
#         # string = "csr_WL, csr_nWR, csr_RL, csr_WLS, tWDQS_on, tWDQS_off, csr_BL, csr_RPST, MinorMode_iActiveRanks, csr_DVFSC, csr_DbiWr, csr_DbiRd, csr_DMD, MinorMode_iClkEnMode, MinorMode_iRxTCTrain, MinorMode_iCSTEn, MinorMode_iRxEnhancedTrainMode, MinorMode_iPhyMstr_DRAM_Mode"
#         # for key in string.split(", "):
#         #     print(f"if {key}: \n\tquery = query.filter(table.c.{key} == {key})")
        
#         return query