
/*
noStroke();
lights();
translate(232, 192, 0);
sphere(112);
*/

import java.lang.Math;
float init_shape[] = new float[]{0, 200, 200, 200, 200, 0, 0, 0,0, 0, 200, 200, 200, 0, 200, 200, 200, 0, 0,0,0, 200, 0, 200};

void setup() {
  size(640, 360, P3D);
  //float init_shape[] = new float[]{0, 200, 200, 200, 200, 00, 0,0, 0, 200, 200, 200, 0, 200, 200, 200, 0, 0,0,0, 200, 0, 200};
}

void draw() {
  frameRate(10);
  background(0);
  camera(mouseX, height/2, (height/2) / tan(PI/6), width/2, height/2, 0, 0, 1, 0);
  translate(width/2, height/2, -100);
  stroke(255);
  noFill();
  //box(200);
  

    beginShape();
    /*vertex(0, 200, 200);
    vertex(200, 200, 0);
    vertex(0, 0,0);
    vertex(0, 200, 200);
    vertex(200, 0, 200);
    vertex(200, 200, 0);
    vertex(0,0,0);
    vertex(200, 0, 200);*/
    for(int i=0; i < init_shape.length-2; i=i+3){
      vertex(init_shape[i], init_shape[i+1], init_shape[i+2]);
    }
    endShape(CLOSE);
    beginShape();
    //init_shape = transform(init_shape, PI/4);
    for(int i=0; i < init_shape.length-2; i=i+3){
      //vertex(init_shape[i], init_shape[i+1], init_shape[i+2]);
      
    }
    endShape(CLOSE);
    
    beginShape();
    for(int i=0; i < init_shape.length-2; i=i+3){
      float radius = (float)(Math.pow((Math.pow(init_shape[i]-100,2) + Math.pow(init_shape[i+1]-100, 2) + Math.pow(init_shape[i+2]-100, 2)), (1/2)));
      vertex(init_shape[i]/radius+10, init_shape[i+1]/radius+10, init_shape[i+2]/radius+10);
      
    }
    endShape(CLOSE);
  
  

}

float[] transform(float[] shape, float angle){
  for(int i = 0; i < shape.length-2; i=i+3){
     if(shape[i+2] > 100){
       shape[i] = cos(angle)*shape[i] - sin(angle)*shape[i+1];
       shape[i+1] = sin(angle)*shape[i] + cos(angle)*shape[i+1];
     }
  }
  return shape;

}
