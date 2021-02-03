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
          <th>${aliases[i]}</th>
          <td>${handleObject(layer.feature.properties[v].split("####").join(" ")).toLocaleString()}</td>
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
      table = tooltip_multilinestring_fill(layer,handleObject);
      break;
  }
  div.innerHTML=table;
  return div;
}

function tooltip_multilinestring_fill(layer,handleObject){
  switch(handleObject(layer.feature.properties["route_name"])){
    case "Connection multimodale" :
      return  tooltip_free_fill();
    default:
      return tooltip_sheduled_fill(layer,handleObject);
  }
}

function tooltip_sheduled_fill(layer,handleObject){
  var splitted = handleObject(layer.feature.properties["route_name"]).split('####');
  var agency_name = splitted[0];
  var line_name = splitted.slice(1).join('');
  var agency_url = get_icon_agency_url(handleObject(layer.feature.properties["route_name"]))
  var line_url = get_icon_line_url(handleObject(layer.feature.properties["route_name"]))
  var route_color = handleObject(layer.feature.properties["route_color"]);
  var route_text_color = handleObject(layer.feature.properties["route_text_color"]);
  return fill_template_tooltip_scheduled(agency_url,line_url,agency_name,line_name,route_color,route_text_color);
}
function tooltip_free_fill(){
  return fill_template_tooltip_free(source_url+"static/idfm_style/agencies/pieton.svg");
}

function get_icon_agency_url(route_name){
  try {return source_url+icons_table[route_name]["agency_url"];}
  catch {return source_url+icons_table["BUS"]["agency_url"];}
}

function get_icon_line_url(route_name){
  try {return source_url+icons_table[route_name]["line_url"];}
  catch {return "NULL";}
}

function scheduled_fill(layer,handleObject){
  var splitted = handleObject(layer.feature.properties["route_name"]).split('####');
  var agency_name = splitted[0];
  console.log(agency_name);
  var line_name = splitted.slice(1).join(' ');
  console.log(line_name);
  var agency_url = get_icon_agency_url(handleObject(layer.feature.properties["route_name"]))
  var line_url = get_icon_line_url(handleObject(layer.feature.properties["route_name"]))
  var route_color = handleObject(layer.feature.properties["route_color"]);
  var route_text_color = handleObject(layer.feature.properties["route_text_color"]);
  var t_depart = handleObject(layer.feature.properties["departure_time"]);
  var t_arriv = handleObject(layer.feature.properties["arrival_time"]);
  var l_depart = handleObject(layer.feature.properties["departure_name"]);
  var l_arriv = handleObject(layer.feature.properties["arrival_name"]);
  var direction = handleObject(layer.feature.properties["trip_headsign"]);
  var nb_arrets = handleObject(layer.feature.properties["len"]);
  switch (line_url){
    case "NULL":
      return fill_template_bus_scheduled(agency_url,agency_name,line_name,route_color,route_text_color,t_depart,t_arriv,l_depart,l_arriv,direction,nb_arrets);
    default :
      return fill_template_non_bus_scheduled(agency_url,line_url,agency_name,line_name,t_depart,t_arriv,l_depart,l_arriv,direction,nb_arrets);
  }
}
function free_fill(layer,handleObject){
  var l_depart = handleObject(layer.feature.properties["departure_name"]);
  var l_arriv = handleObject(layer.feature.properties["arrival_name"]);
  var t_trajet = handleObject(layer.feature.properties["arrival_time"]);
  return fill_template_free(l_depart,l_arriv,t_trajet,source_url+"static/idfm_style/agencies/pieton.svg");
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
        table = free_fill(layer,handleObject);
        break;
      default :
        table = scheduled_fill(layer,handleObject);
        break;
    }
  }
  div.innerHTML = table;
  return div
}
