document.addEventListener("DOMContentLoaded", function() {
    var Factor = 10;
    var point = document.getElementsByClassName("point")[0];
    var rectangle = document.getElementsByClassName("rectangle")[0];
    var html_x = document.getElementById('x');
    var html_y = document.getElementById('y');
    var acc_x = document.getElementById("acc_x");
    var acc_y = document.getElementById("acc_y");
    var acc_z = document.getElementById("acc_z");
    var height = document.getElementById('dim').getAttribute('data-height');
    var width = document.getElementById('dim').getAttribute('data-width');
    var chart1;
    let acc_X, acc_Y, acc_Z;

    function updatePointPosition() {
        $.ajax({
            url: 'get_point_position',
            type: 'GET',
            success: function(data) {

                updateGravityCenter(data);
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
                    backgroundColor: 'rgba(255, 99, 132, 1)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                            {
                    label: 'Acceleration Y',
                    data: [],
                    backgroundColor: 'rgba(75, 192, 192, 1)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1                  
                },          {
                    label: 'Acceleration Z',
                    data: [],
                    backgroundColor: 'rgba(54, 162, 235, 1)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1   
                }
            ]
            },
            options: {
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

        acc_X.shift();
        acc_Y.shift();
        acc_Z.shift();
        acc_X.push(data.acc_x);
        acc_Y.push(data.acc_y);
        acc_Z.push(data.acc_z)

        chart1.data.datasets[0].data = acc_X
        chart1.data.datasets[1].data = acc_Y
        chart1.data.datasets[2].data = acc_Z
        chart1.update();
    }

    function updateGravityCenter(data){
        var screenWidth = window.innerWidth;
        var screenHeight = window.innerHeight;

        var x = Math.round(Factor * (width / 2) * data.x);
        var y = Math.round(Factor * (height / 2) * data.y);
        html_x.textContent = "X = " + x / Factor;
        html_y.textContent = "Y = " + y / Factor;

        var relativeX = screenWidth / 2 + x;
        var relativeY = screenHeight / 2 - y;

        point.style.left = relativeX + "px";
        point.style.top = relativeY + "px";

        var rect_w = Factor * 100 * width / screenWidth;
        var rect_h = Factor * 100 * height / screenHeight;
        rectangle.style.width = rect_w + "%";
        rectangle.style.height = rect_h + "%";
    }

    initVisualisationAcc();
    setInterval(updatePointPosition, 100);
});
