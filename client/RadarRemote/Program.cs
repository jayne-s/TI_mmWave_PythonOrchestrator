using System;
using RtttNetClientAPI;

class Program {
    static void Main(string[] args) {
      
        var radar1 = new RadarController("XXX.XXX.X.XXX"); // replace with host IP
        radar1.Connect();
      
        foreach (string line in File.ReadLines("radar_commands.lua")) {
            radar1.Execute(line);
        }
        
        radar1.Disconnect();
    }
}
