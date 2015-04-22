
/*

Modified use of Sergio Vilches RoundedCornersCube Modules for OpenSCAD to generate cover for Matt Venn's EnergyWristband project https://github.com/mattvenn/energy-wristband

http://codeviewer.org/view/code:1b36 
Copyright (C) 2011 Sergio Vilches
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
Contact: s.vilches.e@gmail.com


    ----------------------------------------------------------- 
                 Round Corners Cube (Extruded)                
      roundCornersCube(x,y,z,r) Where:                        
         - x = Xdir width                                     
         - y = Ydir width                                     
         - z = Height of the cube                             
         - r = Rounding radious                               
                                                              
      Example: roundCornerCube(10,10,2,1);                    
     *Some times it's needed to use F6 to see good results!   
 	 ----------------------------------------------------------- 
*/

// Main Box Inner Dimensions
x1=41.5;
y1 = 28.3;
//height of cover flush with base or board
//allowing 0.5mm for lipo battery
z1=8;
//rounding radius
r = 1.6;
//thickness of case
thickness = 2;
//distance from base of the usb port
usbheightfrombase = 1.79;

//remove the srew hole and button material 
difference(){
mycover();
myscrews_button(1.85, 2.93, 2.76);
}


//custom module definitions

module myscrews_button(screwdiameter, xdistfromcorner, ydistfromcorner){
//position of button hole and radii of screws & buttons
xbuttondistfromedge = 7;
//offet from centre on y axis of the button
ybuttondistfromcentre = 0.96;
buttondiameter = 3;
buttonradius = buttondiameter/2;
screwradius = screwdiameter/2;
//position of recess to view the LEDs
leddistfromedge = 18;

	translate([x1/2-xdistfromcorner, y1/2-ydistfromcorner,(z1/2)-z1])cylinder(h=z1*2, r=screwradius,center=false, $fn=24);
translate([-x1/2+xdistfromcorner, y1/2-ydistfromcorner,(z1/2)-1])cylinder(h=10, r=screwradius,center=false, $fn=24);
translate([x1/2-xdistfromcorner, -y1/2+ydistfromcorner,(z1/2)-1])cylinder(h=10, r=screwradius,center=false, $fn=24);
translate([-x1/2+xdistfromcorner, -y1/2+ydistfromcorner,(z1/2)-1])cylinder(h=10, r=screwradius,center=false, $fn=24);
//button hole
translate([x1/2-xbuttondistfromedge, ybuttondistfromcentre,(z1/2)-1])cylinder(h=z1, r=buttonradius,center=false, $fn=24);
//ledviewer
translate([x1/2-leddistfromedge, 0.5,(z1/2)-1])roundCornersCube(3,13,z1/2-0.25,1);

}

//remove the usb port material

module mycover(){
difference(){
mybox();
translate([(x1/2)-(7.9*2),-(y1/2)-2 ,(-z1/2)+(usbheightfrombase)])myusb();
}
}

// the basic box
module mybox(){
 difference(){
	roundCornersCube(x1+thickness, y1 + thickness, z1 + thickness,r);
	translate ([0, 0,(z1/2)-5])roundCornersCube(x1,y1,z1+thickness,r);
}
}

//the microusbcharger port
module myusb(){	
usbx = 9;
usby = 3;
usbz = 3;

cube([usbx, usby, usbz], center = false);
}

//original module functions Copyright (C) 2011 Sergio Vilches

module createMeniscus(h,radius) 
// This module creates the shape that needs to be substracted from a cube to make its corners rounded.
//basicly the difference between a quarter of cylinder and a cube
difference(){        

   translate([radius/2+0.1,radius/2+0.1,0]){
      cube([radius+0.2,radius+0.1,h+0.2],center=true);         // All that 0.x numbers are to avoid "ghost boundaries" when substracting
   }

   cylinder(h=h+0.2,r=radius,$fn = 25,center=true);
}


module roundCornersCube(x,y,z,r)  // Now we just substract the shape we have created in the four corners
difference(){
   cube([x,y,z], center=true);

translate([x/2-r,y/2-r]){  // We move to the first corner (x,y)
      rotate(0){  
         createMeniscus(z,r); // And substract the meniscus
      }
   }
   translate([-x/2+r,y/2-r]){ // To the second corner (-x,y)
      rotate(90){
         createMeniscus(z,r); // But this time we have to rotate the meniscus 90 deg
      }
   }
      translate([-x/2+r,-y/2+r]){ // ... 
      rotate(180){
         createMeniscus(z,r);
      }
   }
      translate([x/2-r,-y/2+r]){
      rotate(270){
         createMeniscus(z,r);
      }
   }
}



