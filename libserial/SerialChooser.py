import gtk
import logging

LOG = logging.getLogger('libserial.SerialChooser')
DUMMY_PORT = "Select Serial Port"

class SerialChooser(gtk.HBox):
    """
    A composite Gtk widget containg a gtk.ComboBox
    that lists available serial ports, and a icon indicating
    whether the port is connected or not
    """
    def __init__(self, sender, ports, speeds):
        gtk.HBox.__init__(self, spacing=2)
        
        self._sender = sender
        self._image = gtk.image_new_from_stock(gtk.STOCK_NO, gtk.ICON_SIZE_BUTTON)

        #populate the combo with available serial ports
        ports.insert(0, DUMMY_PORT)
        self._portcb = self._build_combo(*ports)
        self._portcb.connect("changed", self._on_serial_port_changed)

        #and available speeds
        self._speedcb = self._build_combo(*speeds)
        self._speedcb.connect("changed", self._on_serial_speed_changed)

        self.pack_start(self._image, False)
        self.pack_start(self._portcb, expand=True)
        self.pack_start(self._speedcb, expand=False)

    def _build_combo(self, *toModel):
        cb = gtk.ComboBox()
        store = gtk.ListStore(str)
        cell = gtk.CellRendererText()
        cb.pack_start(cell, True)
        cb.add_attribute(cell, 'text', 0)
        for p in toModel:
            store.append( (p,) )
        cb.set_model(store)
        cb.set_active(0)
        return cb

    def _connect(self, port, speed):
        if port == DUMMY_PORT:
            self._sender.disconnect_from_port()
            self._image.set_from_stock(gtk.STOCK_NO, gtk.ICON_SIZE_BUTTON)
        else:
            if self._sender.connect_to_port(port=port, speed=speed):
                self._image.set_from_stock(gtk.STOCK_YES, gtk.ICON_SIZE_BUTTON)
            else:
                self._image.set_from_stock(gtk.STOCK_NO, gtk.ICON_SIZE_BUTTON)

    def _on_serial_port_changed(self, cb):
        port = self._portcb.get_active_text()
        speed = int(self._speedcb.get_active_text())
        self._connect(port, speed)

    def _on_serial_speed_changed(self, cb):
        port = self._portcb.get_active_text()
        speed = int(self._speedcb.get_active_text())
        self._connect(port, speed)


