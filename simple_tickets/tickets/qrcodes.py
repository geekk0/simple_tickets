from PIL import Image

import qrcode


class TicketQRCode:
    def __init__(self, qr_data):
        self.data = qr_data
        self.image = None
        self.qr_service = qrcode.QRCode(version=1,
                                     error_correction=qrcode.constants.ERROR_CORRECT_L,
                                     box_size=10,
                                     border=4,
        )
        self.qr_service.add_data(self.data)

    def create_qr_code_image(self):
        self.qr_service.make(fit=True)
        self.qr_service.make_image(fill_color="black", back_color="white").save("qr_temp.png")


def paste_qr_code(background_image_path, qr_data, output_image_path, qr_position):
        # Open the background image
        background = Image.open(background_image_path)

        qr_position = get_qrcode_position(background.size)

        qr_hor = qr_position[0]
        qr_ver = qr_position[1]

        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=2,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Calculate the position to paste the QR code
        qr_position_x, qr_position_y = qr_position

        # Paste the QR code onto the background image
        background.paste(qr_image, (qr_position_x, qr_position_y))

        # Save the resulting image
        background.save(output_image_path)


def get_qrcode_position(background_image_size):
    qrcode_x_position = round(background_image_size[0] / 100 * 5)
    qrcode_y_position = round(background_image_size[1] / 100 * 90)
    return [qrcode_x_position, qrcode_y_position]


# Example usage
if __name__ == "__main__":
    background_image_path = "background_image.jpg"
    qr_data = "https://example.com"
    output_image_path = "output_image.png"
    qr_position = (30, 220)

    paste_qr_code(background_image_path, qr_data, output_image_path, qr_position)

# # Create an instance of QRCode
# qr_code = QRCode("https://example.com")
#
# # Generate the QR code image
# qr_code.create_qr_code_image()
#
# # Show the resulting QR code image
# if qr_code.image:
#     qr_code.image.show()
# else:
#     print("QR code image has not been generated yet.")





