var nodes = null;
var edges = null;
var network = null;
var container = null;
var title_card = null;

var curlgt = 0;
var prevlgv = 0
var MIN_VALID_GRAPH_LGT = 100;
var LOOP_TIMEOUT = 2000;
var glocount = 0;

window.addEvent('domready', function() {
    container = document.getElementById('mynetwork');
    title_card = document.id('title_card');
});


function launch(optional_keyword) {
    /*
    optional_keyword: pour relancer recherches en cliquant sur une node
    */

//    flush_graph_db(); //on vide la base de donnée de graphe avant de recommencer
    loop_db_graph_check();
    title_card.fade('out');
    if(network){
        network.setData({}) //si un graphe est déja la, on le vide
    }
    var search_text = search_field.get('value');
    if (optional_keyword){
        search_field.setProperty('value',optional_keyword);
        search_text = optional_keyword;
    }
    search_field.set('readonly','true');
    var request = new Request.JSON({
        url: '/launch/',
        method: 'get',
        data: {
            'data': search_text
        },
        onProgress: function(event, xhr) {

        },
        onSuccess: function(responseJSON, responseText){
            //DEVRAIT ETRE DANS loop_db_graph_check()
//            if (responseJSON['nodes'].length > 0) {
//               draw(responseJSON['nodes'], responseJSON['edges']) //ne pas redessiner si cles identiques ?
//                console.log(responseJSON)
//              }
//              else{
//
//              }
        },
        onError(text, error){
            search_field.removeProperty('readonly');
            console.log(text, error)
        }
    });
    request.send();

}

var loop_db_graph_check = function() {
    console.log("loop_db_graph_check(): init");
    var myRequest = new Request.JSON({
        url: '/storm/graph_json_nodes/',
        method: 'get',
        onProgress: function(event, xhr) {

        },
        onSuccess: function(responseJSON, responseText){
            console.log("loop_db_graph_check(): onSuccess", responseText.length, glocount);
            curlgt = responseText.length

            if (responseJSON['nodes'].length > 0) {
               draw(responseJSON['nodes'], responseJSON['edges']) //ne pas redessiner si cles identiques ?
//                console.log(responseJSON)
                glocount++;

              }
              else{

              }
            if (glocount < 10 ){setTimeout(loop_db_graph_check, LOOP_TIMEOUT);} else {
                glocount = 0;
            }
        },
        onError(text, error){
            console.log(text, error);
        }
    });
    myRequest.send();
}

//var flush_graph_db = function() {
//    var myRequest = new Request({
//        url: '/storm/flush_graph_db/',
//        method: 'get',
//        onProgress: function(event, xhr) {
//        },
//        onSuccess: function(responseJSON, responseText){
//            console.log("flush_graph_db(): onSuccess");
//        },
//        onError(text, error){
//            console.log(text, error);
//        }
//    });
//    myRequest.send();
//}




function draw(nodes_data, edges_data) {
// create people.
// value corresponds with the age of the person
nodes = nodes_data;
edges = edges_data

// Instantiate our network object.

var data = {
    nodes: nodes,
    edges: edges
};
var options = {
//    configure: {
//            enabled: true,
//            showButton: true
//    },
    interaction:{
        hoverConnectedEdges: true
    },
    physics: {
        enabled: false,
        "barnesHut": {
            "avoidOverlap": 0.1
           },

    },
    height: "700px",
    edges: {
        smooth:{
            enabled:false
        }
    },
    nodes: {
        font:{
            size:30,
            face: "arial",
            color: "#101010"
        },

        shape: 'box',
        scaling: {
            label: {
                min: 8,
                max: 20
            }
        }
    }
};
network = new vis.Network(container, data, options);


network.on("click", function (params) {
        var nodeId = this.getNodeAt(params.pointer.DOM);
        nodeLabel = nodes_data[nodeId].label;
        console.log('click event, getNodeAt returns: ' + nodeLabel);
        console.log('click event, node id: ' + nodeId);
        launch(nodeLabel); //relance recherche avec le label de la node en mot cle
    });

}