var state_edit = "not"
var polygons = []
var ready_flag = false
var canvas = document.getElementById("canvas_id")
var selected_polygons = {}
var receipt_img = new Image()

canvas.width = 1660
canvas.height = 600
var ctx_canvas = canvas.getContext("2d")



function getMousePos(canvas, event) {
    var rect = canvas.getBoundingClientRect()
    return {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
    }
}

canvas.addEventListener('click', function(evt) {
        var mousePos = getMousePos(canvas, evt)
        for (var i = 0; i < polygons.length; i++) {
            if(state_edit == "not"){break}
            if(polygons[i].cv_coord1_min < mousePos.y && polygons[i].cv_coord1_max > mousePos.y &&
               polygons[i].cv_coord2_min < mousePos.x && polygons[i].cv_coord2_max > mousePos.x){

                if(selected_polygons[state_edit] == undefined)
                {
                    selected_polygons[state_edit] = []
                }
                var index = selected_polygons[state_edit].indexOf(i)
                if(index == -1){
                    selected_polygons[state_edit].push(i)
                }else{
                    selected_polygons[state_edit].splice(index, 1)
                }
            }
        }
    }, false)



// TODO: juntar todos los callbacks

function rut_callback(){
    if(state_edit == "rut"){
        document.getElementById(state_edit+"_div").style.display = "none"
        state_edit = "not"
    }
    else{
        try {
          document.getElementById(state_edit+"_div").style.display = "none"
        }
        catch(err) {
          console.log("no possible to hide" + state_edit+"_div")
        }
        state_edit = "rut"
        document.getElementById(state_edit+"_div").style.display = "block"
    }
}

function name_callback(){
    if(state_edit == "name"){
        document.getElementById(state_edit+"_div").style.display = "none"
        state_edit = "not"
    }
    else{
        try {
          document.getElementById(state_edit+"_div").style.display = "none"
        }
        catch(err) {
          console.log("no possible to hide" + state_edit+"_div")
        }
        state_edit = "name"
        document.getElementById(state_edit+"_div").style.display = "block"
    }
}

function total_amount_callback(){
    if(state_edit == "total_amount"){
        document.getElementById(state_edit+"_div").style.display = "none"
        state_edit = "not"
    }
    else{
        try {
          document.getElementById(state_edit+"_div").style.display = "none"
        }
        catch(err) {
          console.log("no possible to hide" + state_edit+"_div")
        }
        state_edit = "total_amount"
        document.getElementById(state_edit+"_div").style.display = "block"
    }
}

function image_is_ready(){
    ready_flag = true
}

function get_polygons() {
    receipt_img.onload = image_is_ready
    receipt_img.src = "/see_receipt/"+$( "#receiptid" ).text()
    $.getJSON("/get_polygons/" +$( "#receiptid" ).text() , function (data, status) {
        polygons = data
    })
}

function draw_image(){

    canvas.width = receipt_img.width
    canvas.height = receipt_img.height
    if(ready_flag){
        ctx_canvas.drawImage(receipt_img, 0, 0)
    }

    if(selected_polygons[state_edit] == undefined){setTimeout(function(){ draw_image() }, 100); return ;}
        if(state_edit != "not"){
        for (var i = 0; i < selected_polygons[state_edit].length; i++) {
            it = selected_polygons[state_edit][i]
            var coord_1_delta = polygons[it].cv_coord1_max-polygons[it].cv_coord1_min
            var coord_2_delta = polygons[it].cv_coord2_max-polygons[it].cv_coord2_min
            ctx_canvas.rect(polygons[it].cv_coord2_min, polygons[it].cv_coord1_min, coord_2_delta, coord_1_delta)
            ctx_canvas.strokeStyle = "#11aa22"
            ctx_canvas.lineWidth   = 4
            ctx_canvas.stroke()
        }
    }
    setTimeout(function(){ draw_image() }, 100)
}


function process_total_amount(){
    encoded_selected_polygons = ""
    for (var i = 0; i < selected_polygons[state_edit].length; i++) {
        it = selected_polygons[state_edit][i]
        encoded_selected_polygons += String(it) + "T"
    }
    console.log(encoded_selected_polygons)
    $.getJSON("/extract_area_info/" + state_edit + "/" + $( "#receiptid" ).text() + "/" + encoded_selected_polygons, function (data, status) {

        document.getElementById("total_amount_ia").innerHTML = "total_amount: "+ data["result"]
        console.log(data)
    })
}


setTimeout(function(){ draw_image() }, 100)
document.addEventListener("DOMContentLoaded", get_polygons(), false)
