
from . import get_key_list, db_create_engine
from sqlalchemy import and_, or_, MetaData, all_, select   # select, all_, MetaData not used thus far
from sqlalchemy.orm import sessionmaker
from csrStructDB.model import Base, CFG3_LP4_x8, CFG3_LP4_x16, CFG3_LP5_x16, CFG3_LP5_x8, CFG8_LP4_x16, CFG8_LP5_x16, CFG8_LP4_x8, CFG8_LP5_x8, Regression_Folder
import os, logging


# Logging Format
format = "(%(asctime)s) QueryDB:\t%(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

###########################
#  Functions to Query DB  #
###########################

'''
Top Level Functions for Querying DB
'''
def query_csr_db(out_path:str, args:dict):
    
    logging.info('In query')
    engine = db_create_engine()
    logging.info('Engine Created')
    
    logging.info(f'args = {args}')
    logging.info(**args)
    # chosen_baud = db_query(engine=engine, 
    #                 phy_cfg=phy_cfg,
    #                 baud=baud,
    #                 protocol=protocol,
    #                 mode=mode,
    #                 dfi2ckratio=dfi2ckratio,
    #                 output_dir=output_dir)
    return 300

# Function to query
# NOTE: we can create a seperate function that does 'deep' query which includes querying for functional test
def db_query(engine, phy_cfg, baud, protocol, mode, dfi2ckratio, output_dir, wck2ckratio=None, EffectiveRL=None, EffectiveWL=None, csr_WL=None, csr_nWR=None, csr_RL=None, csr_WLS=None, tWDQS_on=None, tWDQS_off=None, csr_BL=None, csr_RPST=None, MinorMode_iActiveRanks=None, csr_DVFSC=None, \
csr_DbiWr=None, csr_DbiRd=None, csr_DMD=None, MinorMode_iClkEnMode=None, MinorMode_iRxTCTrain=None, MinorMode_iCSTEn=None, MinorMode_iRxEnhancedTrainMode=None, MinorMode_iPhyMstr_DRAM_Mode=None):
    
    print(f"phy_cfg: {phy_cfg}")
    print(f"MajorSystemMode: {protocol}")
    print(f"MajorMode: {mode}")
    print(f"Baud: {baud}")
    print(f"dfi2ckratio: {dfi2ckratio}\n")
    
    
    freq_bin = find_bin(baud, protocol)
    print("freq_bin = ", freq_bin)
    if freq_bin:
        pass
    else:
        pass
        # invalid baud
    if protocol == 4:
        db_dfi2ckratio = 0 if dfi2ckratio == 4 else 1
    else:
        db_dfi2ckratio = 0
        
    table = f'CFG{phy_cfg}_LP{protocol}_x{mode}'
    table_obj = Base.metadata.tables[table] # TODO: there's another way of using reflectio in tut
    # print(table)
    print(table_obj)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    ## Primary Paramaters
    query = session.query(table_obj)
    query = _build_primary_query(query, table_obj, baud, freq_bin, protocol, mode, db_dfi2ckratio)
    # print(query)
    primary_results = query.first() # returns None if no result
    # print(primary_results)
    
    ## Secondary Parameters
    # NOTE: might need to use other query method, cause the input is not fixed for secondary parameters
    # NOTE: functionality, <query_level_strip>, reports at which query level - primary, secondary,
    query = _build_subquery(query, table_obj, wck2ckratio=wck2ckratio, EffectiveRL=EffectiveRL, EffectiveWL=EffectiveWL)
    # print(query)
    
    ## Result Selection
    secondary_results = query.order_by(table_obj.c.Baud_Rate).all()
    print(secondary_results[-1])
    # for result in secondary_results:
    #     print(result[2], end=', ')
    select_out = secondary_results[-1]
    
    ## Write out result
    _writeout_struct(select_out, table_obj, phy_cfg, baud, protocol, mode, output_dir)
    
    print(select_out[2])
    return select_out[2]
    
    
    
    # return query.all()


