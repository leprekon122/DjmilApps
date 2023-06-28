
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

        var map = new Microsoft.Maps.Map(document.getElementById('myMap'));

        var locations = [
          { latitude: len_home_point, longitude: lon_home_point, title: 'Home point', text: 'H' },
          { latitude: len_rc, longitude: lon_rc, title: 'RC', text: 'H' },
        ];

        console.log(len_rc, lon_rc)
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

          map.entities.push(pin);
        });

        //var center = map.getCenter();

        //Create custom Pushpin
        /*var pin = new Microsoft.Maps.Pushpin(center,{
            title: 'home point',
            text: 'H',


        }); */

        //Add the pushpin to the map
        //map.entities.push(pin);


    }





