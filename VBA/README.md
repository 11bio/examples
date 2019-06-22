# 11B SPOT API VBA Example

Example of REST usage in EXCEL VBA Macros.

In addition to general token retrieval steps, you need to install two dependencies, json parser and dictionary.

Import JsonConverter.bas from:

[VBA-JSON](https://github.com/VBA-tools/VBA-JSON)

Import Dictionary.cls from:

[VBA-Dictionary](https://github.com/VBA-tools/VBA-Dictionary)


Insert your token in the macros module:

```
  Dim ws As Worksheet
  Set ws = Worksheets(s)
  ws.Cells.Clear
  Dim oRequest As Object
  Set oRequest = CreateObject("WinHttp.WinHttpRequest.5.1")
  oRequest.Open "GET", "https://api.demo.11b.io/api/v1/" + u, False
  oRequest.SetRequestHeader "Content-Type", "application/json", "Accept", "application/json" ''Content-Type: application/json'
  oRequest.SetRequestHeader "Authorization", "Bearer 59b3671b-4074-4c53-ba77-db9f01ed1e61"
  oRequest.Send
```


![11B-SPOT-VBA-Example.gif](https://11bio.github.io/examples/11B-SPOT-VBA-Example.gif "11B-SPOT-VBA-Example")


Enjoy,
11B.io Team