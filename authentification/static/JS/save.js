document.addEventListener("DOMContentLoaded", function() {
    
    function updatePointPosition() {
        $.ajax({
            url: 'save',
            type: 'GET',
            success: function(data) {

                
            },
            error: function(xhr, status, error) {
                console.error("Erreur AJAX :", error);
            }
        });
    }
    setInterval(updatePointPosition, 10);
});
