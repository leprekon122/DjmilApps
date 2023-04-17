function GetMap()
    {
        var loc = document.getElementById('loc').value.split(' ')

        var len_lon = document.getElementsByClassName('len_lon')


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


