count = 0
data_1 = null
data_2 = null
data_3 = null
data_4 = null
test = null
test2 = null
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

        var map = new Microsoft.Maps.Map(document.getElementById('myMap', {}));


        //Microsoft.Maps.Events.addHandler(map, 'click', function (e) { set_latitudes_and_longitude(e); })
        Microsoft.Maps.Events.addHandler(map, 'click', function (e) {
        var point = new Microsoft.Maps.Point(e.getX(), e.getY());
        var location = e.target.tryPixelToLocation(point);

        var latitude = location.latitude;
        var longitude = location.longitude;
        count += 1
        if (count % 2 == 1){

            lat1 = location.latitude;
            lon1 = location.longitude;


        } else if (count % 2 == 0){
            lat2 = location.latitude;
            lon2 = location.longitude;

            calculateDistance(lat1, lon1, lat2, lon2)

            }
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




function calculateDistance() {
  const earthRadius = 6371; // Radius of the Earth in kilometers

  const degToRad = (degrees) => {
    return degrees * (Math.PI / 180);
  };

  const dLat = degToRad(lat2 - lat1);
  const dLon = degToRad(lon2 - lon1);

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(degToRad(lat1)) * Math.cos(degToRad(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  const distance = earthRadius * c; // Distance in kilometers
  document.getElementById('distance').value = distance.toFixed(2) + ' ' + 'km'

}


