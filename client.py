import server_module.unit_client as unitClient

unit_client = unitClient.UnitClient(1, "127.0.0.1")
unit_client.connectToServer()
unit_client.sendDataToServer({})