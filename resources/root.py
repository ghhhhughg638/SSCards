from datetime import datetime, timezone
from config import host, IP, version
from datetime import datetime, timezone

class RootResource:
    async def on_get(self, req, resp):
        current_time = datetime.now(timezone.utc)
        server_time_z = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        server_time_z = server_time_z

        endpoints = {
            "draft": f"http://{IP}/draft/",
            "email": f"http://{IP}/email/set",
            "lobbyplayers": f"http://{IP}/lobbyplayers",
            "matches": f"http://{IP}/matches",
            "matches2": f"http://{IP}/matches/v2/",
            "my_draft": None,
            "my_items": None,
            "my_player": None,
            "players": f"http://{IP}/players",
            "purchase": f"http://{IP}/store/v2/txn",
            "root": f"http://{IP}",
            "session": f"http://{IP}/session",
            "store": f"http://{IP}/store/",
            "tourneys": f"http://{IP}/tourney/",
            "transactions": f"http://{IP}/store/txn",
            "view_offers": f"http://{IP}/store/v2/"
        }

        build_info = {
            "build_timestamp": "2025-10-13T17:31:40Z",
            "commit_hash": "dfaf581c",
            "version": version
        }

        host_info = {
            "container_name": "kards-backend-LIVE",
            "docker_image": "618005890699.dkr.ecr.eu-west-1.amazonaws.com/kards-backend:live",
            "host_address": host,
            "host_name": "2a77b085efd1",
            "instance_id": "i-03598bff8bd68fdee"
        }

        auth_header = req.get_header('Authorization')
        if auth_header is None:
            current_user = None
        else:
            current_user = {
                "client_id": 278881,
                "exp": 278881,
                "external_id": "device:Windows-E98A8AD247045B173F7DA08FC0AF9C4D",
                "iat": 1752328020,
                "identity_id": 278881,
                "iss": "",
                "jti": "",
                "language": "zh-Hans",
                "payment": "notavailable",
                "player_id": 278881,
                "provider": "device",
                "roles": [],
                "tier": "LIVE",
                "user_id": 278881,
                "user_name": "device:Windows-E98A8AD247045B173F7DA08FC0AF9C4D"
            }
        root_data = {
            "build_info": build_info,
            "current_user": current_user,
            "endpoints": endpoints,
            "host_info": host_info,
            "server_time": server_time_z,
            "service_name": "kards-backend",
            "tenant_name": "1939-kardslive",
            "tier_name": "LIVE"
        }
        resp.media = root_data
