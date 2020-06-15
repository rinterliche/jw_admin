function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function delete_service_occurrence(id) {
    $.ajax({
        type: "DELETE",
        url: "/api/service_ocurrence/" + id + "/",
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            return confirm("Tem certeza que deseja excluir a saída de campo?");
        },
        success: function () {
            alert("Saída de campo excluído com sucesso!");
            location.reload();
        },
        error: function (XMLHttpRequest) {
            alert(XMLHttpRequest.responseText);
        }
    });
}