var radius = 4;
var weight = 3;

//
function style_station(feature,bool) {
  return {
  color : feature.properties.color,
  fillOpacity : 1 ,
  radius : radius*(1+0.5*bool),
  fillColor : "#ffffff",
  weight : 1 ,
};
}
function style_line(feature,bool) {
  return {color : feature.properties.route_color,
    weight : weight*(1+0.5*bool),
  };
}
function style(feature) {
  switch (feature.geometry.type){
    case "Point" : return style_station(feature,0);
    case "MultiLineString" : return style_line(feature,0);
  };
}

function highlight(feature) {
  switch (feature.geometry.type){
    case "MultiLineString" : return style_line(feature,1);
    case "Point" : return style_station(feature,1);
  };
}

function On_Each_Feature(feature, layer) {
    layer.on({
        mouseout: function(e) {
            plotted_traject.resetStyle(e.target);
        },
        mouseover: function(e) {
            e.target.setStyle(highlight(e.target.feature));
        },
    });
}

function point_to_circle (feature,latlng) {
  return  L.circleMarker(latlng,radius);
}

function add_data(data){
  plotted_traject.addData(data);
}

function table_fill (fields,aliases,layer,handleObject){
  return '<table>' +
      String(
      fields.map(
      (v,i)=>
      `<tr>
          <th>${aliases[i].toLocaleString()}</th>
          <td>${handleObject(layer.feature.properties[v]).toLocaleString()}</td>
      </tr>`).join(''))
  +'</table>';
}


function tool_tip(layer){
  let div = L.DomUtil.create('div');
  let handleObject = feature=>typeof(feature)=='object' ? JSON.stringify(feature) : feature;

  let fields = ["route_name"];

  let aliases_stations = ["Station"];
  let aliases_lines = ["Ligne"];

  let table ;
  switch(layer.feature.geometry.type){
    case "Point" :
      table = table_fill(fields,aliases_stations,layer,handleObject);
      break;
    case "MultiLineString" :
      table = table_fill(fields,aliases_lines,layer,handleObject);
      break;
  }
  div.innerHTML=table;
  return div
}


function pop_up(layer){
  let div = L.DomUtil.create('div');

  let handleObject = feature=>(typeof(feature)=='object') ? JSON.stringify(feature) : feature;

  let fields_sheduled = ["route_name", "trip_headsign", "departure_name", "departure_time", "arrival_name", "arrival_time", "len"];
  let fields_free = ["route_name", "departure_name", "arrival_name", "arrival_time"];
  let fields_stations = ["name","route_name"];

  let aliases_scheduled = ["Ligne", "Direction", "Station de d\u00e9part", "\u00e0", "Station d\u0027arriv\u00e9e", "\u00e0", "Nombre d\u0027arr\u00eats"];
  let aliases_free = ["Ligne", "Station de d\u00e9part", "Station d\u0027arriv\u00e9e", "Dur\u00e9e"];
  let aliases_stations = ["Station","Desservie"];

  let table;
  switch(layer.feature.geometry.type){
    case "Point" :
      table = table_fill(fields_stations,aliases_stations,layer,handleObject);
      break;
    case "MultiLineString" : switch(layer.feature.properties.route_name) {
      case "Connection multimodale" :
        table = table_fill(fields_free,aliases_free,layer,handleObject);
        break;
      default :
        table = table_fill(fields_sheduled,aliases_scheduled,layer,handleObject);
        break;
    }
  }
  div.innerHTML = table;
  return div
}
