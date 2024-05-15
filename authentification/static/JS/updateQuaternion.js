var q0, q1, q2, q3;

document.addEventListener("DOMContentLoaded", function() {
    function updateQua() {
        $.ajax({
            url: 'get_Qua',
            type: 'GET',
            success: function(data) 
            {
                q0 = data.q0;
                q1 = data.q1;
                q2 = data.q2
                q3 = data.q3
            },
            error: function(xhr, status, error) {
                console.error("Erreur AJAX :", error);
            }
        });
    }

    setInterval(updateQua, 10);
});
