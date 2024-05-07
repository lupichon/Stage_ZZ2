document.addEventListener("DOMContentLoaded", function() {

    var Factor = 20;
    var canvas = document.getElementById('myCanvas');
    var ctx = canvas.getContext('2d');
    var slider = document.getElementById("myRange");
    var interval;
    var html_x = document.getElementById('x');
    var html_y = document.getElementById('y');
    var start_stop = document.getElementById('start_stop');
    let coordonnees = new Array(2);
    var first_point = true;

    start_stop.addEventListener('click',function(){
        if(interval)
        {
            clearInterval(interval);
            interval = null;
        }
        else
        {
            interval = setInterval(getVisualisationData, slider.value);
        }
    });

    slider.oninput = function() 
    {
        if(interval)
        {
            clearInterval(interval);
            interval = setInterval(getVisualisationData, this.value);
        }
    } 
    
    function drawVisualisationPoint(x, y, color, taille) 
    {
        ctx.beginPath();
        ctx.arc(x, y, taille, 0, 2 * Math.PI, false);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.closePath();
    }

    function drawLine(x1, y1, x2, y2, color, lineWidth) {
        ctx.beginPath();
        ctx.moveTo(x1, y1);  
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = color;  
        ctx.lineWidth = lineWidth; 
        ctx.stroke();  
        ctx.closePath();
    }
    
    function clearCanvas() 
    {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    function updateVisualisation(data) {
        if (data.status != 2) 
        {
            html_x.textContent = "X = " + data.x.toFixed(2);
            html_y.textContent = "Y = " + data.y.toFixed(2);

            var height = data.height;
            var width = data.width;

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
            if(!first_point)
            {
                drawLine(x_tail, y_tail, coordonnees[0], coordonnees[1], color, taille);
            }
            else
            {
                first_point = false;
            }
            coordonnees[0] = x_tail;
            coordonnees[1] = y_tail;
        } 
        else 
        {
            clearCanvas();
            html_x.textContent = "X = " ;
            html_y.textContent = "Y = " ;
            first_point = true;
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
        interval = setInterval(getVisualisationData, slider.value);
    }


    initVisualisation();

});
