let shape;

let quat = new toxi.geom.Quaternion(1, 0, 0, 0);

let resetButton;

var cheminOBJ = document.getElementById('model3D').getAttribute('data');
let options = {
  normalize: true,
  successCallback: handleModel,
  failureCallback: handleError,
  fileType: '.obj'
};

function preload() 
{
  shape = loadModel(cheminOBJ, options);
}

function handleModel()
{
  console.log("model loaded");
}

function handleError()
{
  console.log("fail to load the model");
}

function setup() 
{
  createCanvas(600, 600, WEBGL);
  lights();
  initButton(resetButton, "Reset rotations", 0, 100, callbackResetButton);
}

function draw() 
{
  background(200);

  orbitControl();

  push();
  drawPitch();
  drawRoll();
  drawYaw();
  pop();
  
  push();
  displayRifle();
  drawPitch();
  drawRoll();
  drawYaw();
  pop();
}

function displayRifle()
{
  quat.set(q0, q1, q2, q3);
  let axis = quat.toAxisAngle();
  let r = axis[0];
  let v = createVector(-axis[1], axis[3], axis[2])
  rotate(r,v);
  
  push()
  rotateX(radians(90));
  rotateZ(radians(-90));

  let c = color(0);
  c.setAlpha(100);
  stroke(c);
  model(shape);
  pop()
}

function drawYaw()
{
  stroke(255,0,0);
  line(0, -75, 0, 0, 75, 0);
}

function drawRoll()
{
  stroke(0,255,0);
  line(0, 0, -75, 0, 0, 75);
}

function drawPitch()
{
  stroke(0,0,255);
  line(-75, 0, 0, 75, 0, 0);
}

function initButton(button, txt, pos_x, pos_y, callback)
{
  button = createButton(txt);
  button.position(pos_x,pos_y);
  button.mousePressed(callback);
}

function callbackResetButton()
{
  console.log("reset");
}
