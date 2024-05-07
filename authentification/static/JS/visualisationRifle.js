document.addEventListener("DOMContentLoaded", function() {
    
    function getVisualisationRifle() 
    {
        $.ajax({
            url: 'visu_Rifle',
            type: 'GET',
        });
    }

    setInterval(getVisualisationRifle,10);

});
