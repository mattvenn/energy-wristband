
/*

Draws a polygon based on 2 days data useage from Matts current cost feed

curl 'https://user:pass@api.xively.com/v2/feeds/130883.csv?start=2015-03-28T00:00:00&duration=24hours&interval_type=discrete&interval=10800'

Text then stripped down to coordinates

You'll need to change user and pass, obviously.

Polygon printed and snap fits to energy-wristband-cover

*/

// Energy Cover Outer Dimensions; the base for our polygon
x1 = 43.5;
y1 = 30.6;
screwdepth = 1.5;


polygonpins();
//button_viewer();




module polygonpins(){

mypolygon();
//rotate([270,270,180])cylinder(h=10,r=2, $fn=16);
mypins(1.7, 2.93, 2.76);
}


module mypolygon(){

resize([x1,0,y1], auto=[false,true,false]) scale([1,0.005,1]) linear_extrude(height=20) 
polygon([[00,270], [03,204], [06,160], [09,1257], [12,515], [15,515], [18,447], [21,571], [24,327],[24,0],[0,0]] );

}



module mypins(screwdiameter, xdistfromcorner, ydistfromcorner){
//position of button hole and radii of screws & buttons
xbuttondistfromedge = 7;
//offet from centre on y axis of the button
ybuttondistfromcentre = 0.96;
buttondiameter = 3;
buttonradius = buttondiameter/2;
screwradius = screwdiameter/2;
//position of recess to view the LEDs
leddistfromedge = 18;
 

translate([0+xdistfromcorner, 0,0+xdistfromcorner])rotate([270,270,180])cylinder(h = screwdepth, r=screwradius,center=false, $fn=16);
translate([0+xdistfromcorner, 0,y1-xdistfromcorner])rotate([270,270,180])cylinder(h = screwdepth, r=screwradius,center=false, $fn=16);
translate([x1-xdistfromcorner, 0,0+xdistfromcorner])rotate([270,270,180])cylinder(h = screwdepth, r=screwradius,center=false, $fn=16);
translate([x1-xdistfromcorner, 0,y1-xdistfromcorner])rotate([270,270,180])cylinder(h = screwdepth, r=screwradius,center=false, $fn=16);


}

module button_viewer(){

translate([x1+xbuttondistfromedge,y1 ,y1])rotate([270,270,180])cylinder(h=10, r=buttonradius,center=false, $fn=24);
//ledviewer
translate([x1+leddistfromedge, 0.5,x1+leddistfromedge])rotate([270,270,180])roundCornersCube(3,13,10,5);
}
