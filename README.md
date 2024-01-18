# NordPoolLights

A solution that controls (turns on/off) a xiaomi smart socket based on current NORDPOOL electricity price.

### Main technology

- Python3
- AWS (Serverless)
- Terraform
- Xiaomi & Nordpool APIs

### Warning

Xiaomi API does not work in the cloud, it does not return "userId" and requires to verify 
email every time an authentication is initiated. This is a protective mechanism by Xiaomi developers.
Additionally, as it turns out, in order to control a smart device, you need to be connected to the
same wifi as the device (in order to utilize local network). All in all, the solution does not work
and can not work - probably something like local raspberry pi with wifi connection is the way to go.