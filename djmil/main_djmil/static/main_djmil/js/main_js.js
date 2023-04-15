function update_data_func(){
     var link_online = window.location.href
     if(link_online == 'http://127.0.0.1:8000/online_second_orders/' || link_online == 'http://127.0.0.1:8000/combat_orders/' ){
        document.getElementById('update_data').style.display = 'block'
     } else {
        document.getElementById('update_data').style.display = 'none'
        }
    }
update_data_func()

function hide_main_search(){
        document.getElementById('main_search').style.display = 'none'
        document.getElementById('hide').style.display = 'none'
        document.getElementById('show').style.display = 'block'
        document.getElementById('show').style.display = 'flex'
        document.getElementById('show').style.justifyContent = 'end'
        document.getElementById('show').style.color = 'green'

}


function show_main_search(){
        document.getElementById('main_search').style.display = 'block'
        document.getElementById('hide').style.display = 'block'
        document.getElementById('show').style.display = 'none'
        document.getElementById('hide').style.display = 'flex'
        document.getElementById('hide').style.justifyContent = 'end'
        document.getElementById('hide').style.color = 'red'
}




function hide_build_orders_all(){
        document.getElementById('build_orders').style.display = 'none'
        document.getElementById('hide_build_orders_all').style.display = 'none'
        document.getElementById('show_build_orders_all').style.display = 'block'
        document.getElementById('show_build_orders_all').style.display = 'flex'
        document.getElementById('show_build_orders_all').style.justifyContent = 'end'
        document.getElementById('show_build_orders_all').style.color = 'green'

}

function show_build_orders_all(){
        document.getElementById('build_orders').style.display = 'block'
        document.getElementById('hide_build_orders_all').style.display = 'block'
        document.getElementById('show_build_orders_all').style.display = 'none'
        document.getElementById('hide_build_orders_all').style.display = 'flex'
        document.getElementById('hide_build_orders_all').style.justifyContent = 'end'
        document.getElementById('hide_build_orders_all').style.justifyContent = 'red'

}

