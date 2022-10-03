import server_module.unit_client as unitClient

unit_client = unitClient.UnitClient(1, "192.168.1.37")
unit_client.connectToServer()
unit_client.sendDataToServer({})