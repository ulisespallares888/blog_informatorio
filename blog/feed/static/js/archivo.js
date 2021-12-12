
function recargar(){
    $.ajax({
       url: url = $("#Url").attr("{% url 'feed' %}"),
        success: function(data){
            $('#seccionRecargar').html(data);
        }
    });
};

