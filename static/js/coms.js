get_db_status();
get_nlp_status();

var recepdiv = document.id('receptor');
var search_field = document.getElement('#search_form > input');

function backend_call() {
    var search_text = search_field.get('value')
    var myRequest = new Request({
        url: '/search/',
        method: 'get',
        data: {
            'keyword': search_text
        },

        onProgress: function(event, xhr) {
            var loaded = event.loaded,
                total = event.total;
            console.log("responseText", xhr.responseText);
            recepdiv.set('text', xhr.responseText);
        }
    });
    myRequest.send();
}

function get_db_status() {

    var db_status_box = document.getElement('#db_status_box');
    console.log("get_db_status()");
    var myRequest = new Request({
        url: '/get_db_status/',
        method: 'get',

        onProgress: function(event, xhr) {
            var loaded = event.loaded,
                total = event.total;
            console.log("get_db_status: ", xhr.responseText);
//            console.log("get_db_status; ", xhr.responseText.localeCompare("error"));

            if (xhr.responseText.localeCompare("error") == 0) {
                db_status_box.removeClass("alert alert-success");
                db_status_box.addClass("alert alert-info");
                db_status_box.set('text', "db unresponsive");
            } else {
                db_status_box.set('text', "db status ok");
            }

        }
    });
    myRequest.send();
}

function get_nlp_status() {

    var db_status_box = document.getElement('#opennlp_status_box');
    console.log("get_nlp_status()");
    var myRequest = new Request({
        url: '/get_nlp_status/',
        method: 'get',
        onProgress: function(event, xhr) {
            var loaded = event.loaded,
                total = event.total;
            console.log("get_nlp_status: ", xhr.responseText);
            if (xhr.responseText.localeCompare("error") == 0) {
                db_status_box.removeClass("alert alert-success");
                db_status_box.addClass("alert alert-info");
                db_status_box.set('text', "OpenNLP unresponsive");
            } else {
                db_status_box.removeClass("alert alert-info");
                db_status_box.addClass("alert alert-success");
                db_status_box.set('text', "OpenNLP status ok");
            }

        },

    });
    myRequest.send();
}

var read_stream = function() {
    var stream_box = document.getElement('#stream_field');
    var myRequest = new Request({
        url: '/streamed_data/',
        method: 'get',
        onProgress: function(event, xhr) {
//            console.log("read_stream", xhr.responseText);
            stream_box.set('value', xhr.responseText);
//            read_stream();
        },
        onSuccess: function(responseText, responseXML){
            setTimeout(read_stream, 200);
        }
    });
    myRequest.send();
}
//read_stream();

