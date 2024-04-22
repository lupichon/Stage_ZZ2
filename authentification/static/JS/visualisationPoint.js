document.addEventListener("DOMContentLoaded", function() {


    var Factor = 10;
    var canvas = document.getElementById('myCanvas');
    var ctx = canvas.getContext('2d');
    var point = document.getElementsByClassName("point")[0];
    
    function drawVisualisationPoint(x, y, color, taille) 
    {
        ctx.beginPath();
        ctx.arc(x, y, taille, 0, 2 * Math.PI, false);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.closePath();
    }

    
    function clearCanvas() 
    {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    function updateVisualisation(data) {
        var screenWidth = window.innerWidth;
        var screenHeight = window.innerHeight;
        if (data.status != 2) 
        {
            var height = data.height;
            var width = data.width;

            var relativeX = screenWidth / 2 + Math.round(data.x * Factor);
            var relativeY = screenHeight / 2 - Math.round(data.y * Factor);

            var x_tail = Factor * width / 2 + Math.round(data.x * Factor);
            var y_tail = Factor * height / 2 - Math.round(data.y * Factor);

            if(data.status == 1)
            {
                var color = 'red';
                var taille = 3;
            }
            else
            {
                var color = 'blue';
                var taille = 5;
            }
            drawVisualisationPoint(x_tail, y_tail, color, taille);

            point.style.left = relativeX + "px";
            point.style.top = relativeY + "px";
        } 
        else 
        {
            clearCanvas();
        }
    }

  
    function getVisualisationData() 
    {
        $.ajax({
            url: 'visu_gravityCenter',
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
        canvas.width = canvasWidth * Factor;
        canvas.height = canvasHeight * Factor;
        setInterval(getVisualisationData, 100);
    }

    initVisualisation();

});
