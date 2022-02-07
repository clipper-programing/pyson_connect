import os
import json
from .errors import Errors
import requests
from requests.auth import HTTPBasicAuth

from PIL import Image


class PysonConnect:
    def __init__(self, client_id=None, client_secret=None):
        if client_id == None:
            self.client_id = os.environ["epsonClientID"]

        else:
            self.client_id = client_id

        if client_secret == None:
            self.client_secret = os.environ["epsonClientSecret"]

        else:
            self.client_secret = client_secret

        self.err = Errors()
        self.base_uri = "https://api.epsonconnect.com"
        self.access_token = None
        self.subject_id = None
        self.job_id = None
        self.upload_uri = None
        
    
    def authentification(self, username):
        req_uri = f"{self.base_uri}/api/1/printing/oauth2/auth/token?subject=printer"
        headers = {
                "Content-Type":"application/x-www-form-urlencoded"
                }
        data = {
                "grant_type":"password",
                "username":username,
                "password":""
                }

        r = requests.post(url=req_uri, headers=headers, data=data, auth=HTTPBasicAuth(self.client_id, self.client_secret))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)
            
        else:
            self.access_token = rjson["access_token"]
            expires_in = rjson["expires_in"]
            refresh_token = rjson["refresh_token"]
            self.subject_id = rjson["subject_id"]

            return_data = {
                    "access_token":self.access_token,
                    "expires_in":expires_in,
                    "refresh_token":refresh_token,
                    "subject_id":self.subject_id
                    }
            return return_data


    def reissue_access_token(self, refresh_token):
        req_uri = f"{self.base_uri}/api/1/printing/oauth2/auth/token?subject=printer"
        headers = {
                "Content-Type":"application/x-www-form-urlencoded"
                }
        data = {
                "grant_type":"refresh_token",
                "refresh_token":refresh_token
                }
        r = requests.post(url=req_uri, headers=headers, data=data, auth=HTTPBasicAuth(self.client_id, self.client_secret))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)
            
        else:
            self.access_token = rjson["access_token"]
            expires_in = rjson["expires_in"]
            self.subject_id = rjson["subject_id"]

            return_data = {
                    "access_token":self.access_token,
                    "expires_in":expires_in,
                    "subject_id":self.subject_id
                    }
            return return_data

        
    def get_device_print_capabilities(self, document_type, access_token=None, subject_id=None):
        if not access_token:
            access_token = self.access_token

        if not subject_id:
            subject_id = self.subject_id

        req_uri = f"{self.base_uri}/api/1/printing/printers/{subject_id}/capability/{document_type}"
        headers = {
                "Authorization":f"Bearer {access_token}"
                }
        r = requests.get(url=req_uri, headers=headers)

        rjson = r.json()
        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)

        else:
            return rjson


    def print_setting(self, setting_data, access_token=None, subject_id=None):
        if not access_token:
            access_token = self.access_token

        if not subject_id:
            subject_id = self.subject_id

        req_uri = f"{self.base_uri}/api/1/printing/printers/{subject_id}/jobs"
        headers = {
                "Authorization":f"Bearer {access_token}",
                "Content-Type":f"application/json"
                }
        r = requests.post(url=req_uri, headers=headers, data=json.dumps(setting_data))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)
            
        else:
            self.job_id = rjson["id"]
            self.upload_uri = rjson["upload_uri"]

            return_data = {
                    "job_id":self.job_id,
                    "upload_uri":self.upload_uri
                    }
            return return_data
            

    def upload_print_file(self, file_path, document_type, job_id=None, upload_uri=None):
        l_ext = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".tiff", ".TIFF"]
        dl_data = None

        if "http" in file_path:
            lf_path = file_path.split(".")
            tmp_name = lf_path[-2]
            name = tmp_name.split("/")[-1]
            extension = lf_path[-1]
            dl_data = f"{name}.{extension}"
            r = requests.get(file_path)
            status_code = r.status_code
            if status_code != 200:
                r.raise_for_status()
            
            else:
                data = r.content
                with open(dl_data, "wb") as f:
                    f.write(data)

                file_path = dl_data

        extension = os.path.splitext(file_path)[1]
        name = os.path.splitext(file_path)[0]
        if str(extension) in l_ext:
            exif_img = Image.open(file_path)
            img_data = exif_img.getdata()
            mode = exif_img.mode
            size = exif_img.size

            del_exif = Image.new(mode, size)
            del_exif.putdata(imgData)
            del_exif.save(f"del_{name}{extension}")

            file_path = f"del_{name}{extension}"

        with open(file_path, "rb") as f:
            data = f.read()
            
        date_size = os.path.getsize(file_path)
        if document_type == "document" and date_size < 200000000:
            content_type = "application/octet-stream"
            
        elif document_type == "photo" and date_size < 100000000:
            content_type = "image/jpeg"

        else:
            self.err.errors()

        req_uri = f"{self.upload_uri}&File=1{extension}"
        headers = {
                "Content-Length":str(date_size),
                "Content-Type":content_type
                }
        r = requests.post(url=req_uri, headers=headers, data=data)
        status_code = r.status_code
        
        if status_code != 200:
            self.err.errors(status_code=status_code)
        
        else:
            if dl_data:
                os.remove(dl_data)

            if "del_" in file_path:
                os.remove(file_path)


    def excute_print(self, access_token=None, subject_id=None, job_id=None):
        if access_token == None:
            access_token = self.access_token
            
        if subject_id == None:
            subject_id = self.subject_id

        if job_id == None:
            job_id = self.job_id

        req_uri = f"{self.base_uri}/api/1/printing/printers/{subject_id}/jobs/{job_id}/print"
        headers = {
                "Authorization":f"Bearer {access_token}",
                "Content-Type":"application/json"
                }
        r = requests.post(url=req_uri, headers=headers)
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)


    def cancel_print(self, access_token, subject_id, job_id, opBy="user"):
        req_uri = f"{self.base_uri}/api/1/printing/printers/{subject_id}/jobs/{job_id}/cancel"
        headers = {
                "Authorization":f"Bearer {access_token}",
                "Content-Type":"application/json"
                }
        data = {
                "operated_by":opBy
                }
        r = requests.post(url=req_uri, headers=headers, data=json.dumps(data))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)


    def get_print_job_info(self, access_token=None, subject_id=None, job_id=None):
        if access_token == None:
            access_token = self.access_token

        if subject_id == None:
            subject_id = self.subject_id

        if job_id == None:
            job_id = self.job_id

        req_uri = f"{self.base_uri}/api/1/printing/printers/{subject_id}/jobs/{job_id}"
        headers = {
                "Authorization":f"Bearer {access_token}"
                }
        r = requests.get(url=req_uri, headers=headers)
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)

        else:            
            status = rjson["status"]
            status_reason = rjson["status_reason"]
            start_date = rjson["start_date"]
            job_name = rjson["job_name"]
            ttl_pages = rjson["total_pages"]
            update_date = rjson["update_date"]

            return_data = {
                    "status":status,
                    "status_reason":status_reason,
                    "start_date":start_date,
                    "job_name":job_name,
                    "ttl_pages":ttl_pages,
                    "update_date":update_date
                    }
            return return_data


    def get_device_info(self, access_token=None, subject_id=None):
        if access_token == None:
            access_token = self.access_token

        if subject_id == None:
            subject_id = self.subject_id

        req_uri = f"{self.base_uri}/api/1/printing/printers/{subject_id}"
        headers = {
                "Authorization":f"Bearer {access_token}"
                }
        r = requests.get(url=req_uri, headers=headers)
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)
            
        else:
            printer_name = rjson["printer_name"]
            serial_no = rjson["serial_no"]
            ec_connected = rjson["ec_connected"]

            return_data = {
                    "printer_name":printer_name,
                    "serial_no":serial_no,
                    "ec_connected":ec_connected
                    }
            return return_data


    def cancel_authentication(self, access_token, subject_id):
        req_uri = f"{self.base_uri}/api/1/printing/printers/{subject_id}"
        headers = {
                "Authorization":f"Bearer {access_token}" 
                }
        r = requests.delete(url=req_uri, headers=headers)
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)


    def notification_setting(self, data, access_token=None, subject_id=None):
        if access_token==None:
            access_token = self.access_token

        if subject_id == None:
            subject_id = self.subject_id 

        req_uri = f"{self.base_uri}/api/1/printing/printers/{subject_id}/settings/notification"
        headers = {
                "Authorization":f"Bearer {access_token}",
                "Content-Type":"application/json"
                }
        r = requests.post(url=req_uri, headers=headers, data=json.dumps(data))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)


    def get_scan_destination_list(self, access_token=None, subject_id=None):
        if access_token==None:
            access_token = self.access_token

        if subject_id == None:
            subject_id = self.subject_id 

        req_uri = f"{self.base_uri}/api/1/scanning/scanners/{subject_id}/destinations"
        headers = {
                "Authorization":f"Bearer {access_token}"
                }
        r = requests.get(url=req_uri, headers=headers)
        rjson = r.json()

        dests = []
        dest_data = {}
        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)
            
        else:
            destinations = rjson["destinations"]
            for dest in destinations:
                dest_data["scan_dest_id"] = dest["id"]
                dest_data["alias_name"] = dest["alias_name"]
                dest_data["dest_type"] = dest["type"]
                dest_data["destination"] = dest["destination"]
                dests.append(dest_data)
                dest_data = {}

            return_data = {
                    "destinations":dests
                    }
            return return_data


    def register_scan_destination(self, data, access_token=None, subject_id=None):
        if access_token == None:
            access_token = self.access_token

        if subject_id == None:
            subject_id = self.subject_id

        req_uri = f"{self.base_uri}/api/1/scanning/scanners/{subject_id}/destinations"
        headers = {
                "Authorization":f"Bearer {access_token}",
                "Content-Type":"application/json"
                }
        data = {
                "alias_name":data["alias_name"],
                "type":data["dest_type"],
                "destination":data["destination"]
                }
        r = requests.post(url=req_uri, headers=headers, data=json.dumps(data))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)


    def update_scan_destination(self, data, access_token=None, subject_id=None):
        if access_token == None:
            access_token = self.access_token

        if subject_id == None:
            subject_id = self.subject_id

        req_uri = f"{self.base_uri}/api/1/scanning/scanners/{subject_id}/destinations"
        headers = {
                "Authorization":f"Bearer {access_token}",
                "Content-Type":"application/json"
                }
        data = {
                "id":data["scan_dest_id"],
                "alias_name":data["alias_name"],
                "type":data["dest_type"],
                "destination":data["destination"]
                }
        r = requests.put(url=req_uri, headers=headers, data=json.dumps(data))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)

    
    def delete_scan_destination(self, access_token, subject_id, scan_dest_id):
        req_uri = f"{self.base_uri}/api/1/scanning/scanners/{subject_id}/destinations"
        headers = {
                "Authorization":f"Bearer {access_token}",
                "Content-Type":"application/json"
                }
        data = {
                "id":scan_dest_id
                }
        r = requests.delete(url=req_uri, headers=headers, data=json.dumps(data))
        rjson = r.json()

        if "error" in rjson or "code" in rjson:
            key = list(rjson.keys())[0]
            message = rjson[key]
            self.err.errors(message=message)