def _writeout_struct(result, table, phy_cfg, baud, protocol, mode, output_dir):
    # get the keys and assign them the values in results
    # get the keys from the table obj
    key_list = table.c.keys()[3:]   # remove 'tid' from key list # NOTE: MAGIC NUMBER
    print(len(key_list))
    
    # Difference between key_list and the list from get_key_lsit() is 'Phy_Cfg'
    agg_list = get_key_list()
    # print(list(set(agg_list) - set(key_list)))
    
    value_list = result[3:] # NOTE: MAGIC NUMBER
    print(len(value_list))
    
    # Internal - csrInitStruct_cfgXX_LPXX_xXX_<true rate>Mbps.txt
    # Customer - csrInitStruct_LPXX_xXX_<requested rate>Mbps.txt
    filename = f"csrInitStruct_cfg{phy_cfg}_LP{protocol}_x{mode}_{result[2]}Mbps.txt" # NOTE: MAGIC NUMBER
    print(f"filename = {filename}")
    
    # for key, value in zip(key_list, value_list):
    #     print(f"{key} = {value}")
        
    # remove None entries
    key_list = table.c.keys()
    result_list = list(result)
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w") as output_file:
        for key, value in zip(key_list, result_list):
            # NOTE: for customers pass, but internally what? Also, do we add that banner?
            if (key == "tid") or (key == "Path") or (key == "Baud_Rate"):
                pass
            elif value is not None:
                output_file.write(f"{key} = {value}\n")
        


def  _build_subquery(query, table, **subkeys):
    for key, val in subkeys.items():
        if val:
            # print(f"{key} = {val}")
            query = query.filter(table.c[key] == val)
    return query

def _build_primary_query(query, table, baud, freq_bin, protocol, mode, db_dfi2ckratio):
    
    query = query.filter(
        and_(
            table.c.MajorSystemMode == protocol,
            table.c.MajorMode == mode,
            table.c.dfi2ckratio == db_dfi2ckratio
        )
    )
    # Range limits are not inclusive, limit results to be less than the upper range limit
    if freq_bin[1] == baud:
        query = query.filter(
            and_(
                table.c.Baud_Rate > freq_bin[0],
                table.c.Baud_Rate < baud - 1     # -1 to be within range
            )
        )
    else:
        query = query.filter(
            or_(
                table.c.Baud_Rate == baud,
                and_(
                    table.c.Baud_Rate > freq_bin[0],
                    table.c.Baud_Rate < baud
                )
            )
        )
    return query
    
        
    

    
def select_entry(result_set, table):
    table_obj = Base.metadata.tables
    key_list = table.c.keys()[1:]   # remove 'tid' from key list
    # print(key_list)
    
    # Difference between key_list and the list from get_key_lsit() is 'Phy_Cfg'
    agg_list = get_key_list()
    # print(list(set(agg_list) - set(key_list)))
    
    for result in result_set:
        print(result[2], end=', ')
        
    # check date inserted
    
    
    # get closest baud_Rate
    
    
    

def find_bin(baud_rate, protocol):
    # global protocol_rate
    print(f"protocol: {protocol}")
    if protocol == 4:
        protocol_rate= 2
        # print("(int(baud_rate) / protocol_rate) = ", (int(baud_rate) / protocol_rate))
        for freq_bin in DB_Handler.freq_bins_lp4:
            # print(freq_bin)
            if freq_bin[0] <= (int(baud_rate) / protocol_rate) <= freq_bin[1]:
                # set freq_bin to be <= baud rate 
                # return (int(freq_bin[0])*protocol_rate, int(freq_bin[1])*protocol_rate)
                return (int(freq_bin[0])*protocol_rate, baud_rate)
                
    elif protocol == 5:
        protocol_rate = 8
        # print("(int(baud_rate) / protocol_rate) = ", (int(baud_rate) / protocol_rate))
        for freq_bin in DB_Handler.freq_bins_lp5:
            # print(freq_bin)
            if freq_bin[0] <= (int(baud_rate) / protocol_rate) <= freq_bin[1]:
                return (int(freq_bin[0])*protocol_rate, baud_rate)
    else:
        # print '\n\033[1;31mProtocol must be LP4 or LP5, LP%s is not allowed\033[0m' % protocol
        print("false protocol")
    return None