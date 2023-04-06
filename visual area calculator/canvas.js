
const blue = "#76b5c5"
const red = "#ff0000"
const yellow = "#eab676"
const green = "#00FF00"
const purple = "#A020F0"
const fill = "#231e1e"

let measurement_scale = 1

let shape;
let ctx;
let text;
let arr;

let start_y = 150;

// TEMPORARY: used for slider to scale the canvas, eventually the scale should be automatic 
// function scale_slide(input){
//     measurement_scale = input/100;
//     signal();

// }
function prep() {

    arr = [];
    shape = document.getElementById("myCanvas");
    ctx = shape.getContext('2d');
    text = shape.getContext('2d');

    // add starting point
    start = new Shape(20, start_y, 0, 0, "start");
    arr.push(start)

    let box = document.querySelector(".box");

    check_border();


    box.addEventListener("mousemove", updateDisplay, false);
    box.addEventListener("mouseenter", updateDisplay, false);
    box.addEventListener("mouseleave", updateDisplay, false);


}


class Shape {
    x;
    y;
    width;
    height;
    info;

    constructor(x,y,w,h,info){
        this.x = x;
        this.y = y;
        this.width = w;
        this.height = h;
        this.info = info;
    }

}

function rot_rect(x,y,w,h){
    ctx.fillRect(-y,x,-h,w);
}
function rot_line(x,y,w,h){
    ctx.strokeRect(-y,x,-h,w);
}

function rot_text(label, x, y, w, h){
    text.fillText(label, -(y + 2.5*h/4) , (x+w/2));
}


function addShape(w,h,colour,label_given, info){
    prevShape = arr[arr.length - 1]
    // IF (prevShape doesnt exist: (0,0)   )
    newx = prevShape.x + prevShape.width;
    newy = prevShape.y;
    
    newShape = new Shape(newx, newy, w, h, info);
    arr.push(newShape)
    text.save();
    ctx.rotate( 3*Math.PI / 2);
    ctx.fillStyle = colour;
    
    rot_rect(newShape.x, newShape.y, newShape.width, newShape.height);
    ctx.lineWidth = 2;
    ctx.strokeStyle = fill;
    rot_line(newShape.x,newShape.y,newShape.width,newShape.height);
    text.fillStyle = "#000000";
    
    text.font = "12px sans-serif";
    rot_text(label_given, newShape.x, newShape.y, newShape.width, newShape.height);
    text.restore();
    // ****************


}


function clearfunct(){
    ctx.clearRect(0, 0, shape.width, shape.height);
    arr.length = 0; // clear cache of shapes 
    // console.log("we tried to clear")
    prep();
}



function render(){
    let total_wid =0;
    clearfunct();
    // for the lane summary elements 
    for(let i = 0; i < Lane_formatted.length; i++){
        let w = Lane_formatted[i]["units"]*CURRENT_SCENARIO.LANE_WIDTH * measurement_scale;
        let h = CURRENT_SCENARIO.lane_height * measurement_scale;
        let colour = lane_colour[Lane_formatted[i]["Lane Type"]+"_units"];
        // let colour = lane_colour[LaneType[i]+"_units"];
        let label = Lane_formatted[i]["Lane Mapping"];
        let info = Lane_formatted[i];                       // what ever you put here is displayed on mouse hover! any object will work
        addShape(w, h, colour,label, info);
        total_wid += w;
        // console.log(info)
    }



    // for DCAP + ESD CLAMP 
    
    // clamp based on current scenario only

    ctx.fillStyle = "#a0b6eb";
    ctx.fillRect(20, start_y, total_wid, -measurement_scale *CURRENT_SCENARIO.clamp_height);
    ctx.lineWidth = 2;
    ctx.strokeStyle = fill;
    ctx.strokeRect(20, start_y, total_wid, - measurement_scale *CURRENT_SCENARIO.clamp_height);
    text.fillStyle = 'Black';
    ctx.fillText("CLAMP", 20+total_wid/2, start_y- measurement_scale * CURRENT_SCENARIO.clamp_height/2);
    
    // dcap ...
    ctx.fillStyle = "#a0b6eb";
    ctx.fillRect(20, start_y- measurement_scale * CURRENT_SCENARIO.clamp_height, total_wid, -measurement_scale*scaled_dcap )
    ctx.lineWidth = 2;
    ctx.strokeStyle = fill;
    ctx.strokeRect(20, start_y- measurement_scale * CURRENT_SCENARIO.clamp_height, total_wid, -measurement_scale*scaled_dcap );
    text.fillStyle = 'Black';
    ctx.fillText("DCAP", 20+total_wid/2, start_y-measurement_scale *CURRENT_SCENARIO.clamp_height -(measurement_scale*scaled_dcap/2));

    

}






