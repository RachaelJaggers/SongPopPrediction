int Y_AXIS = 1;
int X_AXIS = 2;  
color b1, b2;
color c2,c3;
int area_w = 700;
int area_h = 700;
PFont f;
Table songData;

ArrayList songList;
int rows = 0;
int max_year = 2010;
int min_year = 1980;
String mode = "Top 10%";
int curMode = 3;

void loadData(int data)
{
  switch(data)
  {
    case 0:
    //80s
        //Load in Music
      songList.clear();
      songData = loadTable("80s_songs.csv");
      rows = songData.getRowCount();
      
      min_year = 1980;
      max_year = 1990;
      mode = "80s";
     break;
   case 1:
    //90s
        //Load in Music
      songList.clear();
      songData = loadTable("90s_songs.csv");
      rows = songData.getRowCount();
      
      min_year = 1990;
      max_year = 2000;
      mode = "90s";

     break;
   case 2:
    //00s
        //Load in Music
      songList.clear();
      songData = loadTable("00s_songs.csv");
      rows = songData.getRowCount();
      
      min_year = 2000;
      max_year = 2010;
      mode = "00s";

     break;
   case 3:
    //top
        //Load in Music
      songList.clear();
      songData = loadTable("top_songs.csv");
      rows = songData.getRowCount();
      
      min_year = 1980;
      max_year = 2010;
      mode = "Top 10%";

     break;
  }
  

  //Set-up all the grids
  int i = 0;
  for(TableRow row: songData.rows()) {
    int year= row.getInt(0);
    String name = row.getString(1);
    String artist = row.getString(2);
    
    float pop_score = row.getFloat(3);
 
 
    songList.add(new Song(i, year, name, artist, pop_score));

    i++;
  }
}

void setup()  {
  size(1100,800); 
   
   
   songList = new ArrayList();
   
   //Setup font
  f = createFont("Arial",16,true); // Arial, 16 point, anti-aliasing on
  //textFont(f,36);
  
  
  loadData(curMode);
  println("Done!\n");
}

void keyPressed() {
  if (key == CODED) {
    if (keyCode == LEFT) {
      curMode = (curMode - 1);
      if(curMode < 0) {
       curMode = 3; 
      }
    } else if (keyCode == RIGHT) {
      curMode = (curMode + 1) % 4;
    }
    loadData(curMode);
  }
}

int id_sel = -1;
void draw() {
  background(255);
  setGradient(50,50, area_w, area_h, b1, b2, Y_AXIS);
  b1 = color(222, 235, 247);
  b2 = color(8, 48, 107);
  c3 = color(204, 102, 0);
  c2 = color(0,0,0);

  //Axis
  stroke(c2);
  smooth(2);
  strokeCap(PROJECT);
  line(50, 50, 50, area_h+50);
  line(50,50, area_w+50, 50);
  strokeWeight(4);  // Thicker
  line(50, area_h+50, area_w+50, area_h+50);
  line(area_w+50, 50, area_w+50, area_h+50);
  
  rectMode(CORNER);
  //Low X-Marker
  line(50, area_h+50-10, 50, area_h+50+10);
  textFont(f, 16);
  text(str(min_year), 50+3, height-50+15, 200, 400);

  //High X-Marker
  line(area_w+50, area_h+50-10, area_w+50, area_h+50+10);
  text(str(max_year), area_w+20, height-50+15, 200, 400);

  //Low Y-Marker -- 0.0
  line(area_w+50-10, area_h+50, area_w+50+10, area_h+50);
  text("0.0", area_w+50+12, area_h+50, 200, 400);

  //Mid Y-Marker -- 0.5
  line(area_w+50-10, (area_h+50)/2, (area_w+50)+10, (area_h+50)/2);
  text("0.5", area_w+50+12, ((area_h+50)/2)-10, 200, 400);
  
  //High Y-Marker -- 1.0
  line(area_w+50-10, 50, area_w+50+10, 50);
  text("1.0", area_w+50+12,50, 200, 400);


  
  for(int i = 0; i < songList.size(); ++i)
  {
    Song s = (Song)songList.get(i);
    s.display();
    s.mouseCheck();
    //break;
  }
  //Year
  //Danceability
  //Duration
  //Energy
  //Key
  //Hotttnesss
  //Tempo
  //Time Signature
  
  //Song Info Area
    noFill();

  strokeWeight(2);
  stroke(color(0,0,0));
  rectMode(CORNER);
  rect(area_w+50+25+70, 50, 200, 130, 3);
  int song_x = area_w+50+25+72;
  int song_y = 50;
  //Song - Artist
  String name = "Song";
  String artist = "Artist";
  String year = "2013";
  String pop_score = "0.5";
  
  String view_count = "1,000,000";
  String like_count = "20";

  if(id_sel != -1)
  {
    //Set all the strings
    Song song = (Song)songList.get(id_sel);

    name = song.song;
    artist = song.artist; 
    year = str(song.year);
    pop_score = str(song.pop_score);
  }
  textFont(f,18);
  text(name, song_x, song_y, 200, 21);
  textFont(f,16);
  text(artist, song_x, song_y+30, 200, 21);
  text("Year: " + year, song_x, song_y+70, 200, 21);
  text("Popularity " + pop_score, song_x, song_y+110, 200, 21);


  
  rectMode(CENTER);
  textFont(f, 32);
  text(mode, (area_w+50+25+240)+(130/2), 500,400,41);
  //text("YouTube View Count: \n" + view_count, song_x, song_y+200, 200, 51);
 // text("YouTube Like Count: \n" + like_count, song_x, song_y+250, 200, 51);

 // text(name_artist, song_x+40, song_y, 200, 21);
 // text(name_artist, song_x, song_y, 200, 21);

}

void setGradient(int x, int y, float w, float h, color c1, color c2, int axis ) {

  noFill();

  if (axis == Y_AXIS) {  // Top to bottom gradient
    for (int i = y; i <= y+h; i++) {
      float inter = map(i, y, y+h, 0, 1);
      color c = lerpColor(c1, c2, inter);
      stroke(c);
      line(x, i, x+w, i);
    }
  }  
  else if (axis == X_AXIS) {  // Left to right gradient
    for (int i = x; i <= x+w; i++) {
      float inter = map(i, x, x+w, 0, 1);
      color c = lerpColor(c1, c2, inter);
      stroke(c);
      line(i, y, i, y+h);
    }
  }
}

class Song {
  int ident; 
  int year;
  String song;
  String artist;
  float pop_score;
  
  int x, y;

  Song(int _ident, int _year, String _song, String _artist, float _pop_score) {
    ident = _ident;
    year = _year;
    song = _song;
    artist = _artist;
    pop_score = _pop_score;
      
   int min_space_x = 50;
   int max_space_x = area_w+50;
  
   int max_space_y = 50;
    int min_space_y = area_h+50;
    float norm_year = float(year - min_year)/float(max_year-min_year);
    println ("Norm :" + norm_year);
    x = int(norm_year*float(area_w)) + 50;
    y = int(((1.0-pop_score)*float(area_h))) + 50;
    
  } 
 
 //Simple draw function
 void display() {
   noStroke();
   fill(c3);
   rectMode(CENTER);
   rect(x, y, 5, 5);
   //println("X: "+x + ", Y: " + y);
 }
 
 //Checks bounds
 void mouseCheck()
 {
   
   if (mouseX >= x && mouseX <= x+10 && mouseY >= y && mouseY <= y+10) {
     id_sel = ident;
   }
   
 }
}
