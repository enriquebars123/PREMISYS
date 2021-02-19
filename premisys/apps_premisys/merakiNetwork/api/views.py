from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from meraki_sdk.meraki_sdk_client import MerakiSdkClient
from meraki_sdk.exceptions.api_exception import APIException

x_cisco_meraki_api_key = '6bddd12b674553917ce03126f794c4c63272a45b'
meraki = MerakiSdkClient(x_cisco_meraki_api_key)

class merakiOrganizations(APIView):
    
    def get(self, request, format=None):
     
        orgs = meraki.organizations.get_organizations()
        return Response(orgs,status.HTTP_200_OK)

class merakiNetworks(APIView):
    
    def get(self, request, pk, format=None):
        params = {}
        params["organization_id"] = pk  # Demo Organization "DevNet Sandbox"
        nets = meraki.networks.get_organization_networks(params)
        return Response(nets,status.HTTP_200_OK)

class merakiDevices(APIView):
    
    def get(self, request, pk, format=None):
        devices = meraki.devices.get_network_devices(pk)
        return Response(devices,status.HTTP_200_OK)

class merakiClient(APIView):

    def get(self, request, pk , format=None):
        
        collect = {}
        collect['network_id'] = pk
        collect['per_page'] = 999
        result = meraki.clients.get_network_clients(collect)
        print("entre aki ")
        print(len(result))
        
        return Response(result,status.HTTP_200_OK)

class get_network_clients_connection_stats(APIView):
    
    def get(self, request, format=None):
        
        collect = {}

        serial = 'Q2KD-GUX8-5A6V'
        collect['serial'] = serial
        
        #t_0 = 't0'
        #collect['t0'] = t_0
        
        result = meraki.clients.get_device_clients(collect)
        print(len(result))
        """
        collect = {}

        network_id = 'L_677228793965839990'
        collect['network_id'] = network_id

        #t_0 = 't0'
        #collect['t_0'] = t_0

        #t_1 = 't1'
        #collect['t_1'] = t_1

        timespan = 17574
        collect['timespan'] = timespan
        
        ssid = 6
        collect['ssid'] = ssid

        #vlan = 190
        #collect['vlan'] = vlan

        #ap_tag = 'apTag'
        #collect['ap_tag'] = ap_tag
        
        result= meraki.wireless_health.get_network_clients_connection_stats(collect)
        """
        #result= meraki.wireless_health.get_network_devices_connection_stats(collect)
        
        return Response(result,status.HTTP_200_OK)

class get_network_ssids(APIView):
    
    def get(self, request, format=None):
        
        collect = {}

        network_id = 'L_677228793965839990'
        collect['network_id'] = network_id

        result= meraki.ssids.get_network_ssids(network_id)

        return Response(result,status.HTTP_200_OK)