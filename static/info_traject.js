function get_list_steps(feature){
  if (feature["geometry"]["type"]=="Point"){return ""};
  let table;
  switch(feature["properties"]["route_name"]){
    case "Connection multimodale" :
      table = free_fill_list_steps(feature);
      break;
    default :
      table = scheduled_fill_list_steps(feature);
      break;
  }
  //console.log(table);
  return table;
}


function scheduled_fill_list_steps(feature){
  var splitted = feature["properties"]["route_name"].split('####');
  var agency_name = splitted[0];
  var line_name = splitted.slice(1).join('');
  var agency_url = get_icon_agency_url(feature["properties"]["route_name"]);
  var line_url = get_icon_line_url(feature["properties"]["route_name"]);
  var route_color = feature["properties"]["route_color"];
  var route_text_color = feature["properties"]["route_text_color"];
  var t_depart = feature["properties"]["departure_time"];
  var t_arriv = feature["properties"]["arrival_time"];
  var l_depart = feature["properties"]["departure_name"];
  var l_arriv = feature["properties"]["arrival_name"];
  var direction = feature["properties"]["trip_headsign"];
  var nb_arrets = feature["properties"]["len"];
  switch (line_url){
    case "NULL":
      return fill_template_bus_scheduled(agency_url,agency_name,line_name,route_color,route_text_color,t_depart,t_arriv,l_depart,l_arriv,direction,nb_arrets);
    default :
      return fill_template_non_bus_scheduled(agency_url,line_url,agency_name,line_name,t_depart,t_arriv,l_depart,l_arriv,direction,nb_arrets);
  }
}
function free_fill_list_steps(feature){
  var l_depart = feature["properties"]["departure_name"];
  var l_arriv = feature["properties"]["arrival_name"];
  var t_trajet = feature["properties"]["arrival_time"];
  return fill_template_free_min(l_depart,l_arriv,t_trajet);
}

function displayable_html(geojson_data){
  var html = [""];
  for(var i = 0, size = geojson_data["features"].length; i < size ; i++){
   var feature =  geojson_data["features"][i];
   var txt = get_list_steps(feature);
   if (txt!=""){
     html.push('<div class="container fluid border pt-1" >')
     html.push(txt);
     html.push('</div>')
   }
  }
  return html.join("\n");
}
