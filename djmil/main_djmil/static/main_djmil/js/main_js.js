function update_data_func(){
     var link_online = window.location.href
     if(link_online == 'http://127.0.0.1:8000/online_second_orders/' || link_online == 'http://127.0.0.1:8000/combat_orders/' ){
        document.getElementById('update_data').style.display = 'block'
     } else {
        document.getElementById('update_data').style.display = 'none'
        }
    }
update_data_func()




