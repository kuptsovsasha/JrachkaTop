from JrachkaTop.ticket_service_api.pdf_generator import PDFGenerator


def task_convert_order_to_pdf(data, check):
    generate_pdf = PDFGenerator(data, check)
    generate_pdf.generate_pdf_from_order()
