function fill_template_non_bus_scheduled(agency_url,line_url,agency_name,line_name,t_depart,t_arriv,l_depart,l_arriv,direction,nb_arrets){
  var html = [
  '  <table class="idfm">',
  '    <thead>',
  '      <tr>',
  '        <th rowspan="2"><img src="'+agency_url+'" alt="'+agency_name+'"style="width:50px;height:50px;"></th>',
  '        <th rowspan="2"><img src="'+line_url+'" alt="'+line_name+'" style="width:50px;height:50px;"></th>',
  '        <td> <div class="idfm_bold">'+l_depart+'</div></td>',
  '        <td> <div class="idfm_bold">'+l_arriv+'</div></td>',
  '      </tr>',
  '      <tr>',
  '        <td>'+t_depart+'</td>',
  '        <td>'+t_arriv+'</td>',
  '      </tr>',
  '    </thead>',
  '    <tbody>',
  '      <tr>',
  '        <td colspan="3"><div class="idfm_bold">Direction</div>'+direction+'</td>',
  '        <td><div class="idfm_bold">Nombre d'+"'"+'arr\u00eats</div>'+nb_arrets+'</td>',
  '      </tr>',
  '    </tbody>',
  '  </table>'
  ].join('\n');
  return html
}

function fill_template_bus_scheduled(agency_url,agency_name,line_name,route_color,route_text_color,t_depart,t_arriv,l_depart,l_arriv,direction,nb_arrets){
  var html = [
  '    <table class="idfm">',
  '      <thead>',
  '        <tr>',
  '          <th rowspan="2"><img src='+agency_url+' alt="bus" style="width:50px;height:50px;"></th>',
  '            <td rowspan="2">',
  '              <div class="rounded agency">'+agency_name+'</div><div class="rounded" style="background-color: '+route_color+';color : '+route_text_color+';text-align: center;">'+line_name+'</div>',
  '            </td>',
  '          <td> <div class="idfm_bold">'+l_depart+'</div></td>',
  '        <td> <div class="idfm_bold">'+l_arriv+'</div></td>',
  '      </tr>',
  '      <tr>',
  '        <td>'+t_depart+'</td>',
  '        <td>'+t_arriv+'</td>',
  '      </tr>',
  '    </thead>',
  '    <tbody>',
  '      <tr>',
  '        <td colspan="3"><div class="idfm_bold">Direction</div>'+direction+'</td>',
  '        <td><div class="idfm_bold">Nombre d'+"'"+'arr\u00eats</div>'+nb_arrets+'</td>',
  '      </tr>',
  '    </tbody>',
  '  </table>'
  ].join('\n');
      return html;
}

function fill_template_free(l_depart,l_arriv,t_trajet,pieton_url){
  var html =[
  '  <table class=" idfm">',
  '    <thead>',
  '      <tr>',
  '        <th colspan="3">Connection Multimodale</th>',
  '      </tr>',
  '    </thead>',
  '    <tbody>',
  '      <tr>',
  '        <td><img src="'+pieton_url+'" alt="AGENCY" style="width:60px;height:60px;"></td>',
  '        <td>'+l_depart+'</td>',
  '        <td>'+l_arriv+'</td>',
  '      </tr>',
  '      <tr>',
  '        <td colspan="3">'+t_trajet+'</td>',
  '      </tr>',
  '    </tbody>',
  '   </table>'
].join('\n');
  return html;
}

function fill_template_tooltip_scheduled(agency_url,line_url,agency_name,line_name,route_color,route_text_color){
  switch(line_url){
    case "NULL":
      var html=[
        '    <table class="idfm">',
        '        <tr>',
        '          <th><img src='+agency_url+' alt="bus" style="width:50px;height:50px;"></th>',
        '          <style>',
        '          .bus_tool{',
        '              background-color: '+route_color+';',
        '              color : '+route_text_color+';',
        '              text-align: center;',
        '          }',
        '          </style>',
        '          <td>',
        '              <div class="rounded agency">'+agency_name+'</div><div class="rounded bus_tool">'+line_name+'</div>',
        '          </td>',
        '       </tr>',
        '    </table>',
      ].join('\n');
      break;
    default:
      var html=[
        '    <table class=" idfm">',
        '        <tr>',
        '          <th><img src='+agency_url+' alt="bus" style="width:50px;height:50px;"></th>',
        '          <th rowspan="2"><img src="'+line_url+'" alt="'+line_name+'" style="width:50px;height:50px;"></th>',
        '       </tr>',
        '    </table>',
      ].join('\n');
  }
  return html;
}

function fill_template_tooltip_free(pieton_url){
  var html =[
    '  <div class="idfm">',
    '   <img src="'+pieton_url+'" alt="Connection Multimodale" style="width:60px;height:60px;">',
    '  </div>'
  ].join('\n');
  return html;
}

function fill_template_free_min(l_depart,l_arriv,t_trajet){
  var html =[
  '  <table class="idfm">',
  '    <thead>',
  '      <tr>',
  '        <th>Connection Multimodale</th>',
  '        <td>'+l_depart+'</td>',
  '        <td>'+l_arriv+'</td>',
  '      </tr>',
  '   </thead>',
  '    <tbody>',
  '      <tr>',
  '        <td colspan="3">'+t_trajet+'</td>',
  '      </tr>',
  '    </tbody>',
  '   </table>'
].join('\n');
return html;
}
