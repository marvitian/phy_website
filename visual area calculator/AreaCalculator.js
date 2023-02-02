// numerical calculations are done here 
// layout_algorithm.js determines what to draw in what order
// canvas.js draws it

// <characteristic variables>
let DDR_STANDARDS;
let PHY_CONFIG;
let MAX_RANKS;
let PHY_width_units;
let scale_factor
let scaled_dcap;
let CURRENT_SCENARIO; 

let override;   


// window on load to initialize after loading
window.onload = function() { 
    DDR_STANDARDS = "LP4";
    PHY_CONFIG = "1x16";
    MAX_RANKS = 1;
    CURRENT_SCENARIO = TSMC_N12;
    scale_factor = 1
    override = 300;
    signal();

}



// definitions
let phy_summary = {
    TOTAL_HEIGHT : null,
    TOTAL_WIDTH : null
}

let lane_units = {
    "LVHSSE_units" : 1, //phy
    "DQS_units" : 2, //phy
    "WCK_units" : 2,  // ddr
    "CK_units" : 2, //phy
    "LVLSSE_units" : 1, // ddr
    "HVLSSE_units" : 1, //phy
    "CLKGEN_units" : 5, //phy
    "ATST_units" : 1, //phy
    "ZCAL_units" : 1, // 1
    "RESETN_units" : 1, // 1

}
let lane_colour = {
    "LVHSSE_units" : "blue", //phy
    "DQS_units" : "blue", //phy        
    "WCK_units" : "blue",  // ddr
    "CK_units" : "green", //phy
    "LVLSSE_units" : "green", // ddr
    "HVLSSE_units" : "yellow", //phy
    "CLKGEN_units" : "purple", //phy
    "ATST_units" : "yellow", //phy
    "ZCAL_units" : "blue", // 1
    "RESETN_units" : "yellow", // 1

}

let lane_summary_alt = {
    "RESETN" : null, // 1
    "ATST" : null, //phy
    "HVLSSE" : null, //phy
    "LVHSSE" : null, //phy
    "LVLSSE" : null, // ddr
    "CK" : null, //phy
    "WCK" : null,  // ddr
    "DQS" : null, //phy
    "CLKGEN" : null, //phy
    "ZCAL" : null, // 1   
}
let lane_summary= {
    "RESETN" : null, // 1
    "ATST" : null, //phy
    "HVLSSE" : null, //phy
    "LVHSSE" : null, //phy
    "LVLSSE" : null, // ddr
    "CK" : null, //phy
    "WCK" : null,  // ddr
    "DQS" : null, //phy
    "CLKGEN" : null, //phy
    "ZCAL" : null, // 1   
}




let TSMC_N12 = {
    TYPE: "TSMC_N12",
    CPP : 0.09,
    LANE_WIDTH : Number(39.6),
    LV2LV_SPACER_WIDTH : 0.9,
    HV2LV_SPACER_WIDTH : 0.9,
    lane_height : 225.216,
    dcap_height : 20.16,
    clamp_height : 36.288,
}
 

let N6_540_LANEWIDTH = {
    TYPE : "n6_540_lanewidth",
    CPP : 0.057,
    LANE_WIDTH : 31.92,
    LV2LV_SPACER_WIDTH : 0.57,
    HV2LV_SPACER_WIDTH : 0.57,
    lane_height : 186.3,
    dcap_height : 25.2,
    clamp_height : 45.3,    
}


let N6_640_LANEWIDTH = {
    TYPE : "n6_640_lanewidth",
    CPP : 0.057,
    LANE_WIDTH : 36.48,
    LV2LV_SPACER_WIDTH : 0.57,
    HV2LV_SPACER_WIDTH : 0.57,
    lane_height : 166.5,
    dcap_height : 21.9,
    clamp_height : 39.6,    
}

let N6_688_LANEWIDTH = {
    TYPE : "n6_640_lanewidth",
    CPP : 0.057,
    LANE_WIDTH : 39.216,
    LV2LV_SPACER_WIDTH : 0.57,
    HV2LV_SPACER_WIDTH : 0.57,
    lane_height : 157.8,
    dcap_height : 20.4,
    clamp_height : 36.9,    
}



// setter functions
// TRIGGERED BY:    main.html onClick()
// TRIGGERS:        signal()
// EFFECTS:         <characteristic variables>
function set_DDR_STANDARD(input){
    DDR_STANDARDS = input;
    signal();
}

function set_PHY_CONFIG(input){
    PHY_CONFIG = input;
    signal();
}

function set_MAX_RANKS(input){
    MAX_RANKS = Number(input);
    signal();
}

