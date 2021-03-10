JSONObject data;
String dataAdd = "../data/data.json";


void setup(){
  size(730, 367);
  background(0);
  surface.setVisible(false);
  
  data = loadJSONObject(dataAdd);
  pushMatrix();
  translate(width/2, height/2);
  
  JSONArray wall = data.getJSONArray("wall");
  for(int i = 0; i < wall.size(); i++){
    JSONObject fgr = wall.getJSONObject(i);
    boolean clr = fgr.getBoolean("color"); 
    noStroke();
    fill(clr ? 255: 0);
    JSONArray crds = fgr.getJSONArray("coords"); 
    beginShape();
    for(int j = 0; j < crds.size(); j++){
      float[] crd = crds.getJSONArray(j).getFloatArray();
      vertex(crd[0], crd[1]);
    }
    endShape(CLOSE);
    //point(obst.getJSONArray(i).getFloat(0), obst.getJSONArray(i).getFloat(1));
  }
  popMatrix();
  
  JSONArray obst = data.getJSONArray("obst");
  for(int i = 0; i < obst.size(); i++){
    stroke(0);
    strokeWeight(20);
    point(obst.getJSONArray(i).getFloat(0), obst.getJSONArray(i).getFloat(1));
  }
  
  save("../maze.jpg");
}

void draw(){
  exit();
}
