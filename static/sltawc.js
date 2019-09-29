var cl_val = 0;
var ca_val = 0;
var lc_val = 0;

function inc_clients() {
    if(cl_val < target_clients()) {
        cl_val += 1;
        var e = document.getElementById('cl_td');
        e.innerText = cl_val;
        setTimeout(inc_clients, 500);
    }
}

function inc_lotes() {
    if(lc_val < target_lotes()) {
        lc_val += 1;
        var e = document.getElementById('lc_td');
        e.innerText = lc_val;
        setTimeout(inc_lotes, 500);
    }
}

function inc_cars() {
    if(ca_val < target_cars()) {
        ca_val += 1;
        var e = document.getElementById('ca_td');
        e.innerText = ca_val;
        setTimeout(inc_cars, 500);
    }
}

function init() {
    cl_val = 0;
    ca_val = 0;
    lc_val = 0;
    inc_cars();
    inc_lotes();
    inc_clients();
}

async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrer: 'no-referrer', // no-referrer, *client
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  r = await response.json(); // parses JSON response into native JavaScript objects
  console.log(r);
  return r;
}

var tkn = null;

async function clientData() {
    cname = document.getElementById('uname').value;
    pwd = document.getElementById('pwd').value;
    const resp = await postData('get_token', {cname: cname, passwd: pwd});
    var e = document.getElementById('databox');
    if(resp["valid"]) {
        tkn = resp["token"];
        e.hidden = false;
        e = document.getElementById('messagebx');
        e.hidden = false;
        e = document.getElementById('vehicleList');
        e.innerHTML = '';
        e.hidden = false;
        var cars = await postData('get_cars', {token: tkn});
        for(var i in cars["cars"]) {
            var node = document.createElement('button');
            node.className = "list-group-item";
            const vin = cars["cars"][i].vin;
            node.innerText = vin;
            node.onclick = async () => await status(vin);
            const state = cars["cars"][i].state == 1;
            if (state)
                node.classList.add("active");
            e.appendChild(node);
        }
        data = await postData('get_data',{token: tkn});
        var rut = document.getElementById('rutTD');
        rut.innerText = data.rut;
        var nombre = document.getElementById('cnameTD');
        nombre.innerText = data.nombre;
    } else {
        e.hidden = true;
        e = document.getElementById('messagebx');
        e.hidden = true;
    }
}

async function commentOn(VIN, message) {
    if(tkn !== null) {
        var path = await postData('comment_on', {token: tkn, vin: VIN, msg: btoa(message)});
        //console.log(path);
        var e = document.getElementById('sendmsg');
        e.className = "btn " + (path['valid'] ? 'btn-success' : 'btn-danger');
    }
}

async function listMsg(VIN) {
    var msgbox = document.getElementById('messagelist');
    var msgdiv = document.getElementById('messagebx');
    msgbox.innerHTML = '';
    msgdiv.hidden = false;
    var resp_cms = await postData('comments_for',{token: tkn, vin: VIN});
    //console.log(resp_cms);
    if (resp_cms.valid) {
        for(var i = 0; i < resp_cms.messages.length; i++) {
            node = document.createElement('li');
            node.innerText = resp_cms.messages[i];
            node.className = 'list-group-item list-group-item-info';
            node.style.width="100%";
            msgbox.appendChild(node);
        }
    }
 }

async function status(VIN) {
    if(tkn !== null) {
        var data = await postData('get_status', {token: tkn, vin: VIN});
        console.log(data);
//        map_engine_main(VIN, tkn);
//        oms_map(VIN, tkn);
        document.getElementById('modeloTD').innerText = data.modelo;
        document.getElementById('marcaTD').innerText = data.marca;
        document.getElementById('anioTD').innerText = data.anio;
        await listMsg(VIN);
        var path = await postData('get_path', {token: tkn, vin: VIN});
        path = await path.json();
        //console.log(path);
        var e = document.getElementById('pathList');
        e.innerHTML = "";
        for(var k in path["path"]) {
            var node = document.createElement('li');
            node.className = "list-group-item";
            node.innerText = path["path"][k];
            e.appendChild(node);
        }
        var msgbox = document.getElementById('msgbox');
        msgbox.hidden = false;
        var b = document.getElementById('sendmsg');
        b.onclick = async () => {
            await commentOn(VIN, document.getElementById('msg').value);
            listMsg(VIN);
        }
    }
}