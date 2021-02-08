var weight = 3;


function point_to_circle (feature,latlng) {
  if (feature.properties.type=="stop"){
    var layer = L.circleMarker(latlng,0.1)
    layer.feature = feature ;
    layer.interactive = false;
    layer.stroke = false;
    return  layer;
  }
  else {
    return L.marker(latlng);
  }
}



//
function style_circle(feature,bool) {
  return {
    radius : 5,
    fillColor : feature.properties.color,
    opacity : 0.9,
    color : feature.properties.color,
    weight : 0,
    fillOpacity : 0.8,
  };
}
function style_polygon(feature,bool) {
  return {
    fillColor : feature.properties.color,
    opacity : 0.3 + 0.2*bool,
    color : feature.properties.color,
    weight : weight*(1+0.5*bool),
    fillOpacity : 0.3 + 0.2*bool,
  };
}
function style(feature) {
  switch (feature.geometry.type){
    case "Polygon" : return style_polygon(feature,0);
    case "MultiPoint" : return style_circle(feature,0);
  };
}

function highlight(feature) {
  switch (feature.geometry.type){
    case "Polygon" : return style_polygon(feature,1);
    case "MultiPoint" : return style_circle(feature,1);
  };
}

function On_Each_Feature(feature, layer) {
    switch(feature.properties.type){
      case "center" :
          layer.on({
              mouseout: function(e) {
                  plotted_traject.resetStyle(e.target);
              },
              mouseover: function(e) {
                  e.target.setStyle(highlight(e.target.feature));
              },
          });
          break;
    }
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
          <td>${handleObject(layer.feature.properties[v])}</td>
      </tr>`).join(''))
  +'</table>';
}

function tool_tip(layer){
  let div = L.DomUtil.create('div');
  let handleObject = feature=>typeof(feature)=='object' ? JSON.stringify(feature) : feature;
  let fields = ["isochrone"];
  let aliases = [""];
  let table = table_fill(fields,aliases,layer,handleObject);
  div.innerHTML=table;
  return div;
}

function pop_up(layer){
  let div = L.DomUtil.create('div');
  let handleObject = feature=>(typeof(feature)=='object') ? JSON.stringify(feature) : feature;
  let fields = ["isochrone"];
  let aliases = ["Arrêt accessible pour un temps"];
  let table;
  switch(layer.feature.properties.type){
    case "center":
      table = table_fill(["centre"],["Centre des isochrones"],layer,handleObject);
      break;
    default:
      table = table_fill(fields,aliases,layer,handleObject);
      break;
  }
  div.innerHTML = table;
  return div
}
