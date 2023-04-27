let LaneType = [];
let Lane_formatted = [];
let blue_half = [];
let blue_quar = [];

let LaneMapping = [];

// DESCRIPTION:         step one:   arrange the colours (lane types order) arrange clocks,
// DESCRIPTION:         step two:   fill with more structure and make low level decisions (such as where clk, ck, wck, etc. will go)
// TRIGGERED BY:        signal()
// TRIGGERS:            
// EFFECTS:             
function lane_placement_algo(){


    LaneType = [];
    blue_half = [];
    blue_quar = [];
    Lane_formatted = [];

    // ############################STEP ONE############################ //
    // ############################STEP ONE############################ //
    // ############################STEP ONE############################ //
    // ############################STEP ONE############################ //
    // ############################STEP ONE############################ //
    
    LaneType.push("RESETN");
    LaneType.push("ATST");
    // HVLSSE
    for(let i = 0 ; i < lane_summary.HVLSSE; i++){
        LaneType.push("HVLSSE"); 
    }
    // LVLSSE
    for(let i = 0; i< lane_summary.LVLSSE; i++){
        // see math for reasoning 
        if(i == Math.ceil((lane_summary.LVLSSE-lane_summary.HVLSSE)/2) ){
            LaneType.push("CK");
        }
        LaneType.push("LVLSSE");
    }

    
    //lvhsse blue 1st half
    if(lane_summary.LVHSSE < 20){

        for(let i = 0 ; i < (lane_summary.LVHSSE / 2) ; i++ ){
            if(i == Math.ceil(  Math.ceil(lane_summary.LVHSSE / 2) / 2 ) ){
                LaneType.push("DQS");
                blue_half.push("DQS");
                if(lane_summary.WCK != 0){
                    LaneType.push("WCK");
                    blue_half.push("WCK");
                }
            }
            LaneType.push("LVHSSE");
            blue_half.push("LVHSSE");
        }
    } else {
        for(let i = 0 ; i < (lane_summary.LVHSSE / 4) ; i++ ){
            if(i == Math.ceil(lane_summary.LVHSSE / 8) ){
                LaneType.push("DQS");
                blue_quar.push("DQS");
                blue_half.push("DQS");
                if(lane_summary.WCK > 0){
                    LaneType.push("WCK");
                    blue_quar.push("WCK");
                    blue_half.push("WCK");
                }
            }
            LaneType.push("LVHSSE");
            blue_quar.push("LVHSSE");
            blue_half.push("LVHSSE");
        }
        for(let i = blue_quar.length -1; i >=0 ; i--){
            LaneType.push(blue_quar[i]);
            blue_half.push(blue_quar[i]);
        }
    }
        
    //clkgen
    LaneType.push("CLKGEN");

    //blue second half
    // console.log(blue_half);
    for(let i = blue_half.length - 1 ; i >= 0;  i-- ){
        LaneType.push(blue_half[i]);
    }

    //zcal
    LaneType.push("ZCAL");
    
    
    // ############################STEP TWO############################ //
    // ############################STEP TWO############################ //
    // ############################STEP TWO############################ //
    // ############################STEP TWO############################ //
    // ############################STEP TWO############################ //

    LaneMapping = [];




    if(DDR_STANDARDS == "LP4"){
        let count_cs = MAX_RANKS;

        for(let i = 0; i < LaneType.length; i++){
            switch(LaneType[i]){
                case "HVLSSE":
                    LaneMapping.push( "CKE");
                    break;
                case "LVLSSE":
                    if(count_cs > 0 ){
                        LaneMapping.push( "CS");
                        count_cs--;
                    } else {
                        LaneMapping.push( "CA");
                    }
                    break; 
                case "LVHSSE":
                    LaneMapping.push( "DQ");
                    break;
                default:
                    LaneMapping.push( LaneType[i]);
                }
        }

    }   else if (DDR_STANDARDS == "LP5"){

        
        for(let i = 0; i < LaneType.length ; i++ ){
            switch(LaneType[i]){
                case "HVLSSE":
                    LaneMapping.push( "CS");
                    break;
                case "LVLSSE":
                    
                    LaneMapping.push( "CA");
                    
                    break; 
                case "LVHSSE":
                    LaneMapping.push( "DQ");
                    break;
                default:
                    LaneMapping.push( LaneType[i]);
            }
        }
    }   else { 
        let count_cs = MAX_RANKS;

        for(let i = 0; i < LaneType.length; i++ ){
            switch(LaneType[i]){
                case "HVLSSE":
                    LaneMapping.push("CS  /  CKE");
                    break;
                case "LVLSSE":
                    if(count_cs > 1){
                        LaneMapping.push("N/A  /  CS");
                        count_cs--;
                    } else if (count_cs == 1){
                        LaneMapping.push("CA  /  CS");
                        count_cs--;
                    } else {
                        LaneMapping.push("CA");
                    }
                    break; 
                case "LVHSSE":
                    LaneMapping.push( "DQ");
                    break;
                default:
                    LaneMapping.push( LaneType[i]);
            }
        }

    } 

    // this might cause issues ******  looks good , dont remember why i thought this so ill leave this here.... -\_0_-
    for(let i = 0; i< LaneType.length; i++){
        Lane_formatted.push(
            {
            "Lane Type"     : LaneType[i],
            "Lane Mapping"      : LaneMapping[i], 
            "units"     : lane_units[LaneType[i]+"_units"],
            "height"    : CURRENT_SCENARIO.lane_height+ " &micro;m",
            "width"     : (lane_units[LaneType[i]+"_units"] * CURRENT_SCENARIO.LANE_WIDTH).toFixed(3) + " &micro;m"
            }
        );

    }




    // this section will perform the 2x16 transformation....
    let temp_lane_arr = [];
    if(PHY_CONFIG=="2x16"){
        for(let i = LaneType.length-1; i>0 ; i--){
            temp_lane_arr.push(Lane_formatted[i]);
        }
        for(let i = 0 ; i< LaneType.length; i++ ){
            temp_lane_arr.push(Lane_formatted[i]);
        }
        Lane_formatted = temp_lane_arr;
    }


    console.log(Lane_formatted);
    // console.log(Lane_formatted);

    

}