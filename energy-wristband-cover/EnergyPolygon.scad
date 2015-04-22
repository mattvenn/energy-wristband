
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


resize([43.5,0,30.6], auto=[false,true,false]) scale([1,0.005,1]) linear_extrude(height=20) 
polygon([[00,270], [03,204], [06,160], [09,1257], [12,515], [15,515], [18,447], [21,571], [24,327],[24,0],[0,0]] );