document.addEventListener("DOMContentLoaded", function() {
    function updatePointPosition() {
        $.ajax({
            url: 'get_point_position',
            type: 'GET',
            success: function(data) {
                Factor = 10
                var point = document.getElementsByClassName("point")[0];
                var rectangle = document.getElementsByClassName("rectangle")[0];
                var html_x = document.getElementById('x')
                var html_y = document.getElementById('y')
    
                var screenWidth = window.innerWidth;
                var screenHeight = window.innerHeight;

                var height = document.getElementById('dim').getAttribute('data-height');
                var width = document.getElementById('dim').getAttribute('data-width');
               
                var x = Math.round(Factor*(width/2)*data.x);
                var y = Math.round(Factor*(height/2)*data.y);
                html_x.textContent = "X = " + x/Factor;
                html_y.textContent = "Y = " + -y/Factor;

            
                var relativeX = screenWidth / 2 + x;
                var relativeY = screenHeight / 2 + y;

                console.error(data)
                point.style.left = relativeX + "px";
                point.style.top = relativeY + "px";

                var rect_w = Factor*100*width/screenWidth          //trouver la bonne valeur     
                var rect_h = Factor*100*height/screenHeight        
                rectangle.style.width = rect_w + "%"
                rectangle.style.height = rect_h + "%"
            },
            error: function(xhr, status, error) {
                console.error("Erreur AJAX :", error);
                
            }
        });
    }
    setInterval(updatePointPosition,100); 
});

