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

    function updatePointPosition() {
        $.ajax({
            url: 'get_point_position',
            type: 'GET',
            success: function(data) {

                var screenWidth = window.innerWidth;
                var screenHeight = window.innerHeight;

                acc_x.innerHTML = "ACC_X = " + data.acc_x + " m/s<sup>2</sup>";
                acc_y.innerHTML = "ACC_Y = " + data.acc_y + " m/s<sup>2</sup>";
                acc_z.innerHTML = "ACC_Z = " + data.acc_z + " m/s<sup>2</sup>";

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
            },
            error: function(xhr, status, error) {
                console.error("Erreur AJAX :", error);
            }
        });
    }
    
    setInterval(updatePointPosition, 150);
});
