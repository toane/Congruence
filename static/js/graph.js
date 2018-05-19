var nodes = null;
var edges = null;
var network = null;


var get_graph_data = new Request.JSON({
        url: '/storm/graph_json_nodes/',
        method: 'get',
        onProgress: function(event, xhr) {
        },
        onSuccess: function(responseJSON, responseText){
//            console.log("JSON", responseJSON['nodes'], responseJSON['edges'])
            draw(responseJSON['nodes'], responseJSON['edges'])
        },
        onError(text, error){
            console.log(text, error)
        }
    });

get_graph_data.send();

function draw(nodes_data, edges_data) {
// create people.
// value corresponds with the age of the person
nodes = nodes_data;
edges = edges_data

// Instantiate our network object.
var container = document.getElementById('mynetwork');
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
            "avoidOverlap": 0.4
           },

    },
    height: "800px",
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
}