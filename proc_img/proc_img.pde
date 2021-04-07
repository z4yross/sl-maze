import processing.pdf.*;
import processing.svg.*;

JSONObject data;
String dataAdd = "../data/data.json";

final int FACTOR = 38;

void setup(){
  //size(730, 367, SVG, "../maze.svg");
  //size(19, 10, PDF, "../maze.pdf");
  // size(19, 10);
  size(730, 367);
  background(255);
  surface.setVisible(false);
  
  data = loadJSONObject(dataAdd);
  pushMatrix();
  translate(width/2, height/2);
  
  JSONArray wall = data.getJSONArray("wall");
  for(int i = 0; i < wall.size(); i++){
    JSONObject fgr = wall.getJSONObject(i);
    boolean clr = fgr.getBoolean("color"); 
    noStroke();
    fill(clr ? 0 : 255);
    JSONArray crds = fgr.getJSONArray("coords"); 
    beginShape();
    for(int j = 0; j < crds.size(); j++){
      float[] crd = crds.getJSONArray(j).getFloatArray();
      float crdX = crd[0];
      float crdY = crd[1];
      // float crdX = map(crd[0], 0, 730, 0, width);
      // float crdY = map(crd[1], 0, 367, 0, height);
      vertex(crdX, crdY);
    }
    endShape(CLOSE);
    //point(obst.getJSONArray(i).getFloat(0), obst.getJSONArray(i).getFloat(1));
  }
  popMatrix();
  rectMode(CENTER);
  JSONArray obst = data.getJSONArray("obst");
  for(int i = 0; i < obst.size(); i++){
    stroke(255);
    //strokeWeight(0.25);
    float crdX = obst.getJSONArray(i).getFloat(0);
    float crdY = obst.getJSONArray(i).getFloat(1);
    noStroke();
    // float crdX = map(obst.getJSONArray(i).getFloat(0), 0, 730 - 1, 0, width - 1);
    // float crdY = map(obst.getJSONArray(i).getFloat(1), 0, 367, 0, height);
    square(crdX, crdY, 40);
  }
  
  save("../maze.png");
}

void draw(){
  //println("finished");
  //endRecord();
  exit();
}
