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
        var loc = document.getElementById('loc').value.split(' ')

        var len_lon = document.getElementsByClassName('len_lon')


        for(let el = 0; el < len_lon.length; el++){
            console.log(len_lon[el])
        }

        var map = new Microsoft.Maps.Map('#myMap');

        map.setView({
            mapTypeId: Microsoft.Maps.MapTypeId.aerial,
            center: new Microsoft.Maps.Location(loc[0], loc[1]),
            zoom: 18,

        });

        var center = map.getCenter();

        //Create custom Pushpin
        var pin = new Microsoft.Maps.Pushpin(center, {
            title: 'your point',
            text: 'H'
        });

        //Add the pushpin to the map
        map.entities.push(pin);
    }