// below is for mouse events:

// DESCRIPTION:     displays info about content bseing hovered with mouse in real time.
function updateDisplay(event) {
    var bounding = shape.getBoundingClientRect();
    var xbound = bounding.left;
    var ybound = bounding.top;

    let mousex = event.pageX - xbound;
    let mousey = event.pageY - ybound;

    // hover-debugging
    // document.getElementById("x").innerText = mousex;
    // document.getElementById("y").innerText = mousey;
    // document.getElementById("window_size").innerText = window.innerWidth;


    document.getElementById("shapehover").innerHTML = '';
    
    if( mousey < (start_y - measurement_scale*(CURRENT_SCENARIO.clamp_height + scaled_dcap))  || mousey > start_y + CURRENT_SCENARIO.lane_height * measurement_scale || mousex < 20 || mousex > arr[arr.length-1].x + arr[arr.length-1].width){
        return;
    }
    if( mousey < start_y - measurement_scale*(CURRENT_SCENARIO.clamp_height) ){
        document.getElementById("shapehover").innerHTML = `<div> DCAP </div> <div>height: ${scaled_dcap.toFixed(3)} &micro;m </div><div>width: ${phy_summary.TOTAL_WIDTH.toFixed(3)} &micro;m </div>`;
        
        return;
    }
    if( mousey < start_y  ){
        document.getElementById("shapehover").innerHTML = `<div> VDDQ CLAMP </div> <div>height: ${CURRENT_SCENARIO.clamp_height} &micro;m </div><div>width: ${phy_summary.TOTAL_WIDTH.toFixed(3)} &micro;m </div>`;
        
        return;
    }

    for(let i = 0 ; i< arr.length; i++){
        if(mousex - (arr[i].x + arr[i].width ) < 0 ){
            for(const property in arr[i].info){
                document.getElementById("shapehover").innerHTML += `<div>${property}: ${arr[i].info[property]}</div>`;
                

            }
            break;
        }
    }
}




function disp_summary(){
    let h = phy_summary.TOTAL_HEIGHT;
    document.getElementById('display_t_height').innerHTML = "Total *PHY height : " + h.toFixed(3) + "  &micro;m";
    
    let w = phy_summary.TOTAL_WIDTH;
    document.getElementById("display_t_width").innerHTML = "Total *PHY width : " + w.toFixed(3) + "  &micro;m";



    document.getElementById("loop").innerHTML = '';
    for (const property in lane_summary_alt) {
        document.getElementById("loop").innerHTML +=`<tr><td>${property} </td> <td style="text-align: right"> ${lane_summary_alt[property]} </td> </tr>`;
    }

    document.getElementById("loop2").innerHTML = '';
    for (const property in CURRENT_SCENARIO){
        if(property == "TYPE"){
            document.getElementById("loop2").innerHTML += `<div>${property}: ${CURRENT_SCENARIO[property]}</div>`
            continue;
        }else{
            document.getElementById("loop2").innerHTML += `<div>${property}: ${CURRENT_SCENARIO[property]} &micro;m</div>`
        }
    }

    let slider = document.getElementById("myRange");


}

function check_border(){
    // if(start_y + CURRENT_SCENARIO.lane_height * measurement_scale > 400 ){
    //     override = start_y + CURRENT_SCENARIO.lane_height; 
    //     console.log(override);
    //     signal();
    
    // }

    if((start_y-measurement_scale *CURRENT_SCENARIO.clamp_height -measurement_scale*scaled_dcap) <= 5 ){
        start_y = start_y + 30
        signal();
    }else if((start_y-measurement_scale *CURRENT_SCENARIO.clamp_height -measurement_scale*scaled_dcap) > 45){
        start_y = start_y - 30
        signal();
    }
}

function show(){
    document.getElementById("hide").classList.toggle('hide');
}


