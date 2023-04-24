
from . import get_key_list, db_create_engine, freq_bins_lp4, freq_bins_lp5
from sqlalchemy import and_, or_, MetaData, all_, select, desc   # select, all_, MetaData not used thus far
from sqlalchemy.orm import sessionmaker
from csrStructDB.model import Base, CFG3_LP4_x8, CFG3_LP4_x16, CFG3_LP5_x16, CFG3_LP5_x8, CFG8_LP4_x16, CFG8_LP5_x16, CFG8_LP4_x8, CFG8_LP5_x8, Regression_Folder
import os, logging, traceback


# Logging Format
format = "(%(asctime)s)\t%(message)s"
# format = "(%(asctime)s) QueryDb: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

###########################
#  Functions to Query DB  #
###########################

'''
Top Level Functions for Querying DB

Codes:
Error in parameters - 
Error 
'''
# TODO: Factor in entry commit date
def query_csr_db(out_path:str, args:dict):
    
    logging.info("QueryDB:\t" + 'In query')
    engine = db_create_engine()
    logging.info("QueryDB:\t" + 'Engine Created')
    logging.info("QueryDB:\t" + f'engine = {engine}')
    logging.info("QueryDB:\t" + f'args = {args}')
    
    try:
        phy_cfg = int(args['phy_cfg'])
        protocol = int(args['MajorSystemMode'].split('LP')[-1])
        # NOTE: temp cause we are passing the request as it is
        board_setup = int(args['byte-mode'].split('x')[-1])
        dfi2ckratio = int(args['DFI2CKRatio'])
        baud = int(args['baud'])
        
        del args['phy_cfg']
        del args['MajorSystemMode']
        del args['byte-mode']
        del args['DFI2CKRatio']
        del args['baud']
        
        logging.info("QueryDB:\t" + f'args = {args}')

    except KeyError:
        logging.info("QueryDB:\n" + f'{traceback.print_exc()}')
        raise Exception("Error in parsing args passed")

    
    logging.info('')
    logging.info("QueryDB:\t" + f'phy_cfg = {phy_cfg}')
    logging.info("QueryDB:\t" + f'protocol = {protocol}')
    logging.info("QueryDB:\t" + f'board_setup = {board_setup}')
    logging.info("QueryDB:\t" + f'dfi2ckratio = {dfi2ckratio}')
    logging.info("QueryDB:\t" + f'baud = {baud}')
    
    freq_bin = find_bin(baud, protocol)
    if not freq_bin: # invalid baud
        raise Exception("Baud rate not within valid frequency bins.")
    
    # DB dfi2ckratio is either 0 or 1
    if protocol == 4:
        db_dfi2ckratio = 0 if dfi2ckratio == 4 else 1
    else:
        db_dfi2ckratio = 0
    
    logging.info('')
    logging.info("QueryDB:\t" + f'freq_bin = {freq_bin}')
    logging.info("QueryDB:\t" + f'db_dfi2ckratio = {db_dfi2ckratio}')
    
    # Get app
    table_name = f'CFG{phy_cfg}_LP{protocol}_x{board_setup}'
    table = Base.metadata.tables[table_name] # TODO: there's another way of using reflectio in tut
    logging.info("QueryDB:\t" + f'table = {table}')
    # TODO: Check that the table exists and if it's empty or not, e.g. CFG8_LP5_x8 is empty
    
    # Create Session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    ## Primary Query Paramaters
    query = session.query(table)
    query = _build_primary_query(
        query=query, 
        table=table,
        freq_bin=freq_bin,
        protocol=protocol,
        board_setup=board_setup,
        db_dfi2ckratio=db_dfi2ckratio,
        baud=baud
        )
    primary_result = query.order_by(desc(table.c.Baud_Rate)).first() # TODO: returns None if no result
    
    
    logging.info('')
    if primary_result:
        logging.info("QueryDB:\t" + f'primary_result = {primary_result[0:8]}')
        # Only primary keys required
        if not args:
            logging.info("QueryDB:\t" + f'Only Primary Keys Required')
            logging.info("QueryDB:\t" + f'Writing Struct File with Primary Query')
            _writeout_struct(
            result=primary_result,
            table=table,
            phy_cfg=phy_cfg,
            protocol=protocol,
            board_setup=board_setup,
            baud=baud,
            output_dir=out_path
            )
            ## TODO: Write only necessary keys
            ## TODO: Simulate File
            
            return primary_result[2]
            
        else:
            ## Secondary Query Parameters
            logging.info("QueryDB:\t" + f'Subquery Required')
            query = _build_subquery(query, table, args)
            
            ## Result Selection
            secondary_result = query.order_by(desc(table.c.Baud_Rate)).first() # baud <= desired rate
            logging.info("QueryDB:\t" + f'secondary_result = {secondary_result[0:8]}')
            # TODO: in logging, provide which keys are problematic 
            
            if secondary_result:
                logging.info("QueryDB:\t" + f'Writing Struct File with Secondary Query')
                _writeout_struct(
                    result=secondary_result,
                    table=table,
                    phy_cfg=phy_cfg,
                    protocol=protocol,
                    board_setup=board_setup,
                    baud=baud,
                    output_dir=out_path
                    )
                ## TODO: Write only necessary keys
                ## TODO: Simulate File
                return secondary_result[2]
            else:
                logging.info("QueryDB:\t" + f'No Result Found: Failed at Secondary Query')
                return None
            
    else:
        logging.info("QueryDB:\t" + f'No Result Found: Failed at Primary Query')
        return None
    

