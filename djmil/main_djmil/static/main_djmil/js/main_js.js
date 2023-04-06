function update_data_func(){
     var link_online = window.location.href
     if(link_online == 'http://127.0.0.1:8000/online_second_orders/' || 'http://127.0.0.1:8000/online_orders/' ){
        document.getElementById('update_data').style.display = 'block'
     } else {
        document.getElementById('update_data').style.display = 'none'
        }
    }
update_data_func()


function GetMap()
    {
        var len = document.getElementById('len').value
        var lon = document.getElementById('lon').value
        console.log(len, lon)

        var map = new Microsoft.Maps.Map('#myMap');

        map.setView({
            mapTypeId: Microsoft.Maps.MapTypeId.aerial,
            center: new Microsoft.Maps.Location(len, lon),
            zoom: 15
        });
    }

function location_data()
    {
    var data = document.getElementById('position')
    console.log(data)
    }