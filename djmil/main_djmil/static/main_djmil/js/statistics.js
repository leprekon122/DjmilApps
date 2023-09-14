function show_data(){
    document.getElementById('compare_data_detail').style.display = 'block'
}

// function for quant of drones graph
function whose_drones() {

    var total_val_drones = document.getElementById('total_val_drones').innerHTML


    if (document.getElementById('ally') != null) {
        document.getElementById('our_drones').style.height = ((document.getElementById('ally').innerHTML / 250) * 100) + "px"
        document.getElementById('our_drones').innerHTML = (document.getElementById('ally').innerHTML / total_val_drones) * 100
    } else {
        document.getElementById('our_drones').style.display = "none"
        document.getElementById('type_of_owe_our').style.display = "none"


    }

    if (document.getElementById('fag') != null ) {
        var count  = (document.getElementById('fag').innerHTML / total_val_drones) * 100
        //document.getElementById('enemies_drones').style.height = ((document.getElementById('fag').innerHTML / 250) * 100)  + "px"
        document.getElementById('enemies_drones').style.height =  ((250 / 100)) * count  + "px"
        document.getElementById('enemies_drones').innerHTML = (document.getElementById('fag').innerHTML / total_val_drones) * 100


    } else {
        document.getElementById('enemies_drones').style.display = "none"
    }

    if (document.getElementById('fake_gps') != null ) {
        var count  = (document.getElementById('fake_gps').innerHTML / total_val_drones) * 100
        //document.getElementById('unknown_drones').style.height = ((document.getElementById('fake_gps').innerHTML / 250) * 100) + "px"
        document.getElementById('unknown_drones').style.height = ((250 / 100)) * count  + "px"
        document.getElementById('unknown_drones').innerHTML = (document.getElementById('fake_gps').innerHTML / total_val_drones) * 100
    } else {
        document.getElementById('unknown_drones').style.display = "none"
    }

}
whose_drones()