function set_scenario(input){
    switch(input){
        case "TSMC_N12":
            CURRENT_SCENARIO = TSMC_N12;
            break;
        case "n6_540_lanewidth":
            CURRENT_SCENARIO = N6_540_LANEWIDTH;
            break;
        case "n6_640_lanewidth":
            CURRENT_SCENARIO = N6_640_LANEWIDTH;
            break;
        case "n6_688_lanewidth":
            CURRENT_SCENARIO = N6_688_LANEWIDTH;
            break;
        default:
            window.alert("Not yet available. please make another selection");
    }
    signal();
}



function set_SCALEABLE(input){
    scale_factor = Number(input);
    // console.log(input)
     signal();
}


// sets every property of 'lane_summary' based on the current state of 'DDR_STANDARD', 'PHY_CONFIG', and 'MAX_RANKS'
// TRIGGERED BY:    update()
// TRIGGERS:        none
// EFFECTS:         lane_summary, PHY_width_units
function set_lane_summary(){
    PHY_width_units = 0;


    // LVHSSE
    if( PHY_CONFIG == "1x32"){
        lane_summary.LVHSSE = 36;
    }else{
        lane_summary.LVHSSE = 18;
    }
    


    


    // DQS

    if(PHY_CONFIG == "1x32"){
        lane_summary.DQS = 4;
    } else {
        lane_summary.DQS = 2;
    }

    

    // WCK
    if(DDR_STANDARDS == "LP4"){
        lane_summary.WCK = 0;
    } else {

        if(PHY_CONFIG == "1x32"){
            lane_summary.WCK = 4;
        } else {
            lane_summary.WCK = 2;
        }
    }


    // CK
    if(PHY_CONFIG == "1x32"){
        lane_summary.CK = 2;
    } else {
        lane_summary.CK = 1;
    }
    
    


    // LVLSSE
    if( DDR_STANDARDS == "LP5"){
        lane_summary.LVLSSE = 7;
    } else {
        lane_summary.LVLSSE = 6 + MAX_RANKS;
    }


    // HVLSSE
    lane_summary.HVLSSE = MAX_RANKS;
    

    // CLKGEN
    lane_summary.CLKGEN = 1;



    // ATST
    lane_summary.ATST = 1;


    // ZCAL 
    lane_summary.ZCAL = 1;


    // RESETN  
    lane_summary.RESETN = 1;


    // handle 2x16
    if (PHY_CONFIG == "2x16"){
        for(const property in lane_summary_alt){
            if(property == "RESETN"){ 
                lane_summary_alt[property] = lane_summary[property]
                continue;
            }
            lane_summary_alt[property] = lane_summary[property] * 2 
        }
        PHY_width_units = lane_summary_alt.LVHSSE + 2*lane_summary_alt.DQS + 2*lane_summary_alt.WCK + 2*lane_summary_alt.CK + lane_summary_alt.LVLSSE + lane_summary_alt.HVLSSE + 5*lane_summary_alt.CLKGEN + lane_summary_alt.ATST + lane_summary_alt.ZCAL + lane_summary_alt.RESETN;
    } else {
        for(const property in lane_summary_alt){
            lane_summary_alt[property] = lane_summary[property]  
        }
        PHY_width_units = lane_summary.LVHSSE + 2*lane_summary.DQS + 2*lane_summary.WCK + 2*lane_summary.CK + lane_summary.LVLSSE + lane_summary.HVLSSE + 5*lane_summary.CLKGEN + lane_summary.ATST + lane_summary.ZCAL + lane_summary.RESETN;
    }
    
    
    // ##################unit calculation########################################### //       
    

}


// ###################      maybe i should put the um calculations here in another function ##################### //

function calculate(){
    let temp_wid = (PHY_width_units * CURRENT_SCENARIO.LANE_WIDTH) + CURRENT_SCENARIO.HV2LV_SPACER_WIDTH + CURRENT_SCENARIO.LV2LV_SPACER_WIDTH;
    scaled_dcap = (scale_factor) * (CURRENT_SCENARIO.dcap_height);
    // SCALABLE_HEIGHT = (scale_factor) * (CURRENT_SCENARIO.dcap_height)
    phy_summary.TOTAL_WIDTH = temp_wid;
    phy_summary.TOTAL_HEIGHT = CURRENT_SCENARIO.lane_height + CURRENT_SCENARIO.clamp_height + scaled_dcap;
    set_measure(override)
    // phy_summary.TOTAL_HEIGHT = CURRENT_SCENARIO.lane_height;
}

function set_measure(override){
    let temp_wid = (PHY_width_units * CURRENT_SCENARIO.LANE_WIDTH) + CURRENT_SCENARIO.HV2LV_SPACER_WIDTH + CURRENT_SCENARIO.LV2LV_SPACER_WIDTH;
    measurement_scale = ((window.innerWidth - 300)/temp_wid);


}


function signal(){
    set_lane_summary();
    calculate();
    disp_summary();
    lane_placement_algo();
    prep();
    render();
    // set_measure();
    console.log(lane_summary)
    console.log(lane_summary_alt)
}