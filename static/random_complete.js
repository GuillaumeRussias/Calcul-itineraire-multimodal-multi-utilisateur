function random_complete_station(list_id,list_summits){
  let random_seed;
  for (let i = 0; i < list_id.length; i++) {
    random_seed = Math.floor((Math.random() * list_summits.length));
    document.getElementById(list_id[i]).value = list_summits[random_seed]
  }
}
function random_complete_time(list_id){
  let random_seed_hour;
  let random_seed_min;
  for (let i = 0; i < list_id.length; i++) {
    random_seed_hour = Math.floor((Math.random() * 24));
    random_seed_min = Math.floor((Math.random() * 60));
    if (random_seed_hour<10){random_seed_hour = ["0",random_seed_hour.toString()].join("");}
    else{random_seed_hour = random_seed_hour.toString();}
    if (random_seed_min<10){random_seed_min = ["0",random_seed_min.toString()].join("");}
    else{random_seed_min = random_seed_min.toString();}
    document.getElementById(list_id[i]).value = [random_seed_hour,random_seed_min].join(":");
  }
}

function random_complete_int(id){
  let int = Math.floor((Math.random() * 50)+1);
  document.getElementById(id).value = int.toString();
}

function random_complete_with_summit(bool_rd,list_id_stations,list_id_time,list_summits){
  if (bool_rd==true){
    random_complete_station(list_id_stations,list_summits);
    random_complete_time(list_id_time);
  }
}
function random_complete_with_summit_range(bool_rd,n,list_summits){
  if (bool_rd==true){
    for(let i=0; i<n;i++){
    random_complete_station([i.toString()],list_summits)
    }
  }
}

function complete_without_summit(bool_rd,id_int,list_id_time){
  if (bool_rd==true){
    random_complete_int(id_int);
    random_complete_time(list_id_time);
  }
}
