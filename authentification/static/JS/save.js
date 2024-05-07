document.addEventListener("DOMContentLoaded", function() {
    
    function save() {
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
    setInterval(save, 10);
});
