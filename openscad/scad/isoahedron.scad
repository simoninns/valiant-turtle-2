////////////////////////////
// icosahedron
// by skitcher
////////////////////////////

/* [Customizer Parameters] */

// Edge length
Edge_length=40;

// Resolution
Resolution=45;

// Corner radius
Corner_radius=5;



/* [Hidden] */
phi=(1 + sqrt(5)) / 2;
$fn=Resolution;
s=Edge_length/2-Corner_radius/1.5;
r=Corner_radius;
s2=s*phi;



//translate([0,0,25]) cube(20 ,true);

hull(){
    
    translate([s,0,s2]) sphere(r);
    translate([s,0,-s2]) sphere(r);
    
    translate([-s,0,s2]) sphere(r);
    translate([-s,0,-s2]) sphere(r);
    
    translate([s2,s,0]) sphere(r);
    translate([-s2,s,0]) sphere(r);
    
    translate([s2,-s,0]) sphere(r);
    translate([-s2,-s,0]) sphere(r);
    
    translate([0,s2,s]) sphere(r);
    translate([0,s2,-s]) sphere(r);
    
    translate([0,-s2,s]) sphere(r);
    translate([0,-s2,-s]) sphere(r);
    
    
}


// Or maybe this...

// phi value: don't change this
phi=(1 + sqrt(5)) / 2;
// -phi makes regular dodecahedron, 1 makes rhombic dodecahedron.
h=-phi; //[-phi,1]
// Resolution
$fn=50;
// Sphere radius
D=0.3;
// Overall scale
scle=1;

/*[Hidden]*/
s=1;

scale([scle,scle,scle]){
    hull(){
      
        translate([0, (1 + h), (1 - h*h)]) sphere(D);
        translate([0, -(1 + h), (1 - h*h)]) sphere(D);
        translate([0, (1 + h), -(1 - h*h)]) sphere(D);
        translate([0, -(1 + h), -(1 - h*h)]) sphere(D);
        
        
        
        translate([(1 + h), (1 - h*h), 0]) sphere(D);
        translate([-(1 + h), (1 - h*h), 0]) sphere(D);
        translate([(1 + h), -(1 - h*h), 0]) sphere(D);
        translate([-(1 + h), -(1 - h*h), 0]) sphere(D);
        
        translate([(1 - h*h), 0, (1 + h)]) sphere(D);
        translate([(1 - h*h), 0, -(1 + h)]) sphere(D);
        translate([-(1 - h*h), 0, (1 + h)]) sphere(D);
        translate([-(1 - h*h), 0, -(1 + h)]) sphere(D);
  
        
        
        
        translate([s,s,s]) sphere(D);
        translate([-s,s,-s]) sphere(D);
        translate([s,s,-s]) sphere(D);
        translate([-s,-s,s]) sphere(D);
        translate([s,-s,-s]) sphere(D);
        translate([-s,s,s]) sphere(D);
        translate([s,-s,s]) sphere(D);
        translate([-s,-s,-s]) sphere(D);
        
        
    }
}