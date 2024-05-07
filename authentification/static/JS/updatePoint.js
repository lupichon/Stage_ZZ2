document.addEventListener("DOMContentLoaded", function() {
    var Factor = 20;
    var point = document.getElementsByClassName("point")[0];
    var rectangle = document.getElementsByClassName("rectangle")[0];
    var sessionInfo = document.getElementById('session-info');
    var html_x = document.getElementById('x');
    var html_y = document.getElementById('y');
    var height = document.getElementById('dim').getAttribute('data-height');
    var width = document.getElementById('dim').getAttribute('data-width');

    function updatePointPosition() {
        $.ajax({
            url: 'get_point_position',
            type: 'GET',
            success: function(data) {

                updateGravityCenter(data);
            },
            error: function(xhr, status, error) {
                console.error("Erreur AJAX :", error);
            }
        });
    }

    function updateGravityCenter(data){
        sessionInfo.innerHTML = "Session ID : " + data.sessionID + "<br><br> shot number " + data.shotID;

        var screenWidth = window.innerWidth;
        var screenHeight = window.innerHeight;

        var x = Math.round(Factor * (width / 2) * data.x);
        var y = Math.round(Factor * (height / 2) * data.y);
        html_x.textContent = "X = " + x / Factor;
        html_y.textContent = "Y = " + y / Factor;

        var relativeX = screenWidth / 2 + x;
        var relativeY = screenHeight / 2 - y;

        if(data.CoG == 1)
        {
            point.style.backgroundColor = "blue";
        }
        else
        {
            point.style.backgroundColor = "red";
        }
        point.style.left = relativeX + "px";
        point.style.top = relativeY + "px";

        var rect_w = Factor * 100 * width / screenWidth;
        var rect_h = Factor * 100 * height / screenHeight;
        rectangle.style.width = rect_w + "%";
        rectangle.style.height = rect_h + "%";
    }

    setInterval(updatePointPosition, 50);
});
