function TestDataGenerato(){
    return ['48.90310714879134934563 38.27950588140924992331', '48.90310714879134934563 38.27950588140924992331']
}

function GetMap()
    {
        var loc = document.getElementById('loc').value.split(' ')


        var data = document.getElementsByClassName('home_point_cor')
        var rc_cor = document.getElementsByClassName('rc_cor')

        var len_home_point = data[data.length -1].innerHTML.split('\n')[1].split(' ')[20]
        var lon_home_point = data[data.length -1].innerHTML.split('\n')[2].split(' ')[20]

        var len_rc = rc_cor[rc_cor.length -1].innerHTML.split('\n')[1].split(' ')[20]
        var lon_rc = rc_cor[rc_cor.length -1].innerHTML.split('\n')[2].split(' ')[20]




        var map = new Microsoft.Maps.Map(document.getElementById('myMap'));

        map.setView({
            mapTypeId: Microsoft.Maps.MapTypeId.aerial,
            center: new Microsoft.Maps.Location(loc[0], loc[1]),
            zoom: 18,

        });



        var locations = [
          { latitude: len_home_point, longitude: lon_home_point, title: 'Home point', text: 'H' },
          { latitude: len_rc, longitude: lon_rc, title: 'RC', text: 'H' },
          { latitude: loc[0], longitude: loc[1], title: 'my_pos', text: 'H' }
          // Add more locations as needed
        ];

        locations.forEach(function(location) {
          var pin = new Microsoft.Maps.Pushpin(new Microsoft.Maps.Location(location.latitude, location.longitude), {
            title: location.title,
            text: location.text
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