'''
Adds main db search parameters to query
'''
def _build_primary_query(query, table, freq_bin, protocol, board_setup, db_dfi2ckratio, baud):
    
    query = query.filter(
        and_(
            table.c.MajorSystemMode == protocol,
            table.c.MajorMode == board_setup,
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

'''
'''
def  _build_subquery(query, table, subkeys):
    # logging.info(f"_build_subquery\t {subkeys.items} = {subkeys.items()}")
    for key, val in subkeys.items():
        if val:
            # logging.info(f"_build_subquery\t {key} = {val}")
            query = query.filter(table.c[key] == int(val)) #NOTE: Assuming all keys except MajorSystemMode and byte-mode will be integers
    return query
    

def find_bin(baud_rate, protocol):
    # global protocol_rate
    if protocol == 4:
        protocol_rate= 2
        for freq_bin in freq_bins_lp4:
            # print(freq_bin)
            if freq_bin[0] <= (int(baud_rate) / protocol_rate) <= freq_bin[1]:
                return (int(freq_bin[0])*protocol_rate, baud_rate)
                
    elif protocol == 5:
        protocol_rate = 8
        for freq_bin in freq_bins_lp5:
            if freq_bin[0] <= (int(baud_rate) / protocol_rate) <= freq_bin[1]:
                return (int(freq_bin[0])*protocol_rate, baud_rate)
    else:
        # print '\n\033[1;31mProtocol must be LP4 or LP5, LP%s is not allowed\033[0m' % protocol
        print("Invalid protocol")
    return None

def _writeout_struct(result, table, phy_cfg, protocol, board_setup, baud, output_dir):
    # get the keys and assign them the values in results
    # get the keys from the table obj
    key_list = table.c.keys()[3:]   # remove 'tid' from key list # NOTE: MAGIC NUMBER
    # print(len(key_list))
    
    # Difference between key_list and the list from get_key_lsit() is 'Phy_Cfg'
    agg_list = get_key_list()
    # print(list(set(agg_list) - set(key_list)))
    
    value_list = result[3:] # NOTE: MAGIC NUMBER
    # print(len(value_list))
    
    # Internal - csrInitStruct_cfgXX_LPXX_xXX_<true rate>Mbps.txt
    # Customer - csrInitStruct_LPXX_xXX_<requested rate>Mbps.txt
    filename = f"csrInitStruct_cfg{phy_cfg}_LP{protocol}_x{board_setup}_{result[2]}Mbps.txt" # NOTE: MAGIC NUMBER
    # print(f"filename = {filename}")
    
    # for key, value in zip(key_list, value_list):
    #     print(f"{key} = {value}")
        
    # remove None entries
    key_list = table.c.keys()
    result_list = list(result)
    
    # TODO: try-except for path
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w") as output_file:
        for key, value in zip(key_list, result_list):
            # NOTE: for customers pass, but internally what? Also, do we add that banner?
            if (key == "tid") or (key == "Path") or (key == "Baud_Rate"):
                pass
            elif value is not None:
                output_file.write(f"{key} = {value}\n")