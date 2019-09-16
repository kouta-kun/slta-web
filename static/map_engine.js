async function loadImages_MAP() { // cargar las "texturas"
    // el cargado de imágenes en javascript es asíncrono, por ende devolvemos una promesa
    // la cual esperamos con await fuera de la función
    var cv = document.getElementById("be_2d_2");
    var ctx = cv.getContext("2d");
    var tsImage = new Image();
    var tsImgProm = new Promise((resolve, reject) => {
        tsImage.src = tsPath();
        tsImage.onload = function() {
            cv.height = tsImage.height;
            cv.width = tsImage.width+36;
            ctx.globalCompositeOperation = 'copy';
            ctx.drawImage(tsImage, 0, 0);
            const tilesX = tsImage.width/16;
            const tilesY = tsImage.height/16;
            const totalTiles = tilesX * tilesY;
            let tileData = new Array(totalTiles);
            //console.log(tileData);
            let tmpCanvas = document.createElement('canvas');
            //console.log(tmpCanvas);
            let tmpContext = tmpCanvas.getContext('2d');
            tmpCanvas.height = 16;
            tmpCanvas.width = 16;
            var tI = new Image();
            tmpContext.drawImage(tsImage, 0, 0, 16, 16, 0, 0, 16, 16);
            tI = new Image();
            tI.src = tmpCanvas.toDataURL('image/png');
            tileData[0] = tI;
            for(let y = 0; y < tilesY; y++) {
                for(let x = (y==0?1:0); x<tilesX; x++)
                {
                    tmpCanvas = document.createElement('canvas');
                    tmpContext = tmpCanvas.getContext('2d');
                    tmpCanvas.height = 16;
                    tmpCanvas.width = 16;
                    tmpContext.drawImage(tsImage, x*16, y*16, 16, 16, 0, 0, 16, 16);
                    tI = new Image();
                    tI.src = tmpCanvas.toDataURL('image/png');
                    tileData[y*tilesX+x] = tI;
                }
            }
            //console.log(tileData);
            resolve(tileData);
        };
    });
    var tsImg = await tsImgProm;
    var tmImg = new Promise((resolve, reject) => {
        var tmImage = new Image();
        tmImage.src = tmPath();
        tmImage.onload = () => {
            var kvs = {};
            ctx.drawImage(tmImage,36,0);
            //console.log(tmImage);
            //console.log("sizeofTMImage");
            let cols = {};
            for(var x = 0; x < 36; x++)
            {
                for(var y = 0; y < 36; y++)
                {
                    var imgData = ctx.getImageData(36+x,y,1,1);
                    if(imgData.data[3] != 0)
                        kvs[[x,y]] = imgData.data[0];
                }
            }
            //console.log(kvs);
            resolve(kvs);
        };

    });
    return [tsImg, tmImg];
}

function drawTile(ctx, tile, x, y) {
    const xOffset = (x*16);
    const yOffset = (y*16);
    ctx.drawImage(tile, xOffset, yOffset);
}

var departamentos = {119: "Artigas", 31: "Salto", 111: "Rivera", 39: "Tacuarembo", 63: "Paysandu", 143: "Cerro Largo", 79: "Rio negro", 103: "Durazno", 247: "Florida", 47: "Treinta y tres", 127: "Soriano", 15: "Flores", 0: "Lavalleja", 207:"Rocha", 175: "Colonia", 183: "San Jose", 167: "Canelones", 71: "Maldonado", 23: "Montevideo"};

