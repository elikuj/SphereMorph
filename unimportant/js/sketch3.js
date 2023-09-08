class Face {
  constructor(points){
      this.points = points;
  }

  plotFace(){
      var l = points.length;
      //beginShape();
      stroke(0);
      for(let i = 0; i < points.length +1; i++){
          
          point(points[i%l][0], points[i%l][1], points[i%l][2]);
      }
      //endShape();
  }
}


class Graph {
  constructor(faces){
      this.faces = faces;
  }

  plotShape(){
    for(let i = 0; i < faces.length; i++){
        faces[i].plotFace();
    }
  }
}

function plotShape(faces){
  for(let i = 0; i < faces.length; i++){
      faces[i].plotFace();
  }
}

let directionalLightEnable = false
const p1 = [0, 0, 200];
const p2 = [0, 200, 0];
const p3 = [200, 0, 0];
const p4 = [0, 0, -200];
const p5 = [0, -200, 0];
const p6 = [-200, 0, 0];

const f1 = new Face([p1, p2, p3]);
const f2 = new Face([p1, p2, p6]);
const f3 = new Face([p1, p3, p5]);
const f4 = new Face([p1, p5, p6]);
const f5 = new Face([p4, p2, p3]);
const f6 = new Face([p4, p2, p6]);
const f7 = new Face([p4, p3, p5]);
const f8 = new Face([p4, p5, p6]);

var f9 = [p1, p2, p3];

var octahedron2 = new Graph([f1,f2,f3,f4,f5,f6,f7,f8]);

var octahedron3 = [
  [[0, 0, 200], [0, 200, 0], [200, 0, 0]],
  [[0, 0, 200], [0, 200, 0], [-200, 0, 0]],
  [[0, 0, 200], [200, 0, 0], [0, -200, 0]],
  [[0, 0, 200], [0, -200, 0], [-200, 0, 0]],
  [[0, 0, -200], [0, 200, 0], [200, 0, 0]],
  [[0, 0, -200], [0, 200, 0], [-200, 0, 0]],
  [[0, 0, -200], [200, 0, 0], [0, -200, 0]],
  [[0, 0, -200], [0, -200, 0], [-200, 0, 0]],
]

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
];

var oct4 = [f1,f2,f3,f4,f5,f6,f7,f8]

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
  //fill(50, 200, 5, 100);
  
}

function draw() {
  background(255, 255, 255);
  //ambientLight(100);
  directionalLight(255, 0, 0, height / 2, width / 2, -1);
  directionalLight(0, 0, 255, -height / 2, -width / 2, -1);
  directionalLight(0, 255, 0, -height / 2, width / 2, -1);
  directionalLight(255, 255, 255, height / 2, -width / 2, -1);
  lights();

  camera(4*(mouseX-width/2), 4*(mouseY-height/2), (height/2.0)/(Math.tan(PI/6)), 0, 0, 0, 0, 1, 0)
  //translate(width / 4, 0, 0);
  c = color(255, 0, 0, 100);
  //normalMaterial(c);
  //sphere(100, 25);
  //fill(c);
  /*beginShape();
  stroke(0);
  for(let i = 0; i < octahedron.length; i++){
    vertex(octahedron[i][0], octahedron[i][1], octahedron[i][2]);
    //line(octahedron[i][0], octahedron[i][1], octahedron[i][2], octahedron[(i+1)%octahedron.length][0], octahedron[(i+1)%octahedron.length][1], octahedron[(i+1)%octahedron.length][2])
  }*/

  //octahedron.plotShape();
  //beginShape();
  for(let i = 0; i < 8; i++){
    push();
    beginShape();
    for(let j = 0; j < octahedron3[i].length+1; j++){
      
      //noFill();
      noFill()
      vertex(octahedron3[i][j%octahedron3[i].length][0], octahedron3[i][j%octahedron3[i].length][1], octahedron3[i][j%octahedron3[i].length][2]);
    }
    endShape();
    pop();
  }
  draw3DPoints(octahedron)




  
  //endShape();
 
  /*beginShape();
    for(let i = 0; i < 3, i++){
      vertex(f9[i][0], f9[i][1], f9[i][3]);
    }
  endShape()*/

  beginShape();
  //octahedron.plotShape();
  for(let i = 0; i < oct4.length; i++){
    //for(let j = 0; j < octahedron3[i].length; j++){
      //let r = Math.sqrt(octahedron3[i][j][0]**2 + octahedron3[i][j][1]**2 + octahedron3[i][j][2]**2);
      //point(octahedron3[i][j][0]/r * 100, octahedron3[i][j][1]/r * 100, octahedron3[i][j][2]/r * 100);
    //}
    //oct4[i].plotFace();
  }
  endShape();
  push();
  noFill();
  for(let i = 0; i < octahedron.length; i++){
    
    let p1 = octahedron[i];
    let p2 = octahedron[(i+1)%octahedron.length];
    let r1 = Math.sqrt(p1[0]**2+p1[1]**2+p1[2]**2);
    let angle1 = Math.acos((1*p2[0] )/(Math.sqrt(p2[0]**2 + p2[1]**2 + p2[2]**2)));
    let angle2 = Math.acos((p1[0]*p2[0])/(Math.sqrt(p1[0]**2 + p1[1]**2 + p1[2]**2)));
    arc(0, 0, 200, 200, angle1, angle2).rotate(PI, createVector((200+(p1[0]/r1))/2, p1[1]/(2*r1), p1[2]/(2*r1)));

  }
  //arc(0, 0, 200, 200, 100, 0).rotateX(PI/4);
  //arc(0, 0, 200, 200, 100, 0);

  pop();

  //circle(0, 0, 400);
  
  
  //projectToSphere(octahedron, 100)
}
