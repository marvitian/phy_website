from . import get_key_list, TABLES_DIR
from .model import Base, CFG3_LP4_x8, CFG3_LP4_x16, CFG3_LP5_x16, CFG3_LP5_x8, CFG8_LP4_x16, CFG8_LP5_x16, CFG8_LP4_x8, CFG8_LP5_x8, Regression_Folder
import pandas as pd
import os, pathlib, sys, logging

# Logging Format
format = "(%(asctime)s) UpdateDB: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

############################
#  Functions to Update DB  #
############################


### Top-Level function for updating the database
# @param: paths_file A txt file containing the regression paths to be added. If a path already already exists in the database, it will be skipped.
# @param: engine 
# @param: csv_path Can be a single path or a list of paths to csv files
def update_db(paths_file, db_engine, csv_path=None):
    
    if csv_path:
        
        
        # check path(s) exists
        
        print([ os.path.exists() for path in csv_path ])
        # Check that the CONFIG doesn't already exist in db

        # self.import_csv(csv_path, engine) # NOTE: NO SELF



# TODO: 1) Fix update_db 2) Sanity 3) Update csv methods to take new csvs we wrote

## For inserting into db NOTE: review, is it for inserting cause the output csvs don't have phy_cfg

# TODO: give defualt to csv_folder
## Parameters for inputs csv
    # 1) All keys must have a column
    # 2) First row is headers, second and onwards is the data
    # 3) TODO: CSV NAME
    
def import_csv(csv_path, db_engine, csv_folder):
    # TODO: pre import functions that checks that the passed csv is structured properly
    pd.set_option("display.max_colwidth", 10000)    # TODO: Move to __init__
    df = pd.read_csv(csv_path, skiprows=[1], header=0, index_col=False) # Note
    
    # Unknown keys NOTE:UNTESTED
    if list(set(list(df.columns)) - set(get_key_list())):
        raise Exception(f"Unknown keys: {list(set(list(df.columns)) - set(get_key_list()))}")
    
    # Missing Keys
    # TODO: For future, set default (either add or not add) and have option flag for swapping
    # TODO: Maybe a generate example csv function?
    missing_keys = list(set(get_key_list()) - set(list(df.columns)))
    # if missing_keys:
    #     num_res = 0
    #     res_limit = 3
    #     while num_res < res_limit:
    #         res = input(f"Keys {missing_keys} are missing from csv, do you want to add them? [y,n] ")
    #         if res == "y":
    #             for key in missing_keys:
    #                 df.insert(len(df.columns), key, None)
    #             break
    #         elif res == "n":
    #             sys.exit(f"Keys missing from csv, please make sure the csv has the following keys: {missing_keys}")
    #         else:
    #             print("Invalid Respone, Please input \'y\' for yes or \'n\' for no")
            
    #         if num_res == (res_limit-1):
    #             sys.exit("Too many wrong attempts, exiting.")
    #         else:
    #             num_res+=1
    
    
    # TODO: check that only the first row contains keys
    
    # CSV NAME
    csv_name = os.path.basename(csv_path)
    print(csv_name)
    
    # Sort data by phy_cfg, protocol, and mode
    df.sort_values(by=['Phy_Cfg', 'MajorSystemMode', 'MajorMode'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Save New CSV
    # df.to_csv(os.path.join(TABLES_DIR, f"CONFIG_{csv_name}.csv"))
    tables_to_write = []
    
    phy_cfgs = df.Phy_Cfg.unique()
    for phy_cfg in phy_cfgs:
        temp = df.sort_values(by=['Phy_Cfg'])
        cfg_df = df.loc[df['Phy_Cfg'] == phy_cfg]

        for protocol in cfg_df.MajorSystemMode.unique():
            prot_df = cfg_df.loc[cfg_df['MajorSystemMode'] == protocol]
            
            for mode in prot_df.MajorMode.unique():
                
                print(f"phy_cfg = {phy_cfg} ")
                print(f"protocol = {protocol}")
                print(f"mode = {mode}")
                mode_df = prot_df.loc[prot_df['MajorMode'] == mode]
                table = f"CFG{phy_cfg}_LP{protocol}_x{mode}"
                
                # print("---------------------")
                # tables_to_write.append({f"CFG{phy_cfg}_LP{protocol}_x{mode}" : (mode_df.index.min(), mode_df.index.max())})
                
                # TODO: add exception handling if table doesn't exist
                # # Drop the 'Phy_Cfg' column, the tables are arranged in 
                mode_df.drop(columns=['Phy_Cfg'], inplace=True)
                
                # Update DB
                Base.metadata.create_all(bind=db_engine)
                #   # cfg_df.to_sql(table, con=engine, index=True, index_label='tid', if_exists='append')
                mode_df.to_sql(table, con=db_engine, index=False, if_exists='append')
                
                # Save new data to csv folder mode = 0o666
                new_table_path = os.path.join(TABLES_DIR, f"cfg{phy_cfg}", f"lp{protocol}", f"x{mode}")
                os.makedirs(new_table_path, exist_ok=True)
                mode_df.to_csv(path_or_buf=os.path.join(new_table_path, csv_name))
                
                # get unique paths
                all_paths = mode_df.iloc[0,0]
                tp_dir = pathlib.Path(*pathlib.Path(all_paths).parts[:4]).__str__()

                # unique_paths = []
                # for path in all_paths:
                #     # print(f"tp_dir = {tp_dir}")
                #     if tp_dir not in path:
                #         print(f"NEW TP: {path}")
                #         tp_dir = pathlib.Path(*pathlib.Path(all_paths[0]).parts[:4]).__str__()
                #     else:
                #         # print(f"EXISTS: {path}")
                #         unique_paths.append(path)
                #     # print(" # -------------------------- #")
                # # print(unique_paths)
                
                # config_num = pathlib.Path(csv_path).stem.split("_")[-1]
                # print(config_num)
                
                # TODO: Metadata says no tables
                # https://stackoverflow.com/questions/38883256/with-sqlalchemy-metadata-reflect-how-do-you-get-an-actual-table-object
                # print(table)
                # metadata = MetaData(bind=db_engine)
                # print(metadata.tables)
                
                ## Top Level Table
                # Regression_Folder
                
                # with db_engine.begin() as connection:
                #     connection.execute(tableRow.__table__.insert().
                #                     values([row_to_dict(row) for row in listOfRows]))
                                    
                

