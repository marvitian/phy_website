import os
import pandas as pd
from tabulate import tabulate
                
if __name__ == '__main__':
    all_functional_spec = []
    all_functional_mode = []
    all_functional_test = []
    
    phy_cfg = ""
    protocol = ""
    mjr_mode = ""
    baud = ""
    dfi2ckratio = ""
    filenames = []
                
    top_df = pd.DataFrame()
    count=0
    for root, dirs, files in os.walk(".", topdown=False):
        for filename in files:
            # print(filename)
            
            if "CFG" in filename:
                param_parts = filename.split(".log")[0].split("_")
                filenames.append(filename)
                phy_cfg = param_parts[1]
                protocol = param_parts[3]
                mjr_mode = param_parts[5]
                baud = param_parts[7]
                dfi2ckratio = param_parts[9]
                # print(f" FILE: {filename} \n \
                #         \t protocol: {protocol}\n \
                #         \t phy_cfg: {phy_cfg}\n \
                #         \t mode: {mjr_mode}\n \
                #         \t dfi2ckratio: {dfi2ckratio}\n \
                #         \t baud: {baud} \n \
                #       ")
                
                functional_spec = []
                functional_mode = []
                functional_test = []
                
                with open(os.path.join(root, filename), "r") as csr_file:
                    content = csr_file.read()
                    mode = "FUNCTIONAL_SPEC"
                    for line in content.split("\n"):
                        if ("##" in line) or (line == ""):
                            pass
                        elif "#" in line:
                            if "FUNCTIONAL_MODE" in line:
                                mode = "FUNCTIONAL_MODE"                    
                            elif "FUNCTIONAL_TEST" in line:
                                mode = "FUNCTIONAL_TEST"
                            # print(f" -------- {mode} -------- ")
                        else:
                            # print(line.split("=")[0].strip(), end=", ")
                            if mode == "FUNCTIONAL_SPEC":
                                functional_spec.append(line.split("=")[0].strip())
                            elif mode == "FUNCTIONAL_MODE":
                                functional_mode.append(line.split("=")[0].strip())
                            elif mode == "FUNCTIONAL_TEST":
                                functional_test.append(line.split("=")[0].strip())
                            
                # get differences
                functional_mode = list(set(functional_mode) - set(functional_spec))
                functional_test = list(set(functional_test) - set(functional_spec))
                # print("\n")
                
            
                report_path = "report.log"
                with open(report_path, "a") as report_file:
                    report_file.write(f"protocol: {protocol}\n phy_cfg: {phy_cfg}\n mode: {mode}\n dfi2ckratio: {dfi2ckratio}\n baud: {baud} \n\n")
                    
                    N = max(len(functional_spec), len(functional_mode), len(functional_test))
                    functional_spec += [''] * (N - len(functional_spec))
                    functional_mode += [''] * (N - len(functional_mode))
                    functional_test += [''] * (N - len(functional_test))
                    # print(f"N = {N}")

                    df = pd.DataFrame({f'CFG{phy_cfg}_LP{protocol}_x{mjr_mode}_DFI{dfi2ckratio}_SPEC': functional_spec, f'CFG{phy_cfg}_LP{protocol}_x{mjr_mode}_DFI{dfi2ckratio}_MODE': functional_mode, f'CFG{phy_cfg}_LP{protocol}_x{mjr_mode}_DFI{dfi2ckratio}_TEST': functional_test})
                    # print(tabulate(df, headers='keys', tablefmt='psql'))
                    # report_file.write(tabulate(df, headers='keys', tablefmt='psql'))
                    # top_df = top_df.join(df, lsuffix='l', rsuffix='r')
                    # print(df)
                    # print(top_df)
                    if count == 0:
                        top_df = df
                        count+=1
                    else:
                        # print(f" FILE: {filename}")
                        top_df = top_df.join(df, lsuffix=f'l{count}', rsuffix=f'r{count}')
                        count+=1
                    # print(top_df)


        
                
    
    top_df.to_csv(path_or_buf="./report.csv")
    
    # get similarities
    
    spec_columns = []
    mode_columns = []
    test_columns = []
    spec_columns_ser = []
    mode_columns_ser = []
    test_columns_ser = []
    for column in top_df:
        temp = top_df[column].dropna().drop_duplicates()
        if temp.iloc[-1] == "":
            temp.drop(labels=(int(temp.size)-1), inplace=True)
        if "SPEC" in column:
            spec_columns.append(temp.to_list())
            spec_columns_ser.append(temp)
        elif "MODE" in column:
            mode_columns.append(temp.to_list())
            mode_columns_ser.append(temp)
        elif "TEST" in column:
            test_columns.append(temp.to_list())
            test_columns_ser.append(temp)
        print(type(temp))


    import numpy as np
    from functools import reduce
    base_spec_keys = reduce(np.intersect1d, spec_columns)
    base_mode_keys = reduce(np.intersect1d, mode_columns)
    base_test_keys = reduce(np.intersect1d, test_columns)

    print(f"\n{10*'-'} FUNCTIONAL_SPEC {10*'-'} \n {base_spec_keys}")
    print(f"\n{10*'-'} FUNCTIONAL_MODE {10*'-'} \n {base_mode_keys}")
    print(f"\n{10*'-'} FUNCTIONAL_TEST {10*'-'} \n {base_test_keys}")
                
    
    ## Get Differences
    print(f"{10*'#'} DIFFERENCES {10*'#'}")
    # print(f"\n{10*'-'} FUNCTIONAL_SPEC {10*'-'} \n {reduce(pd.Series.compare, spec_columns_ser)}")

    print(len(filenames))
    print(filenames)
    
    print(len(spec_columns))
    print(spec_columns)
    
    for file_idx, filename in enumerate(filenames):
        print(filename)
        print(f"{spec_columns[file_idx]}")
        extra_spec_keys = set(spec_columns[file_idx]) - set(base_spec_keys)
        extra_mode_keys = set(mode_columns[file_idx]) - set(base_mode_keys)
        extra_test_keys = set(test_columns[file_idx]) - set(base_test_keys)
        print(extra_spec_keys)
        print(extra_mode_keys)
        print(extra_test_keys)
        print("")
        
        
        
    
                        
                        
                        
        