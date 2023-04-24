# # from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, SmallInteger, ARRAY, Boolean, JSON

# # # Base class that we will extent/ inheret from
# # from sqlalchemy.ext.declarative import declarative_base

# # # session maker will create a session --> we can then do things with our database
# # from sqlalchemy.orm import sessionmaker

# # Base = declarative_base()
# # # Base.prepare(engine, reflect=True)
# # engine = create_engine("sqlite:///test.db", echo=True)
    
# # class User(Base):
# #     __tablename__ = 'user'
# #     id = Column(Integer, primary_key=True)
# #     username = Column(String(50))

# # #see what tables exist in metadata right now
# # print(Base.metadata.sorted_tables)
# # # Out[85]: [Table('user', MetaData(bind=None), Column('id', Integer(), table=<user>, primary_key=True, nullable=False), Column('username', String(length=50), table=<user>), schema=None)]

# # # this will add the organization table/class to the Base's Metadata. This also needs to happen before the Foreign Key reference in OrgPrediction class.
# # Base.metadata.reflect(bind=engine, only=['organization'])

# # # now this class' foreign key will reference organization.id which exists in Base metadata.
# # class OrgPrediction(Base):
# #     __tablename__ = 'org_prediction'
# #     id = Column(Integer, primary_key=True)
# #     company_id = Column(String(255), ForeignKey('organization.id'), nullable=True)
# #     prediction = Column(String(255))

# # # this should pass because the foreign key constraint is met.
# # Base.metadata.create_all(engine)


# import pandas as pd

# pd.set_option("display.max_colwidth", 10000)
# df = pd.read_csv('CONFIG_8303.csv', skiprows=[1])

# # print(list(df.columns.values))
# # print(df.iloc[:2].to_string())

# # [1]
# col_names = df.loc[:,"Path"].to_list()
# # print(df.iloc[:4,0].to_string())
# # print(type(col_names))
# # print(df.loc[:15,"Path"].to_string())
# # print(col_names)
# print("---------------------")

# # [2]
# col_names_split = [ "/".join(path.split("/")[:-2]) for path in col_names ]
# # print(col_names_split)
# unique_parent_dirs = list(dict.fromkeys(col_names_split))
# print(unique_parent_dirs)

# # [3]
# all_entries = []
# top_df_dict = {}
# df_columns = ['Regression_Path', 'Baud_Rate_Min', 'Baud_Rate_Max', 'Phy_Cfg', 'System_Mode']

# # Either this or create the data frame and append to it
# top_df_phy_cfgs = []
# top_df_min_baud_rate = []
# top_df_max_baud_rate = []
# top_df_sys_modes = []
# # other way
# # top_df = pd.DataFrame(columns=df_columns)


# for parent_dir in unique_parent_dirs:
#     entry_list = df[df['Path'].str.contains(parent_dir)]
#     # print("regression_path ", parent_dir)
#     # print("min", entry_list["Baud_Rate"].min())
#     # print("max", entry_list["Baud_Rate"].max())
#     # print("phy_cfg ", entry_list['Phy_Cfg'].iloc[0])    # Just takes the first value assuming that all the entries in the same parent dir have the same cfg
#     # print("sys_mode ", entry_list['MajorSystemMode'].iloc[0])    # Just takes the first value assuming that all the entries in the same parent dir have the same sys mode
    
#     # top_df_dict = {'Regression_Path':parent_dir, 'Baud_Rate_Range': {'min':entry_list["Baud_Rate"].min(), 'max':entry_list["Baud_Rate"].max()}, 'Phy_Cfg':entry_list['Phy_Cfg'].iloc[0], 'System_Mode':entry_list['MajorSystemMode'].iloc[0]}

#     top_df_phy_cfgs.append(entry_list['Phy_Cfg'].iloc[0])
#     top_df_min_baud_rate.append(entry_list["Baud_Rate"].min())
#     top_df_max_baud_rate.append(entry_list["Baud_Rate"].max())
#     top_df_sys_modes.append(entry_list['MajorSystemMode'].iloc[0])

#     # top_df.add({''})
    
#     # print(type(entry_list))
#     # print(entry_list)
#     all_entries.append(entry_list)
    
# # print(all_entries)
# # print("regression_paths = ", unique_parent_dirs)
# print("top_df_phy_cfgs = ", top_df_phy_cfgs)
# print("top_df_min_baud_rate", top_df_min_baud_rate)
# print("top_df_max_baud_rate", top_df_max_baud_rate)
# print("top_df_sys_modes", top_df_sys_modes)
# # print("top_df_dict = ", top_df_dict)
# top_df = pd.DataFrame({'Regression_Path':unique_parent_dirs, 'Baud_Rate_Min':top_df_min_baud_rate, 'Baud_Rate_Max':top_df_max_baud_rate, 'Phy_Cfg':top_df_phy_cfgs, 'System_Mode':top_df_sys_modes}, columns=df_columns)

# print(top_df)


# # -------------------
# # create table




# # --------------------



# import sqlalchemy
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Numeric
# from sqlalchemy.orm import sessionmaker
# import pandas as pd


# # Set up of the engine to connect to the database
# # the urlquote is used for passing the password which might contain special characters such as "/"
# engine = create_engine("sqlite:///testdb.db", echo=False)
# conn = engine.connect()
# Base = declarative_base()

# ### writing to db
# import sqlalchemy
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Numeric, SmallInteger
# from sqlalchemy.orm import sessionmaker
# import pandas as pd

# # Set up of the engine to connect to the database
# # the urlquote is used for passing the password which might contain special characters such as "/"
# engine = create_engine("sqlite:///mydb.db", echo=True)
# conn = engine.connect()
# Base = declarative_base()

# from main import Regression_Folder

# # Set up of the table in db and the file to import
# fileToRead = 'file.csv'
# tableToWriteTo = Regression_Folder.__tablename__

# # The orient='records' is the key of this, it allows to align with the format mentioned in the doc to insert in bulks.
# listToWrite = top_df.to_dict(orient='records')
# print("listToWrite = ", listToWrite)

# metadata = sqlalchemy.schema.MetaData(bind=engine)
# table = sqlalchemy.Table(tableToWriteTo, metadata, autoload=True)

# # Open the session
# Session = sessionmaker(bind=engine)
# session = Session()

# # Inser the dataframe into the database in one bulk
# conn.execute(table.insert(), listToWrite)

# # Commit the changes
# session.commit()

# # Close the session
# session.close()

# # [1] get list of column names
# # get unique parent dir names
# #   split list of column names to have just the parent names
# #   get list of unique values
# # get list of row numbers that have the same parent dir name
# # get top level info: regr_parent_dirs, baud_rate_range, phy_cfg, sys_mode

# # what if I make a csv and feed it into the db 










### ------------------------------- NEW TESTS - WEBSITE BUILT  ------------------------------------------- ###
from queryDB import query_csr_db

my_dict = {'MajorSystemMode': 'LP4', 'MinorMode': '16', 'DFI2CKRatio': '4', 'baud': '1800'}
out_dir = 'TEMP_DIR'
print(**my_dict)
query_csr_db(out_path=out_dir, args=my_dict)


