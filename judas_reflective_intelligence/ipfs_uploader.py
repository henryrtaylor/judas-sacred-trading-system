import os
import requests

NFT_STORAGE_KEY = os.getenv("NFT_STORAGE_KEY")

def upload_to_ipfs(file_path):
    headers = {
        "Authorization": f"Bearer {NFT_STORAGE_KEY}"
    }
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post("https://api.nft.storage/upload", headers=headers, files=files)
    if response.status_code == 200:
        cid = response.json()["value"]["cid"]
        return f"https://{cid}.ipfs.nftstorage.link"
    else:
        raise Exception(f"IPFS upload failed: {response.text}")