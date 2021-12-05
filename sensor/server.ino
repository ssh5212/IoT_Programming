#include <ESP8266WiFi.h>
#include <Servo.h>
Servo mysv;
int p0 = 0; 

const char* ssid = "iptime_Shins"; // 네트워크 이름

const char* password = "01086659620"; // 네트워크 비밀번호

WiFiServer server(80);


int LED_pin_B = D0; // D3

 


int turn_on = 0;

int turn_off = 1;

void setup() {

  Serial.begin(9600);

  delay(10);
  pinMode(LED_pin_B, OUTPUT);



  digitalWrite(LED_pin_B, turn_off);
  mysv.attach(D0);
 

  // Connect to WiFi network

  Serial.println();

  Serial.println();

  Serial.print("Connecting to ");

  Serial.println(ssid);

 

  WiFi.begin(ssid, password);

 

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");

  }

  Serial.println("");

  Serial.println("WiFi connected");

 

  // Start the server

  server.begin();

  Serial.println("Server started");

 

  // Print the IP address

  Serial.print("Use this URL to connect: ");

  Serial.print("http://");

  Serial.print(WiFi.localIP());

  Serial.println("/");

 

}

 

void loop() {

  // Check if a client has connected

  WiFiClient client = server.available();

  if (!client) {

    return;

  }

 

  // Wait until the client sends some data

  Serial.println("new client");

  while(!client.available()){

    delay(1);

  }

 

  // Read the first line of the request

  String request = client.readStringUntil('\r');

  Serial.println(request);

  client.flush();



 


  int value_B = turn_off;

 



  

 

  if (request.indexOf("/LED_B=ON") != -1)  {

   

    value_B = turn_on;
    mysv.write(180);

  }

  if (request.indexOf("/LED_B=OFF") != -1)  {

    
  mysv.write(-180);
    value_B = turn_off;

  }

 

  // Return the response

  client.println("HTTP/1.1 200 OK");

  client.println("Content-Type: text/html");

  client.println(""); //  do not forget this one

  client.println("<!DOCTYPE HTML>");

  client.println("<html>");

 

  client.println("<meta http-equiv='Content-Type' content='text/html' charset='utf-8'/>");

 




  client.println("<a href=\"/LED_B=ON\"\"><button> 서보모터 ON </button></a>");

  client.println("<a href=\"/LED_B=OFF\"\"><button> 서보모터 OFF </button></a><br/>");

  client.println("</html>");

 

  delay(1);

  Serial.println("Client disonnected");

  Serial.println("");

 

}
