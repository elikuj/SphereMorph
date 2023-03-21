var octahedron = [
  [200, 0, 0],
  [0, 0, 200],
  [-200, 0, 0],
  [0, 0, -200],
  [0, 200, 0],
  [0, 0, 200],
  [0, -200, 0],
  [0, 0, -200],
  [200, 0, 0],
  [0, 200, 0],
  [-200, 0, 0],
  [0, -200, 0],
  [200, 0, 0]                           
]

function projectToSphere(shape, radius){
  beginShape();
  for(let i = 0; i < shape.length; i++){
    var r = Math.sqrt(shape[i][0]**2 + shape[i][1]**2 + shape[i][2]**2);
    curveVertex(radius*shape[i][0]/(r), radius*shape[i][1]/(r), radius*shape[i][2]/(r));
  }
  curveVertex(shape[0][0], shape[0][1], shape[0][1]);
  endShape();
} 

function setup() {
  createCanvas(1000, 1000, WEBGL);
  
}

function draw() {
  background(0);
  ambientLight(50);
  directionalLight(255, 0, 0, 0.25, 0.25, 0);
  
  camera(2*(mouseX-width/2), 2*(mouseY-height/2), (height/2.0)/(Math.tan(PI/6)), 0, 0, 0, 0, 1, 0)
  //translate(width / 4, 0, 0);
  ambientMaterial(250);
  //sphere(100, 25);
  beginShape();
  stroke(0, 255, 0)
  for(let i = 0; i < octahedron.length; i++){
    point(octahedron[i][0], octahedron[i][1], octahedron[i][2])
    line(octahedron[i][0], octahedron[i][1], octahedron[i][2], octahedron[(i+1)%octahedron.length][0], octahedron[(i+1)%octahedron.length][1], octahedron[(i+1)%octahedron.length][2])
  }
  endShape();

  projectToSphere(octahedron, 100)
}
