document.addEventListener("DOMContentLoaded", function() {
    var Factor = 20;
    var screenWidth = window.innerWidth;
    var screenHeight = window.innerHeight;
    var point = document.getElementsByClassName("point")[0];
    var rectangle = document.getElementsByClassName("rectangle")[0];
    var sessionInfo = document.getElementById('session-info');
    var clearButton = document.getElementById('clearButton');
    var html_x = document.getElementById('x');
    var html_y = document.getElementById('y');
    var height = document.getElementById('dim').getAttribute('data-height');
    var width = document.getElementById('dim').getAttribute('data-width');
    var container = document.querySelector('.container-login100');
    var pointsArray = [];

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

    function resizing()
    {
        if(screenHeight != window.innerHeight || screenWidth != window.innerWidth)
        {
            for (var i = 0; i < pointsArray.length; i++)
            {
                var pointStyle = window.getComputedStyle(pointsArray[i]);
                var currentLeft = parseFloat(pointStyle.left);
                var currentTop = parseFloat(pointStyle.top);
                pointsArray[i].style.left = (currentLeft - screenWidth / 2 + window.innerWidth / 2) + "px";
                pointsArray[i].style.top = (currentTop - screenHeight / 2 + window.innerHeight / 2) + "px";
            }
            screenHeight = window.innerHeight;
            screenWidth = window.innerWidth;
        }
    }

    function displayNewPoint(relativeX, relativeY, shotID)
    {
        var newPoint = document.createElement('div');
        newPoint.className = 'point';
        newPoint.style.backgroundColor = 'blue';
        newPoint.style.left = relativeX + "px";
        newPoint.style.top = relativeY + "px";

        var text = document.createElement('span');
        text.className = 'textPoint';
        text.textContent = shotID-1;
        
        newPoint.appendChild(text);       

        container.insertBefore(newPoint,container.firstChild);
        
        var highestZIndex = Math.max(...pointsArray.map(point => parseInt(point.style.zIndex) || 0));
        newPoint.style.zIndex = highestZIndex + 1;

        pointsArray.push(newPoint);
    }

    function displayCurrentPoint(relativeX, relativeY)
    {
        point.style.backgroundColor = "red";
        point.style.left = relativeX + "px";
        point.style.top = relativeY + "px";
    }

    function displayRect()
    {
        var rect_w = Factor * 100 * width / screenWidth;
        var rect_h = Factor * 100 * height / screenHeight;
        rectangle.style.width = rect_w + "%";
        rectangle.style.height = rect_h + "%";
    }

    function updateGravityCenter(data)
    {
        sessionInfo.innerHTML = "Session ID : " + data.sessionID + "<br><br> shot number " + data.shotID;

        resizing();
        
        var x = Math.round(Factor * (width / 2) * data.x);
        var y = Math.round(Factor * (height / 2) * data.y);
        html_x.textContent = "X = " + x / Factor;
        html_y.textContent = "Y = " + y / Factor;
        
        var relativeX = screenWidth / 2 + x;
        var relativeY = screenHeight / 2 - y;

        if(data.CoG == 1)
        {
            displayNewPoint(relativeX, relativeY, data.shotID);
        }
        
        displayCurrentPoint(relativeX, relativeY);

        displayRect();
    }

    function clearNewPoint()
    {
        pointsArray.forEach(function(point)
        {
            point.parentNode.removeChild(point);
        });
        pointsArray.splice(0, pointsArray.length);
    }

    clearButton.addEventListener('click',clearNewPoint);
    point.style.zIndex = "9999";
    setInterval(updatePointPosition, 50);
});
