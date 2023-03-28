function start_page(){
    var link = window.location.href
    if(link == 'http://127.0.0.1:8000/orders/' || link == 'http://127.0.0.1:8000/main_page'){
        document.getElementById('online_order').style.display = 'none'
        document.getElementById('offline_order').style.display = 'block'
    } else if (link == 'http://85.209.89.166:8001/online_orders/' || link == 'http://85.209.89.166:8001/main_page'){
       document.getElementById('offline_order').style.display = 'none'
       document.getElementById('online_order').style.display = 'block'
    }
}
start_page()