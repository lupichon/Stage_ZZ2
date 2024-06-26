document.addEventListener("DOMContentLoaded", function() {
    var acc_x = document.getElementById("acc_x");
    var acc_y = document.getElementById("acc_y");
    var acc_z = document.getElementById("acc_z");
    var chart1;
    let acc_X, acc_Y, acc_Z;

    function updatePointAcc() {
        $.ajax({
            url: 'get_Acc',
            type: 'GET',
            success: function(data) {
                updateAcc(data);
            },
            error: function(xhr, status, error) {
                console.error("Erreur AJAX :", error);
            }
        });
    }

    function initVisualisationAcc() {
        acc_X = new Array(60);
        acc_Y = new Array(60);
        acc_Z = new Array(60);
        var labels = [];
        for (var i = 0; i < 60; i++) 
        {
            labels.push(i.toString());
            acc_X[i] = 0;
            acc_Y[i] = 0;
            acc_Z[i] = 0;
        }

        chart1 = new Chart(document.getElementById('chart1').getContext('2d'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Acceleration X',
                    data: [],
                    fill: false,
                    backgroundColor: 'rgba(255, 99, 132, 1)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                            {
                    label: 'Acceleration Y',
                    data: [],
                    fill: false,
                    backgroundColor: 'rgba(75, 192, 192, 1)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1                  
                },          {
                    label: 'Acceleration Z',
                    data: [],
                    fill: false,
                    backgroundColor: 'rgba(54, 162, 235, 1)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1   
                }
            ]
            },
            options: {
                animation: {
                    duration: 5,
                    easing: 'easeInOut',
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'num' 
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Acceleration (m/s²)' 
                        }
                    }
                },
                responsive: true, 
                maintainAspectRatio: false
            }
        });
    }

    function updateAcc(data){

        acc_x.innerHTML = "ACC_X = " + data.acc_x + " m/s<sup>2</sup>";
        acc_y.innerHTML = "ACC_Y = " + data.acc_y + " m/s<sup>2</sup>";
        acc_z.innerHTML = "ACC_Z = " + data.acc_z + " m/s<sup>2</sup>";

        acc_X.pop();
        acc_Y.pop();
        acc_Z.pop();
        acc_X.unshift(data.acc_x);
        acc_Y.unshift(data.acc_y);
        acc_Z.unshift(data.acc_z);

        chart1.data.datasets[0].data = acc_X;
        chart1.data.datasets[1].data = acc_Y;
        chart1.data.datasets[2].data = acc_Z;
        chart1.update();
    }

    initVisualisationAcc();
    setInterval(updatePointAcc, 10);
});