async function oms_map(vin, tkn) {
    var mapDom = document.createElement('div');
    mapDom.id='map';
    document.body.appendChild(mapDom);    // The overlay layer for our marker, with a simple diamond as symbol
    var overlay = new OpenLayers.Layer.Vector('Overlay', {
        styleMap: new OpenLayers.StyleMap({
            externalGraphic: '../img/marker.png',
            graphicWidth: 20, graphicHeight: 24, graphicYOffset: -24,
            title: '${tooltip}'
        })
    });

    // The location of our marker and popup. We usually think in geographic
    // coordinates ('EPSG:4326'), but the map is projected ('EPSG:3857').
    var myLocation = new OpenLayers.Geometry.Point(10.2, 48.9)
        .transform('EPSG:4326', 'EPSG:3857');

    // We add the marker with a tooltip text to the overlay
    overlay.addFeatures([
        new OpenLayers.Feature.Vector(myLocation, {tooltip: 'OpenLayers'})
    ]);

    // A popup with some information about our location
    var popup = new OpenLayers.Popup.FramedCloud("Popup",
        myLocation.getBounds().getCenterLonLat(), null,
        '<a target="_blank" href="http://openlayers.org/">We</a> ' +
        'could be here.<br>Or elsewhere.', null,
        true // <-- true if we want a close (X) button, false otherwise
    );

    // Finally we create the map
    map = new OpenLayers.Map({
        div: "map", projection: "EPSG:3857",
        layers: [new OpenLayers.Layer.OSM(), overlay],
        center: myLocation.getBounds().getCenterLonLat(), zoom: 15
    });
    // and add the popup to it.
    map.addPopup(popup);
}

