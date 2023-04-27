phy_state = {
    "DDR_STANDARDS" : None,
    "PHY_CONFIG" : None,
    "MAX_RANKS" : None
}

CURRENT_SCENARIO = {

}

phy_summary = {
    "T_height" : None,
    "T_width" : None
}

lane_summary = {
    "RESETN" : None,
    "ATST" : None,
    "HVLSSE" : None,
    "LVHSSE" : None,
    "LVLSSE" : None,
    "CK" : None,
    "WCK" : None, 
    "DQS" : None,
    "CLKGEN" : None,
    "ZCAL" : None
}

lane_summary_2x16 = {
    "RESETN" : None,
    "ATST" : None,
    "HVLSSE" : None,
    "LVHSSE" : None,
    "LVLSSE" : None,
    "CK" : None,
    "WCK" : None, 
    "DQS" : None,
    "CLKGEN" : None,
    "ZCAL" : None
}



TSMC_N12 = {
    "TYPE": "TSMC_N12",
    "CPP" : 0.09,
    "LANE_WIDTH" : 39.6,
    "LV2LV_SPACER_WIDTH" : 0.9,
    "HV2LV_SPACER_WIDTH" : 0.9,
    "lane_height" : 225.216,
    "dcap_height" : 20.16,
    "clamp_height" : 36.288
}
 

N6_540_LANEWIDTH = {
    "TYPE" : "n6_540_lanewidth",
    "CPP" : 0.057,
    "LANE_WIDTH" : 31.92,
    "LV2LV_SPACER_WIDTH" : 0.57,
    "HV2LV_SPACER_WIDTH" : 0.57,
    "lane_height" : 186.3,
    "dcap_height" : 25.2,
    "clamp_height" : 45.3,    
}


N6_640_LANEWIDTH = {
    "TYPE" : "n6_640_lanewidth",
    "CPP" : 0.057,
    "LANE_WIDTH" : 36.48,
    "LV2LV_SPACER_WIDTH" : 0.57,
    "HV2LV_SPACER_WIDTH" : 0.57,
    "lane_height" : 166.5,
    "dcap_height" : 21.9,
    "clamp_height" : 39.6,    
}

N6_688_LANEWIDTH = {
    "TYPE" : "n6_640_lanewidth",
    "CPP" : 0.057,
    "LANE_WIDTH" : 39.216,
    "LV2LV_SPACER_WIDTH" : 0.57,
    "HV2LV_SPACER_WIDTH" : 0.57,
    "lane_height" : 157.8,
    "dcap_height" : 20.4,
    "clamp_height" : 36.9,    
}



# sets every property of 'lane_summary' bsaed on the currenct state of:'DDR_STANDARD', 'PHY_CONFIG', and 'MAX_RANKS'
# TRIGGERED BY:         update()
# EFFECTS:              lane_summary, PHY_width_units 
def set_lane_summary():
    # reset phy width for recalc
    PHY_WIDTH_UNITS = 0


    # LVHSSE
    if( phy_state["PHY_CONFIG"] == "1x32"):
        lane_summary["LVHSSE"] = 36
    else:
        lane_summary["LVHSSE"] = 18
    
    # DQS
    if( phy_state["PHY_CONFIG"] == "1x31"):
        lane_summary["DQS"] = 4
    else:
        lane_summary["DQS"] = 2

    #WCK
    if(phy_state["DDR_STANDARDS"] == "LP4"):
        lane_summary["WCK"] = 0
    else:
        if(phy_state["PHY_CONFIG"] == "1x32"):
            lane_summary["WCK"] = 4
        else:
            lane_summary["WCK"] = 2
    
    # CK
    if(phy_state["PHY_CONFIG"] == "1x32"):
        lane_summary["CK"] = 2
    else:
        lane_summary["CK"] = 1
    
    # LVLSSE
    if( phy_state["DDR_STANDARDS"] == "LP5"):
        lane_summary["LVLSSE"] = 7
    else:
        lane_summary["LVLSSE"] = 6 + phy_state["MAX_RANKS"];
    
    # HVLSSE
    lane_summary["HVLSSE"] = phy_state["MAX_RANKS"]
    

    # CLKGEN
    lane_summary["CLKGEN"] = 1



    # ATST
    lane_summary["ATST"] = 1


    # ZCAL 
    lane_summary["ZCAL"] = 1


    # RESETN  
    lane_summary["RESETN"] = 1

    

    # handle 2x16 
    if ( phy_state["PHY_CONFIG"] == "2x16" ):
        for key in lane_summary_2x16.keys():
            if( key == "RESETN"):
                continue
            lane_summary[key] = lane_summary[key] * 2
    

    # unit calculation 
    PHY_WIDTH_UNITS =  lane_summary["LVHSSE"] + 2*lane_summary["DQS"] + 2*lane_summary["WCK"] + 2*lane_summary["CK"] + lane_summary["LVLSSE"] + lane_summary["HVLSSE"] + 5* lane_summary["CLKGEN"] + lane_summary["ATST"] + lane_summary["ZCAL"] + lane_summary["RESETN"]




        






def lane_placement_algo():
    for i in range(lane_summary["HVLSSE"]):
        

