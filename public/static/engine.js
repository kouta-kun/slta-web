function randomBinary() { // generar un string binario de 41 bits al azar
    var str = "";
    for(var i = 0; i < 40; i++) {
        var b_i = Math.abs(Math.round(Math.random())); // numero al azar entre 0 y 1
        str += b_i;
    }
    return str.padStart(41, '0');
}

const initT = init;
init = function() { initT(); engine_main();}

function loadImages() { // cargar las "texturas"
    // el cargado de imágenes en javascript es asíncrono, por ende devolvemos una promesa
    // la cual esperamos con await fuera de la función
    var bImg = new Promise((resolve, reject) => {
        var bitImage = new Image();
        bitImage.src = route_bit();
        bitImage.onload = () => resolve(bitImage);
    });
    var rImg = new Promise((resolve, reject) => {
        var roadImage = new Image();
        roadImage.src = route_road();
        roadImage.onload = () => resolve(roadImage);
    });
    return [bImg, rImg];
}

function escalaSeno(limiteX, limiteY) { // explicación: genera una escala de la función seno en limiteX/2, donde eS(limiteX/2)=limiteY;
    return k => Math.sin(k*(Math.PI/limiteX))*limiteY;
}

async function engine_main() {
    const frameRate = 60;
    if(document.getElementById('be_2d') === null) { // si no hay un canvas, lo creamos
        let renderer = document.createElement('canvas');
        renderer.id = "be_2d";
        renderer.height = 250;
        renderer.width = 250; 
        document.body.appendChild(renderer);// creamos un canvas de 250*250 y lo agregamos a la página
    }
    var renderer = document.getElementById("be_2d");
    var images = loadImages();
    var bitImage = await images[0]; // el cargado de imagenes en javascript es asíncrono así que debemos esperarlo
    var roadImage = await images[1]; // utilizando 'await' esperamos a que la promesa de carga se cumpla
    var frameCount = 0;
    var ctx = renderer.getContext('2d');
    ctx.btext = []; // donde se guardarán los string de bits a mostrar de fondo
    for(var k = 0; k < 25; k++) {
        ctx.btext.push(randomBinary());
    }
    const roadSpeed = 2; // mayor roadspeed -> menor velocidad de rotación
    function animate() {
        ctx.lineWidth = 1;
        ctx.fillStyle = "white";
        ctx.fillRect(0,0,renderer.width,renderer.height); // llenamos el canvas de negro
        ctx.strokeStyle = "#c7eaf2";
        if(frameCount % 6 == 0) { // cada 3 frames eliminamos la última línea y agregamos una nueva
            ctx.btext.shift();
            ctx.btext.push(randomBinary());
        }
        for(var k = 0; k < 25; k++) {
            ctx.strokeText(ctx.btext[k], 2, 8 + (10 * (k))); // dibujamos los strings binarios del fondo
        }
        ctx.fillStyle = "white";
        ctx.drawImage(roadImage, 0, 0, 250, 250); // dibujamos la ruta azul
                                                  // (además también dibuja el fondo blanco alrededor)

        ctx.translate(125,125);                   // la ruta tiene su centro en (125,125), el medio de la pantalla,
                                                  // por lo cual nos movemos a ese punto
        ctx.rotate((2) *                        // rotamos por un grado calculado en base al frame actual
                    ((frameCount/roadSpeed))
                    * Math.PI / 180);
        ctx.translate(-125,-125);                 // y volvemos a nuestra posición inicial
        ctx.lineWidth = 3;
        for(var i = 0; i < 10; i++) {
            ctx.strokeStyle = "rgb(255,255,0)";
            ctx.beginPath();
            ctx.arc(125,125,105,
            (i*(360/10))*Math.PI / 180, ((i*(360/10))+(360/20)) * Math.PI / 180); // dibujamos las lineas de la ruta
            ctx.stroke();
        }
        ctx.setTransform(1,0,0,1,0,0); // reiniciamos la matriz de transformación para no rotar la imagen de bit
        ctx.drawImage(bitImage, 0, 0, 250, 250);
        frameCount++;
        setTimeout(animate, 1000/frameRate); // en (1000/frameRate) milisegundos se volverá a dibujar una imagen
    }
    animate();
}