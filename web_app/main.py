from website import create_app

app = create_app()

@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message))

    return dict(mdebug=print_in_console)

# Only if we run this file, not import, run 
if __name__ == '__main__':
    app.run(debug=True) # debug = true, reruns webserver when we make changes
    
     ########## QUERY ###############
    # from csrStructDB import queryDB
    # my_dict = {'phy_cfg':'3', 'MajorSystemMode': 'LP5', 'MinorMode': '8', 'DFI2CKRatio': '1', 'baud': '3200', 'wck2ckratio': '4'}
    # out_dir = '/home/mohamed/dbWeb/csrStructDB/csrInits'
    # # wck2ckratio=wck2ckratio, EffectiveRL=EffectiveRL, EffectiveWL=EffectiveWL
    # output_baud = queryDB.query_csr_db(out_path=out_dir, args=my_dict)
    # print(output_baud)
    ################################
    