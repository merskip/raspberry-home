from raspberry_home.display.epd.epd_commands import EPD2in7Commands
from raspberry_home.display.epd.epd_hardware import EPDHardware
from raspberry_home.display.epd.epd_lut import EPDLUTSetBase


class EPD2in7Driver:
    """
    - Datasheet: https://www.waveshare.com/w/upload/d/d8/2.7inch-e-paper-b-specification.pdf
    - Hacking E-paper: https://benkrasnow.blogspot.com/2017/10/fast-partial-refresh-on-42-e-paper.html
    """

    width = 264
    height = 176

    def __init__(self, hardware: EPDHardware):
        self._hardware = hardware

    def init_sequence(self, lut: EPDLUTSetBase):
        self._hardware.setup()
        self._hardware.hard_reset()

        # 5. Power ON  (p. 13)
        self._hardware.send(EPD2in7Commands.POWER_ON)
        self._hardware.wait_until_idle()

        # 1. Panel Setting  (p. 11)
        # RES[7..6] - Display resolution setting - 296x160 (source x gate)
        # +LUT_EN[5] - Color selecting setting - Using LUT from register
        # -BWR[4] - Pixel with B/W/Red. Run both LU1 and LU2.
        # +UD[3] - Scan up - G1 -> ... -> Gn
        # +SHL[2] - Shift right - S1 -> ... -> Sn
        # +SHD_N[1] - Booster switch - Booster ON (?)
        # +RST_N[0] - Soft Reset - Booster OFF (?)
        self._hardware.send(EPD2in7Commands.PANEL_SETTING, [0xAF])

        # 21. PLL control (PLL) (p. 18)
        # SEL_DIV[6..5] - 01
        # SELf_F[4..0] - 11010
        # 0x3A - 100HZ (?)
        self._hardware.send(EPD2in7Commands.PLL_CONTROL, [0x3A])

        # 2. Selecting Internal/External Power (p. 11)
        # +VDS_EN - Internal DC/DC function for generate VDH/VDL
        # +VDG_END - Internal DC/DC function for generate VGH/VGL
        # VCOM_HV - VCOMH = VDH + VCOMDC, VCOML = VHL + VCOMDC
        # VGHL_LV - VGH=16V, VGL= -16V
        # VDH  - +11.0V (B/W pixel)
        # VDL  - -11.0V (B/W pixel)
        # VDHR -  +4.2V (red pixel)
        self._hardware.send(EPD2in7Commands.POWER_SETTING, [
            0x03,  # +VDS_EN, +VDG_END
            0x00,  # VCOM_HV, VGHL_LV
            0x2B,  # VDH
            0x2B,  # VDL
            0x09,  # VDHR
        ])

        # 7. Booster Soft Start (BTST) (p. 13)
        # BT_PHA[7..6] - Soft start period of phase A - 10 ms
        # BT_PHA[5..3] - Driving strength of phase A - strength 1
        # BT_PHA[2..0] - Minimum OFF time setting of GDR in phase A - 6.58us
        # BT_PHB[7..6] - Soft start period of phase B - 10 ms
        # BT_PHB[5..3] - Driving strength of phase B - strength 1
        # BT_PHB[2..0] - Minimum OFF time setting of GDR in phase B - 6.58us
        # BT_PHC[5..3] - Driving strength of phase C - strength 3
        # BT_PHC[2..0] - Minimum OFF time setting of GDR in phase C - 6.58us
        self._hardware.send(EPD2in7Commands.BOOSTER_SOFT_START, [
            0x07,  # BT_PHA[7...0]
            0x07,  # BT_PHB[7...0]
            0x17,  # BT_PHC[5...0]
        ])

        # Undocumented command - Power optimization
        # Some magic values
        self._hardware.send(EPD2in7Commands.POWER_OPTIMIZATION, [0x60, 0xA5])
        self._hardware.send(EPD2in7Commands.POWER_OPTIMIZATION, [0x89, 0xA5])
        self._hardware.send(EPD2in7Commands.POWER_OPTIMIZATION, [0x90, 0x00])
        self._hardware.send(EPD2in7Commands.POWER_OPTIMIZATION, [0x93, 0x2A])
        self._hardware.send(EPD2in7Commands.POWER_OPTIMIZATION, [0x73, 0x41])

        # 34. VCM_DC Setting register (p. 24)
        # VDCS[6..0] - -1.0V
        self._hardware.send(EPD2in7Commands.VCM_DC_SETTING_REGISTER, [0x12])

        # 26. VCOM and Data Interval Setting (p. 24)
        # VBD[7..6] - ?
        # DDX[5..4] - ?
        # CDI[3..0] - ?
        self._hardware.send(EPD2in7Commands.VCOM_AND_DATA_INTERVAL_SETTING, [0x87])

        # Set LUT

        assert len(lut.vcom_dc) == 44
        self._hardware.send(EPD2in7Commands.LUT_FOR_VCOM, lut.vcom_dc)

        assert len(lut.ww) == 42
        self._hardware.send(EPD2in7Commands.LUT_WHITE_TO_WHITE, lut.ww)

        assert len(lut.bw) == 42
        self._hardware.send(EPD2in7Commands.LUT_BLACK_TO_WHITE, lut.bw)

        assert len(lut.bb) == 42
        self._hardware.send(EPD2in7Commands.LUT_WHITE_TO_BLACK, lut.bb)

        assert len(lut.wb) == 42
        self._hardware.send(EPD2in7Commands.LUT_BLACK_TO_BLACK, lut.wb)

        # 15. Partial Display Refresh (p. 17)
        # (x, y, width, height) = (0, 0, 0, 0)
        self._hardware.send(EPD2in7Commands.PARTIAL_DISPLAY_REFRESH, [0x00])

    def display(self, image_black, image_red):
        self._send_transmission(EPD2in7Commands.DATA_START_TRANSMISSION_1,
                                self._image_to_buffer(image_black))
        self._send_transmission(EPD2in7Commands.DATA_START_TRANSMISSION_2,
                                self._image_to_buffer(image_red))
        self._hardware.send_command(EPD2in7Commands.DISPLAY_REFRESH)
        self._hardware.wait_until_idle()

    def _image_to_buffer(self, image):
        assert image.size == (self.width, self.height)

        buffer_size = (self.width * self.height) // 8  # Each byte describes 8 pixels
        buffer = [0x00] * buffer_size  # Buffer filled with black/red color, bit 1 - black/red, 0 - white
        image_pixels = image.convert('1').load()

        for image_y in range(self.height):
            for image_x in range(self.width):
                if image_pixels[image_x, image_y] == 0:  # If pixel is black/red
                    x = image_y
                    y = self.width - image_x - 1
                    buffer_index = (x + y * self.height) // 8
                    buffer[buffer_index] |= 0x80 >> (image_y % 8)  # Set only one bit inside buffer
        return buffer

    def _send_transmission(self, command: int, data: list):
        assert command == EPD2in7Commands.DATA_START_TRANSMISSION_1 \
               or command == EPD2in7Commands.DATA_START_TRANSMISSION_2
        assert len(data) == self.width * self.height / 8

        self._hardware.send_command(command)
        self._hardware.send_data(data)
        self._hardware.send_command(EPD2in7Commands.DATA_STOP)

    def deep_sleep(self):
        self._hardware.send(EPD2in7Commands.VCOM_AND_DATA_INTERVAL_SETTING, [0xF7])
        self._hardware.send(EPD2in7Commands.POWER_OFF)
        self._hardware.send(EPD2in7Commands.DEEP_SLEEP, [0xA5])
