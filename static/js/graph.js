var nodes = null;
var edges = null;
var network = null;
var container = null;
var title_card = null;

window.addEvent('domready', function() {
    container = document.getElementById('mynetwork');
    title_card = document.id('title_card');
});


function get_graph_data() {
//    title_card.dispose(); //faire disparaitre le bloc titre
    title_card.fade('out');
    if(network){
        network.setData({}) //si un graphe est déja la, on le vide
    }
    var search_text = search_field.get('value');
    search_field.set('readonly','true');
    var request = new Request.JSON({

        url: '/launch/',
        method: 'get',
        data: {
            'data': search_text
        },
        onProgress: function(event, xhr) {
            console.log(container)
        },
        onSuccess: function(responseJSON, responseText){
            //cree element my network
            //appeler draw
            search_field.removeProperty('readonly');
            if (responseJSON['nodes'].length > 0) {
               draw(responseJSON['nodes'], responseJSON['edges'])
              }
              else{
                //afficher un message
//               draw([{nodes: [{id: "NO DATA", label: 'No data'}] }] )
              }
        },
        onError(text, error){
            search_field.removeProperty('readonly');
            console.log(text, error)
        }
    })
    request.send();
}



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
    configure: {
            enabled: true,
            showButton: true
    },
    interaction:{
        hoverConnectedEdges: true
    },
    physics: {
        enabled: false,
        "barnesHut": {
            "avoidOverlap": 0.1
           },

    },
    height: "1000px",
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
    params.event = "[original event]";
    console.log('click event, getNodeAt returns: ' + this.getNodeAt(params.pointer.DOM));
});
}