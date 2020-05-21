function delete_service_occurrence(id) {
    $.ajax({
        type: "DELETE",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}"
        },
        url: "{{ HTTP_HOST }}/api/service_ocurrence/" + id + "/",
        data: {
            csrfmiddlewaretoken: "{{ csrf_token }}"
        },
        contentType: 'application/json',
        beforeSend: function () {
            return confirm("Tem certeza que deseja excluir a saída de campo?");
        },
        success: function (data, textStatus) {
            alert("Saída de campo excluído com sucesso!");
            location.reload();
        },
        error: function (XMLHttpRequest) {
            alert(XMLHttpRequest.responseText);
        }
    });
}