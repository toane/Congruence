var nodes = null;
var edges = null;
var network = null;


var get_nodes = new Request.JSON({
        url: '/storm/graph_json_nodes/',
        method: 'get',
        onProgress: function(event, xhr) {
        },
        onSuccess: function(responseJSON, responseText){
            console.log("JSON", responseJSON['nodes'])
            draw(responseJSON['nodes'])
        },
        onError(text, error){
            console.log(text, error)
        }
    });
    get_nodes.send();

function draw(node_data) {
// create people.
// value corresponds with the age of the person
nodes = node_data;
//nodes = [{group:'TOPIC',label:'show',id:'0',color:'rgb( 204, 204, 204)',value:'1'},
//{group:'ORGANIZATION',label:'New York Times',id:'1',color:'rgb(255, 204, 0)',value:'1'},
//{group:'ORGANIZATION',label:'Adelphi',id:'2',color:'rgb(255, 204, 0)',value:'1'},
//{group:'PERSON',label:'Donald Trump',id:'3',color:'rgb( 0, 51, 102)',value:'1'},
//{group:'ORGANIZATION',label:'Forestry Commission',id:'4',color:'rgb(255, 204, 0)',value:'1'},
//{group:'PERSON',label:'Jeff Koons',id:'5',color:'rgb( 0, 51, 102)',value:'1'},
//{group:'TOPIC',label:'time',id:'6',color:'rgb( 204, 204, 204)',value:'1'},
//{group:'TOPIC',label:'art',id:'7',color:'rgb( 204, 204, 204)',value:'1'},
//{group:'TOPIC',label:'work',id:'8',color:'rgb( 204, 204, 204)',value:'1'},
//{group:'PERSON',label:'Joe Paterno',id:'9',color:'rgb( 0, 51, 102)',value:'1'},
//{group:'ORGANIZATION',label:'CNN',id:'10',color:'rgb(255, 204, 0)',value:'1'},
//{group:'PERSON',label:'Christoph Büchel',id:'11',color:'rgb( 0, 51, 102)',value:'1'},
//{group:'ORGANIZATION',label:'Penn State',id:'12',color:'rgb(255, 204, 0)',value:'1'},
//{group:'ORGANIZATION',label:'MAGA',id:'13',color:'rgb(255, 204, 0)',value:'1'},
//{group:'TOPIC',label:'urinal',id:'14',color:'rgb( 204, 204, 204)',value:'1'},
//{group:'PERSON',label:'Jerry Sandusky',id:'15',color:'rgb( 0, 51, 102)',value:'1'},
//{group:'TOPIC',label:'money',id:'16',color:'rgb( 204, 204, 204)',value:'1'},
//{group:'PERSON',label:'John Weber Gallery',id:'17',color:'rgb( 0, 51, 102)',value:'1'}];


// create connections between people
// value corresponds with the amount of contact between two people
edges = [{title:'1',to:'10',from:'2',color:'rgb(100,100,100'},
{title:'1',to:'6',from:'2',color:'rgb(100,100,100'},
{title:'1',to:'14',from:'2',color:'rgb(100,100,100'},
{title:'1',to:'8',from:'4',color:'rgb(100,100,100'},
{title:'1',to:'17',from:'5',color:'rgb(100,100,100'},
{title:'1',to:'10',from:'15',color:'rgb(100,100,100'},
{title:'1',to:'9',from:'15',color:'rgb(100,100,100'},
{title:'1',to:'12',from:'15',color:'rgb(100,100,100'},
{title:'1',to:'6',from:'15',color:'rgb(100,100,100'},
{title:'1',to:'14',from:'1',color:'rgb(100,100,100'},
{title:'1',to:'8',from:'1',color:'rgb(100,100,100'},
{title:'1',to:'6',from:'12',color:'rgb(100,100,100'},
{title:'1',to:'14',from:'12',color:'rgb(100,100,100'},
{title:'1',to:'16',from:'7',color:'rgb(100,100,100'},
{title:'1',to:'0',from:'7',color:'rgb(100,100,100'},
{title:'1',to:'6',from:'7',color:'rgb(100,100,100'},
{title:'1',to:'14',from:'0',color:'rgb(100,100,100'},
{title:'1',to:'8',from:'0',color:'rgb(100,100,100'},
{title:'1',to:'14',from:'6',color:'rgb(100,100,100'},
{title:'1',to:'8',from:'6',color:'rgb(100,100,100'},
{title:'1',to:'8',from:'14',color:'rgb(100,100,100'}];


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