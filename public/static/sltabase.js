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
    inc_cars();
    inc_lotes();
    inc_clients();
}