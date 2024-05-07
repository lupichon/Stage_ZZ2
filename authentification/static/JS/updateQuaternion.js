document.addEventListener("DOMContentLoaded", function() {
    function updateQua() {
        $.ajax({
            url: 'get_Qua',
            type: 'GET',
            success: function(data) {
                
            },
            error: function(xhr, status, error) {
                console.error("Erreur AJAX :", error);
            }
        });
    }

    setInterval(updateQua, 10);
});
