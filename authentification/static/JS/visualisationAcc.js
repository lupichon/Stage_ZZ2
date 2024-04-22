document.addEventListener("DOMContentLoaded", function() {

    var chart1;

    function updateVisualisation(data){

        var len = data.x.length

        var labels = [];
        for (var i = 0; i < len; i++) 
        {
            labels.push(i.toString());
        }

        chart1.data.labels = labels
        chart1.data.datasets[0].data = data.x
        chart1.data.datasets[1].data = data.y
        chart1.data.datasets[2].data = data.z
        chart1.update();
    }
  
    function getVisualisationData() 
    {
        $.ajax({
            url: 'visu_Acc',
            type: 'GET',
            success: function(data) {
                updateVisualisation(data);
            },
            error: function(xhr, status, error) {
                console.error("Erreur AJAX :", error);
            }
        });
    }

    function initVisualisation() {
        chart1 = new Chart(document.getElementById('chart1').getContext('2d'), {
            type: 'line',
            data: {
                labels: [],
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
    
        getVisualisationData()
    }
    initVisualisation();
});
