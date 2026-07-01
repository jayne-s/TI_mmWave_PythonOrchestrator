using RtttNetClientAPI;
using RstdNet;

public class RadarController {
  
    private readonly RtttClient client;
    private readonly string ip;
    private readonly int port;

    public RadarController(string ip, int port = 2777) {
        this.ip = ip;
        this.port = port;
        this.client = new RtttClient(null); // independent instance
    }

    public bool Connect() {
        return client.Connect(ip, port) == 0;
    }

    public void Disconnect() {
        Console.WriteLine("Disconnecting...");
        int err = client.Disconnect();
        Console.WriteLine($"Disconnect() returned {err}");
      
        err = client.Close();
        Console.WriteLine($"Close() returned {err}");
        Console.WriteLine("Finished disconnect");
    }

    public bool Execute(string lua) {
        var cmd = new RstdNetObject {
            Version = RstdNetConsts.RSTD_NET_VERSION,
            ID = RstdNetCmdID.ScriptCommand,
            Script = lua
        };
      
        int err = client.SendNetCmd(cmd);
        if (err != 0) {
          return false;
        }
      
        RstdNetObject res;
        err = client.ReceiveNetRes(out res);
        return err == 0;
    }

    public bool RunScript(string lua) {
        var cmd = new RstdNetObject {
            Version = RstdNetConsts.RSTD_NET_VERSION,
            ID = RstdNetCmdID.RunScriptCommand,
            Script = lua
        };
      
        int err = client.SendNetCmd(cmd);
        if (err != 0) return false;
      
        RstdNetObject res;
        err = client.ReceiveNetRes(out res);
        return err == 0;
    }
}
