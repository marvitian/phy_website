'''
Management:
1) Choose a port and setup docker
2) Create a github for the project?
3) Look into github codespaces for setup
'''

'''
WEBSITE
1) Define a csr output path for each user
2) What if someone tries to query while db is being updated



Resources:
Flask:
https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask
Streaming content: https://stackoverflow.com/questions/31830663/how-to-render-template-in-flask-without-using-request-context

WEB DB:
1. Check off same thread
https://stackoverflow.com/questions/50846856/in-flask-sqlalchemy-how-do-i-set-check-same-thread-false-in-config-py


'''




'''
CSR STRUCT DB
Query:
1) Factor in entry commit date in query
2) Add backlog to get coverage on common user requests
3) Before querying, check that the file doesn't exist in output directory and that 1) the files parameters are the same, 2) no modifications were made to firmware (ie. doesn't need to be verified again)

Update:
1) Sanity

Links
1. Adding a column to a table without rerun
https://stackoverflow.com/questions/7300948/add-column-to-sqlalchemy-table#:~:text=go%20to%20the%20terminal%20of,column%20%5BCOLUMN_NAME%5D%20%5BTYPE%5D

2. SQLAlchemy nearset datetime
https://stackoverflow.com/questions/42552696/sqlalchemy-nearest-datetime


'''

#  List of companies and their cfgs
# [mohamed@nitrogen sim]$ libreoffice ../../../../PHYTOP/configuration/sys

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



