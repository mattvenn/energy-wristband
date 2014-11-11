width = 20;
length = 40;
height = 30;
thick = 3;
elect_thick = 3;

color("blue")
{
difference()
{
    outer();
    inner();

}
translate([0,height/2+thick/2,0])
    cube([length,elect_thick,width],center=true);
}
module outer()
{
    cube([length,height,width],center=true);
    translate([-length/2,0,0])
        cylinder(r=height/2,h=width,center=true);
    translate([length/2,0,0])
        cylinder(r=height/2,h=width,center=true);
}
module inner()
{
    cube([length-thick,height-thick,width+thick],center=true);
    translate([-length/2,0,0])
        cylinder(r=(height-thick)/2,h=width+thick,center=true);
    translate([length/2,0,0])
        cylinder(r=(height-thick)/2,h=width+thick,center=true);
}
