function start_page(){
    var link = window.location.href
    if(link == 'http://127.0.0.1:8000/orders/' || link == 'http://127.0.0.1:8000/main_page' ||
    link== 'http://127.0.0.1:8000/second_orders/'){
        document.getElementById('online_order').style.display = 'none'
        document.getElementById('offline_order').style.display = 'block'
    } else if (link == 'http://85.209.89.166:8001/online_orders/' || link == 'http://85.209.89.166:8001/main_page'
     || link == 'http://85.209.89.166:8001/online_second_orders/'){
       document.getElementById('offline_order').style.display = 'none'
       document.getElementById('online_order').style.display = 'block'
    }
}
start_page()

function update_data_func(){
     var link_online = window.location.href
     if(link_online == 'http://127.0.0.1:8000/online_second_orders/' || 'http://127.0.0.1:8000/online_orders/' ){
        document.getElementById('update_data').style.display = 'blokc'
     } else {
        document.getElementByID('update_data').style.display = 'none'
        }
    }
update_data_func()