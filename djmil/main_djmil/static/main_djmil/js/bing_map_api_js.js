
function GetMap()
    {

        var data = document.getElementsByClassName('home_point_cor')
        var rc_cor = document.getElementsByClassName('rc_cor')

        var len_home_point = data[data.length -1].innerHTML.split('\n')[1].split(' ')[20]
        var lon_home_point = data[data.length -1].innerHTML.split('\n')[2].split(' ')[20]

        var len_rc = rc_cor[rc_cor.length -1].innerHTML.split('\n')[1].split(' ')[20]
        var lon_rc = rc_cor[rc_cor.length -1].innerHTML.split('\n')[2].split(' ')[20]


        var len_drone = document.getElementsByClassName('drone_len')
        var lon_drone = document.getElementsByClassName('drone_lon')

        var loc_set = []


        var count = 0
        var dist_set = []
        var map = new Microsoft.Maps.Map(document.getElementById('myMap', {}));


        //Microsoft.Maps.Events.addHandler(map, 'click', function (e) { set_latitudes_and_longitude(e); })
        Microsoft.Maps.Events.addHandler(map, 'click', function (e) {
        var point = new Microsoft.Maps.Point(e.getX(), e.getY());
        var location = e.target.tryPixelToLocation(point);

        var latitude = location.latitude;
        var longitude = location.longitude;
        console.log(latitude, longitude)

        document.getElementById('lat_data').value = latitude
        document.getElementById('lon_data').value = longitude



        // Calculate the distance between the two locations using the SpatialMath module



        })

        Microsoft.Maps.loadModule('Microsoft.Maps.DrawingTools', function () {
        var tools = new Microsoft.Maps.DrawingTools(map);
        tools.showDrawingManager(function (manager) {
         });
            });


        var bounds = Microsoft.Maps.LocationRect.fromLocations(new Microsoft.Maps.Location(48.97538, 38.138973), new Microsoft.Maps.Location(48.969433, 38.146511));

        var boundsBorder = new Microsoft.Maps.Polyline([
            bounds.getNorthwest(),
            new Microsoft.Maps.Location(bounds.getNorthwest().latitude, bounds.getSoutheast().longitude),
            bounds.getSoutheast(),
            new Microsoft.Maps.Location(bounds.getSoutheast().latitude, bounds.getNorthwest().longitude),
            bounds.getNorthwest()], { strokeColor: 'yellow', strokeThickness: 5 });



        var locations = [
          { latitude: len_home_point, longitude: lon_home_point, title: 'Home point', text: 'H'},
          { latitude: len_rc, longitude: lon_rc, title: 'RC', text: 'H' },
        ];

        map.setView({
            mapTypeId: Microsoft.Maps.MapTypeId.aerial,
            center: new Microsoft.Maps.Location(len_home_point, lon_home_point),
            zoom: 18,
        });



        for (let item = 0; item < len_drone.length; item++ ){
             let data_1 = len_drone[item].innerText
             let data_2 = lon_drone[item].innerText
             locations.push({ latitude: data_1, longitude: data_2, title: 'drone point_' + item, text: 'H', icon: 'https://www.bingmapsportal.com/Content/images/poi_custom.png'})
             }


        locations.forEach(function(location) {
          var pin = new Microsoft.Maps.Pushpin(new Microsoft.Maps.Location(location.latitude, location.longitude), {
            title: location.title,
            text: location.text,
            icon: location.icon,
          });
          map.entities.push([pin,boundsBorder]);
        });

    }



var btn = 0
var data_cor = []

function set_latitudes_and_longitude(map)
    {
        btn += 1
        var coord_1 = null
        var coord_2 = null
        var coord_3 = null
        var coord_4 = null


        if (btn % 2 == 1){
           coord_1 = (map.location.latitude);
           coord_2 = (map.location.longitude);
           data_cor += [coord_1, coord_2]

           //location_1 = new Microsoft.Maps.Location(coord_1, coord_2);
        } else if(btn % 2 == 0) {
            coord_3 = (map.location.latitude)
            coord_4 = (map.location.longitude)

        }

    }


