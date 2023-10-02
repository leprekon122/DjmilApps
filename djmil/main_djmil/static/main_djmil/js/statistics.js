function show_data(){
    document.getElementById('compare_data_detail').style.display = 'block'
}

// function for quant of drones graph
function whose_drones() {

    var total_val_drones = document.getElementById('total_val_drones').innerHTML
    var data_1 = []
    var data_2 = []




    if (document.getElementById('ally') != null) {
        data_1.push(Math.round((document.getElementById('ally').innerHTML / total_val_drones) * 100))
        data_2.push('наші')
    }


    if (document.getElementById('fag') != null ) {
        data_1.push(Math.round((document.getElementById('fag').innerHTML / total_val_drones) * 100))
        data_2.push('ворожі')
    }


    if (document.getElementById('fake_gps') != null ) {
        data_1.push(Math.round((document.getElementById('fake_gps').innerHTML / total_val_drones) * 100))
        data_2.push('fake_gps')
    }

    const ctx = document.getElementById('myChart1');

    new Chart(ctx, {
    type: 'polarArea',
    data: {
      labels: data_2,
      datasets: [{
        label: '# of Votes',
        data: data_1,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
      }
    }
  });

}
whose_drones()


function round_diagram(){
      var total_val_drones = document.getElementById('total_val_drones').innerHTML

      // variables for count data to round diagramm
      var mavic_2 = document.getElementById('mavic_2')
      var M_200_v2 = document.getElementById('M_200_v2')
      var Mavic_Mini = document.getElementById('Mavic_Mini')
      var Mavic_Air_2 = document.getElementById('Mavic_Air_2')
      var M300RTK = document.getElementById('M300RTK')
      var mini_2 = document.getElementById('mini_2')
      var air_2s = document.getElementById('air_2s')
      var M30 = document.getElementById('M30')
      var mavic2Enterprise = document.getElementById('mavic2Enterprise')
      var mini_se = document.getElementById('mini_se')
      var mavic_3 = document.getElementById('mavic_3')
      var mini_3_Pro = document.getElementById('mini_3_Pro')
      var Mavic_3T_3E = document.getElementById('Mavic_3T_3E')
      var Mavic_3_Classic = document.getElementById('Mavic_3_Classic')

      // variables for drone names for round diagram
      var mavic_2_title = document.getElementById('mavic_2_title')
      var M_200_v2_title = document.getElementById('M_200_v2_title')
      var Mavic_Mini_title = document.getElementById('Mavic_Mini_title')
      var Mavic_Air_2_title = document.getElementById('Mavic_Air_2_title')
      var M300RTK_title = document.getElementById('M300RTK_title')
      var mini_2_title = document.getElementById('mini_2_title')
      var air_2s_title = document.getElementById('air_2s_title')
      var M30_title = document.getElementById('M30_title')
      var mavic2Enterprise_title = document.getElementById('mavic2Enterprise_title')
      var mini_se_title = document.getElementById('mini_se_title')
      var mavic_3_title = document.getElementById('mavic_3_title')
      var mini_3_Pro_title = document.getElementById('mini_3_Pro_title')
      var Mavic_3T_3E_title = document.getElementById('Mavic_3T_3E_title')
      var Mavic_3_Classic_title = document.getElementById('Mavic_3_Classic_title')


      var data_1 = []
      var data_2 = []
      var drones_data = [mavic_2, M_200_v2, Mavic_Mini, Mavic_Air_2, M300RTK, mini_2, air_2s, M30,mavic2Enterprise,
      mini_se, mavic_3,  mini_3_Pro, Mavic_3T_3E, Mavic_3_Classic]
      var drones_data_title = [mavic_2_title, M_200_v2_title, Mavic_Mini_title, Mavic_Air_2_title, M300RTK_title,
      mini_2_title, air_2s_title, M30_title, mavic2Enterprise_title, mini_se_title, mavic_3_title, mini_3_Pro_title,
      Mavic_3T_3E_title, Mavic_3_Classic_title]

      for (let i = 0;  i < drones_data.length; i++){
        if (drones_data[i] != null){
            data_1.push((drones_data[i].innerHTML / total_val_drones) * 100)
            data_2.push(drones_data_title[i].innerHTML)
            }
      }

      const ctx = document.getElementById('myChart');

      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: data_2,
          datasets: [{
            label: '# of Votes',
            data: data_1,
            borderWidth: 1,
            hoverOffset: 4,
          }]
        },
        options: {
          scales: {

          }
        }
      });

}
round_diagram()


function line_diagram(){

  var day_1 = document.getElementById('day_1').innerHTML
  var day_2 = document.getElementById('day_2').innerHTML
  var day_3 = document.getElementById('day_3').innerHTML
  var day_4 = document.getElementById('day_4').innerHTML
  var day_5 = document.getElementById('day_5').innerHTML
  var day_6 = document.getElementById('day_6').innerHTML
  var day_7 = document.getElementById('day_7').innerHTML

  var day_1_quan = document.getElementById('day_1_quan').innerHTML
  var day_2_quan = document.getElementById('day_2_quan').innerHTML
  var day_3_quan = document.getElementById('day_3_quan').innerHTML
  var day_4_quan = document.getElementById('day_4_quan').innerHTML
  var day_5_quan = document.getElementById('day_5_quan').innerHTML
  var day_6_quan = document.getElementById('day_6_quan').innerHTML
  var day_7_quan = document.getElementById('day_7_quan').innerHTML


  const ctx = document.getElementById('myChart2');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: [day_1, day_2, day_3, day_4, day_5, day_6, day_7],
      datasets: [{
        label: '# of Votes',
        data: [day_1_quan, day_2_quan, day_3_quan, day_4_quan, day_5_quan, day_6_quan, day_7_quan],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

}
line_diagram()
