var nodes;
var edges;
var network;
var keyword;
var container = null;
var title_card = null;

var curlgt = 0;
var prevlgt = 0
var MIN_VALID_GRAPH_LGT = 100;
var LOOP_TIMEOUT = 2000;
var glocount = 0;
var loop_db_graph_running = 0;
var search_field = null;

// window.addEvent('domready', function() {
//     container = document.getElementById('mynetwork');
//     title_card = document.id('title_card');
//     search_field = document.getElement('#search_form > #search_field');
//     draw();
// });

function toggle_spinner(active){
    if (active){
        console.log("spinner active");
        }
    else {
        console.log("spinner inactive");
    }
}



function update_graph(new_nodes, new_edges) {
    existing_nids = nodes.getIds();
    new_nids = new_nodes.map(n=>n.id);
    console.log("updating_graph")
    // remove old nodes

    for (var i = 0; i < existing_nids.length; i++) {
	id = existing_nids[i];
	if (! new_nids.includes(id)) {
	    nodes.remove(id);
	}
    }
    nodes.update(new_nodes);


    existing_eids = edges.getIds();
    new_eids = new_edges.map(n=>n.id);
    for (var id in existing_eids) {
	if (! new_eids.includes(id)) {
	    edges.remove(id);
	}
    }
    edges.update(new_edges);
}

function launch(optional_keyword) {
    /*
    optional_keyword: pour relancer recherches en cliquant sur une node
    */
    toggle_spinner(1);
    //ne lancer la boucle de dessin qu'une seule fois
    if (!loop_db_graph_running){
        loop_db_graph_check();
        loop_db_graph_running = 1;
    }
    
    title_card.fade('out');
    if(network){
        // network.setData({}) //si un graphe est déja la, on le vide
    }
    var search_text = search_field.get('value');
    if (optional_keyword){
        search_field.setProperty('value', optional_keyword);
        search_text = optional_keyword;
    }
    search_field.set('readOnly','true');
    keyword = search_text
    
    var request = new Request.JSON({
        url: '/launch/',
        method: 'get',
        data: {
            'data': search_text
        },
        onProgress: function(event, xhr) {
	    
        },
        onSuccess: function(responseJSON, responseText){
            search_field.removeProperty('readOnly');
	    update_graph(responseJSON['nodes'], responseJSON['edges']);
	    //draw(responseJSON['nodes'], responseJSON['edges'])
        },
        onError(text, error){
            search_field.removeProperty('readOnly');
            console.log(text, error)
        }
    });
    request.send();
}

var loop_db_graph_check = function() {
    console.log("loop_db_graph_check(): init");
    console.log("current_kw : ")
    console.log(keyword)
    var myRequest = new Request.JSON({
        url: '/storm/graph_json_nodes/',
        method: 'get',
	data : {
	    "keyword" : keyword
	},
        onProgress: function(event, xhr) {
            console.log("loop_db_graph_check(): onProgress", curlgt, prevlgt);
        },
        onSuccess: function(responseJSON, responseText){
            curlgt = responseText.length
            console.log("loop_db_graph_check(): onSuccess", curlgt, prevlgt);
            //arrête de redessiner apres 2 graphes de longueur identique
            if (curlgt > MIN_VALID_GRAPH_LGT && curlgt != prevlgt && prevlgt > 0){
		toggle_spinner(0);
		console.log("loop_db_graph_check(): onSuccess:draw", curlgt, prevlgt);
		update_graph(responseJSON['nodes'], responseJSON['edges']);
		// draw(responseJSON['nodes'], responseJSON['edges'])
		search_field.removeProperty('readonly');
            } else {
                //MESSAGE SI PAS DE DONNEES
            }
            console.log("loop_db_graph_check(): loop call");
            setTimeout(loop_db_graph_check, LOOP_TIMEOUT);
            prevlgt = responseText.length;
        },
        onError(text, error){
            console.log(text, error);
        }
    });
    console.log("loop_db_graph_check(): send");
    myRequest.send();
}

function draw() {
    nodes = new vis.DataSet();
    edges = new vis.DataSet();

    nodes.sid = "nnn";
    edges.sid = "eee";
    // Instantiate our network object.
    
    var data = {
	nodes: nodes,
	edges: edges
    };
    var options = {
	configure: {
            enabled: false,
	    filter: "physics",
            showButton: true,
            // container: document.getElementById('config')
	},
	physics: {
	    enabled: true,
	    hierarchicalRepulsion: {
		centralGravity: 0.35,
		springLength: 145,
		springConstant: 0.025,
		nodeDistance: 125,
		damping: 0.12
	    },
	    minVelocity: 0.75,
	    solver: "hierarchicalRepulsion"
	},
	interaction:{
            hoverConnectedEdges: true
	},
	height: "700px",
	edges: {
            smooth:{
		enabled:false
            },
	    color: {inherit:'both' }
	},
	nodes: {
            font:{
		size:30,
		face: "arial",
		color: "#101010"
            },
	    
            shape: 'box',
            scaling: {
		label : {enabled: true},
		min : 5,
		max : 100
            }
	},
    };
    network = new vis.Network(container, data, options);
    network.on("click", function (params) {
        var nodeId = this.getNodeAt(params.pointer.DOM);
        nodeLabel = nodes[nodeId].label;
        console.log('click event, getNodeAt returns: ' + nodeLabel);
        console.log('click event, node id: ' + nodeId);
        launch(nodeLabel); //relance recherche avec le label de la node en mot cle
    });
    
}
container = document.getElementById('mynetwork');
title_card = document.id('title_card');
search_field = document.getElement('#search_form > #search_field');
draw();
