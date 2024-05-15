document.addEventListener("DOMContentLoaded", function() {

    var Factor = 20;
    var canvas = document.getElementById('myCanvas');
    var ctx = canvas.getContext('2d');
    
    function drawVisualisationPoint(x, y, color, taille, shotID) 
    {
        ctx.beginPath();
        ctx.arc(x, y, taille, 0, 2 * Math.PI, false);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.closePath();

        ctx.fillStyle = 'white';
        ctx.font = '12px';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(shotID,x,y);
    }


    function updateVisualisation(data) 
    {
        var len = data.list_points.length
        var height = canvas.height/Factor;
        var width = canvas.width/Factor;

        for (var i = 0; i < len; i++) 
        {

            var x = Factor * width / 2 + Math.round(data.list_points[len - i - 1][0] * Factor);
            var y = Factor * height / 2 - Math.round(data.list_points[len - i - 1][1] * Factor);
            drawVisualisationPoint(x, y, 'blue', 7, i+1);
        }
    }

  
    function getVisualisationData() 
    {
        $.ajax({
            url: 'visu_sessionGravityCenter',
            type: 'GET',
            success: function(data) {
                updateVisualisation(data);
            },
            error: function(xhr, status, error) {
                console.error("Erreur AJAX :", error);
            }
        });
    }

    function initVisualisation() 
    {
        var dimElement = document.getElementById('dim');
        var canvasHeight = parseInt(dimElement.getAttribute('data-height'));
        var canvasWidth = parseInt(dimElement.getAttribute('data-width'));

        canvas.width = canvasWidth * Factor ;
        canvas.height = canvasHeight * Factor;
        
        getVisualisationData();
    }


    initVisualisation();

});
