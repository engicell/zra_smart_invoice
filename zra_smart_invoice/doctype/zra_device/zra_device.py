
import frappe
from frappe.model.document import Document
import requests

class ZRADevice(Document):
    def validate(self):
        self.init_device()

    def init_device(self):
        settings = frappe.get_single("ZRA Settings")
        payload = {
            "tpin": settings.tpin,
            "bhfId": settings.bhf_id,
            "dvcSrlNo": settings.dvc_serial_no
        }
        try:
            url = f"{settings.api_base_url}/zraVsdc_v1TestLatest/initializer/selectInitInfo"
            res = requests.post(url, json=payload)
            if res.status_code == 200:
                data = res.json().get("data", {}).get("info", {})
                self.intrl_key = data.get("intrlKey")
                self.sign_key = data.get("signKey")
                self.cmc_key = data.get("cmcKey")
            else:
                frappe.throw(f"Error from ZRA: {res.text}")
        except Exception as e:
            frappe.log_error(str(e), "ZRA Init Error")
