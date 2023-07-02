var count = 0
function show_filter_panel(){
    count += 1
    if (count % 2 == 1){
        console.log(count)

        document.getElementById('orders_search').style.display = 'block'
        document.getElementById('orders_search').style.height = '70vh'
    } else {
        console.log(count)
        document.getElementById('orders_search').style.display = 'none'
    }
}