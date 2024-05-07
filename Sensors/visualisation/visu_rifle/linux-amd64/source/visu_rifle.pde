import processing.serial.*;
import processing.opengl.*;
import toxi.geom.*;
import toxi.processing.*;
import processing.net.*;

ToxiclibsSupport gfx;

float[] q = new float[4];
Quaternion quat = new Quaternion(1, 0, 0, 0);

Server server;
int port = 12345;

PShape rifle;

void setup() {
    // 300px square viewport using OpenGL rendering
    size(2000, 2000, OPENGL);
    gfx = new ToxiclibsSupport(this);

    // setup lights and antialiasing
    lights();
    smooth();
  
    server = new Server(this, port);
    
    rifle = loadShape("3D_model_rifle/11737_rifle_v1_L2.obj");
}

void draw() 
{
    background(255);

    Client client = server.available();
    if (client != null) {

        byte[] data = client.readBytes();
        
        if (data != null) 
        {
          q[0] = byteArrayToFloat(data,0);
          q[1] = byteArrayToFloat(data,4);
          q[2] = byteArrayToFloat(data,8);
          q[3] = byteArrayToFloat(data,12);
          
          //println("q:\t" + round(q[0]*100.0f)/100.0f + "\t" + round(q[1]*100.0f)/100.0f + "\t" + round(q[2]*100.0f)/100.0f + "\t" + round(q[3]*100.0f)/100.0f);
          
          quat.set(q[0], q[1], q[2], q[3]);
        }
        
    }
    
    pushMatrix();
    translate(width / 2, height / 2);
    
    float[] axis = quat.toAxisAngle();
    rotate(axis[0],-axis[1], axis[3], axis[2]);
    
    scale(3);
    rotateX(radians(90));
    rotateZ(radians(-90));
    
    shape(rifle);
    popMatrix();
}

float byteArrayToFloat(byte[] bytes, int offset) {
  return Float.intBitsToFloat((bytes[offset + 0] & 0xFF) | 
                              ((bytes[offset + 1] & 0xFF) << 8) | 
                              ((bytes[offset + 2] & 0xFF) << 16) | 
                              ((bytes[offset + 3] & 0xFF) << 24));
} 