async function map_engine_main(vin, tkn) {
    const frameRate = 60;
    //console.log(frameRate);
    var renderer;
    renderer = document.getElementById("be_2d_2");
    if(renderer !== null) {
        // si hay un canvas, lo eliminamos
        //console.log(renderer);
        document.body.removeChild(renderer);
    }
    renderer = document.createElement('canvas');
    renderer.id = "be_2d_2";
    document.body.appendChild(renderer);
    // creamos un canvas y lo agregamos a la página
    var gridpath = fetch('get_gridpath?token=' + tkn + '&vin=' + vin);
    var renderer = document.getElementById("be_2d_2");
    var images = await loadImages_MAP();
    //console.log(images);
    var tsImage = await images[0]; // el cargado de imagenes en javascript es asíncrono así que debemos esperarlo
    renderer.height = 36*16;
    renderer.width = 36*16;
    var ctx = renderer.getContext('2d');
    //console.log(tsImage);
    var waterTile = tsImage[168];
    var earthTile = tsImage[3];
    var castleTile = tsImage[34];
    var towerTile = tsImage[32];
    var homeTile = tsImage[7];
    var campTile = tsImage[37];
    var swordTile = tsImage[36];
    var villageTile = tsImage[43];
    ctx.globalCompositeOperation = 'source-over';
    var tmap = await images[1];
    gridpath = await gridpath;
    gridpath = await gridpath.json();
    var fmap = {};
    for(var key in tmap) {
        //console.log(Object.keys(fmap).indexOf(Number.parseInt(tmap[key])));
        if(Object.keys(fmap).indexOf(Number.parseInt(tmap[key])) >= 0)
        {
            //console.log("repeated: " + tmap[key]);
        }
        fmap[Number.parseInt(tmap[key])] = {"index": tmap[key]}
    }
    //console.log(fmap);
    //console.log(Object.keys(fmap).length);
    var bmap = {};
    var buildings = {};
    for(var i = 0; i < gridpath.path.length; i++)
    {
        const key = [gridpath.path[i][0], gridpath.path[i][1]]
        if(buildings[key] === undefined) {
            buildings[key] = [];
        }
        if(gridpath.path[i][2] == "Puerto")
        {
            if(bmap[key] === undefined)
                bmap[key] = "p";
            else bmap[key] += "p";
        } else if (gridpath.path[i][2] == "Patio")
        {
            if(bmap[key] === undefined)
                bmap[key] = "P";
            else bmap[key] += "P";
        }
        else if (gridpath.path[i][2] == "Establecimiento")
        {
            if(bmap[key] === undefined)
                bmap[key] = "E";
            else bmap[key] += "E";
        }
        if(buildings[key].indexOf(gridpath.path[i][3]) < 0)
            buildings[key].push(gridpath.path[i][3]);
    }
    ////console.log(buildings);
    var msg = "";
    var msgSrc = [0,0];
    renderer.addEventListener("mousemove", function(evt) {
        var rect = renderer.getBoundingClientRect();
        var relX = evt.clientX-rect.left;
        var relY = evt.clientY-rect.top;
        var tileX = Math.floor(relX / 16);
        var tileY = Math.floor(relY / 16);
        msg = departamentos[tmap[[tileX,tileY]]] || "Mar";
        if (buildings[[tileX,tileY]] !== undefined) {
            msg += ":\n" + buildings[[tileX, tileY]].join('\n');
        }
        msgSrc = [relX+16,relY];
    });
    function animate() {
        ctx.strokeStyle = "#000000";
        ctx.fillStyle = "black";
        ctx.fillRect(0,0,36*16,36*16);
        for(let x = 0; x < 36; x++) {
            for(let y = 0; y < 36; y++) {
                drawTile(ctx, (tmap[[x,y]] !== undefined) ? earthTile : waterTile, x, y);
                if(bmap[[x,y]] !== undefined) {
                    var hasPort = bmap[[x,y]].indexOf('p') >= 0;
                    var hasGrounds = bmap[[x,y]].indexOf('P') >= 0;
                    var hasClient = bmap[[x,y]].indexOf('E') >= 0;
                    if(hasClient && hasGrounds && hasPort) {
                        drawTile(ctx, castleTile, x, y);
                    } else if (hasPort) {
                        drawTile(ctx, towerTile, x,y);
                    } else if (hasClient && hasGrounds) {
                        drawTile(ctx, villageTile, x,y);
                    } else if (hasClient) {
                        drawTile(ctx, homeTile, x, y);
                    } else if (hasGrounds) {
                        drawTile(ctx, campTile, x,y);
                    }
                }
                if(tmap[[x,y]] !== undefined) {
                    if(tmap[[x-1, y]] !== undefined && tmap[[x-1,y]] != tmap[[x,y]]) {
//                        //console.log([[x-1,y], [x,y]]);
                        ctx.beginPath();
                        ctx.moveTo(x*16,y*16);
                        ctx.lineTo(x*16,(y+1)*16);
                        ctx.stroke();
                    }
                    if(tmap[[x+1, y]] !== undefined && tmap[[x+1,y]] != tmap[[x,y]]) {
                        ctx.beginPath();
                        ctx.moveTo((x+1)*16,y*16);
                        ctx.lineTo((x+1)*16,(y+1)*16);
                        ctx.stroke();
                    }
                    if(tmap[[x,y-1]] !== undefined && tmap[[x,y-1]] != tmap[[x,y]]) {
                        ctx.beginPath();
                        ctx.moveTo((x)*16,y*16);
                        ctx.lineTo((x+1)*16,y*16);
                        ctx.stroke();
                    }
                    if(tmap[[x,y+1]] !== undefined && tmap[[x,y+1]] != tmap[[x,y]]) {
                        ctx.beginPath();
                        ctx.moveTo((x)*16,(y+1)*16);
                        ctx.lineTo((x+1)*16,(y+1)*16);
                        ctx.stroke();
                    }
                }
            }
        }
        ctx.strokeStyle = "#00a0f0";
        ctx.strokeText(0,gridpath.path[0][0]*16,gridpath.path[0][1]*16);
        for(var k = 0; k < gridpath.path.length/2; k++)
        {
            ctx.beginPath();
            ctx.moveTo(gridpath.path[k*2][0]*16,gridpath.path[k*2][1]*16);
            ctx.lineTo(gridpath.path[k*2+1][0]*16,gridpath.path[k*2+1][1]*16);
            ctx.stroke();
            ctx.strokeText(k+1,gridpath.path[k*2+1][0]*16,gridpath.path[k*2+1][1]*16);
        }
        ctx.strokeStyle = "#000000";
        ctx.fillStyle = "#a0a0ff";
        if(msg != ''){
            let xLen = 0;
            var msgData = msg.split('\n');
            let yLen = msgData.length*12;
            for(var i = 0; i < msgData.length; i++)
                if(msgData[i].length > xLen)
                    xLen = msgData[i].length;
            ctx.fillRect(msgSrc[0], msgSrc[1], 6*xLen, yLen);
            ctx.strokeRect(msgSrc[0],msgSrc[1],6*xLen, yLen);
            for(var i = 0; i < msgData.length; i++)
                ctx.strokeText(msgData[i], msgSrc[0],msgSrc[1]+(10*(i+1)))
        }
        setTimeout(animate, 1000/frameRate); // en (1000/frameRate) milisegundos se volverá a dibujar una imagen
    }
    animate();
}