import base64
import json

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string

host = settings.HOST_RQ


class PDFGenerator:
    """Class for prepare and generate pdf file base of order data in check
    and existed template"""

    def __init__(self, data: dict, check):
        self.data: dict = data
        self.check = check
        self.check_type = self.check.type.lower() if self.check else None
        self.file_name = self.__get_filename()

    def __get_filename(self) -> str:
        if self.data and self.check:
            order_id = self.data.get("order_id")
            return f"{order_id}_{self.check_type}"

    def __get_content_for_html(self) -> dict:
        content = {
            "address": self.data["address"],
            "order_id": self.data["order_id"],
            "phone": self.data["client"]["phone"],
            "name": self.data["client"]["name"],
            "items": self.data["items"],
        }
        return content

    def __decode_content_to_b64(self, content: dict) -> str:
        rendered_template = render_to_string(f"{self.check_type}_check.html", content)
        contents = rendered_template.encode("utf-8")
        base64_contents = base64.b64encode(contents).decode()
        return base64_contents

    def __save_pdf_in_model(self, base64_contents: str):
        data = {"contents": base64_contents}
        headers = {"Content-Type": "application/json"}
        response = requests.post(host, data=json.dumps(data), headers=headers)
        self.check.change_check_status("Rendered")
        self.check.pdf_file.save(f"{self.file_name}.pdf", ContentFile(response.content))

    def generate_pdf_from_order(self):
        content = self.__get_content_for_html()
        base64_contents = self.__decode_content_to_b64(content)
        self.__save_pdf_in_model(base64_contents)
