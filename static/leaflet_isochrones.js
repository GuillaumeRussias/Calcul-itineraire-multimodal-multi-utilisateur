var weight = 3;
//
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
  };
}

function highlight(feature) {
  switch (feature.geometry.type){
    case "Polygon" : return style_polygon(feature,1);
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
  let aliases = ["Zone accessible pour un temps"];
  let table;
  switch(layer.feature.geometry.type){
    case "Point":
      table = table_fill(["centre"],["Centre des isochrones"],layer,handleObject);
      break;
    default :
      table = table_fill(fields,aliases,layer,handleObject);
      break;
  }
  div.innerHTML = table;
  return div
}
