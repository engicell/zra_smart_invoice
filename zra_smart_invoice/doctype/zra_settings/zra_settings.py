
import frappe
from frappe.model.document import Document
import requests

class ZRASettings(Document):
    def fetch_device_keys(self):
        payload = {
            "tpin": self.tpin,
            "bhfId": self.bhf_id,
            "dvcSrlNo": self.dvc_serial_no
        }
        try:
            url = f"{self.api_base_url}/zraVsdc_v1TestLatest/initializer/selectInitInfo"
            res = requests.post(url, json=payload)
            if res.status_code == 200:
                data = res.json().get("data", {}).get("info", {})
                self.intrl_key = data.get("intrlKey")
                self.sign_key = data.get("signKey")
                self.cmc_key = data.get("cmcKey")
                frappe.msgprint("Keys successfully fetched from ZRA API.")
            else:
                frappe.throw(f"Error from ZRA API: {res.text}")
        except Exception as e:
            frappe.log_error(str(e), "ZRA API Fetch Error")
            frappe.throw("Failed to connect to ZRA API.")
