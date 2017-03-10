"""
Gui for vat verification.
"""
import re
import sys
import PyQt5.QtWidgets as Qw
from afmgr import isvat, vatol, get_vat


class Vat_form(Qw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(u'Έλεγχος Ελληνικού Α.Φ.Μ.')
        mainLayout = Qw.QVBoxLayout(self)
        glay = Qw.QGridLayout()
        gla2 = Qw.QGridLayout()
        grb = Qw.QGroupBox()
        grb.setTitle(u'Αποτελέσματα αναζήτησης')
        grb.setLayout(gla2)
        buttonLayout = Qw.QHBoxLayout()
        mainLayout.addLayout(glay)
        mainLayout.addWidget(grb)
        mainLayout.addLayout(buttonLayout)
        # create widgets here
        self.afm = Qw.QLineEdit()
        self.aff = Qw.QLineEdit()
        self.dat = Qw.QLineEdit()
        self.na1 = Qw.QLineEdit()
        self.na2 = Qw.QLineEdit()
        self.ad1 = Qw.QLineEdit()
        self.ad2 = Qw.QLineEdit()
        self.tk = Qw.QLineEdit()
        # Make them read-only
        self.aff.setReadOnly(True)
        self.dat.setReadOnly(True)
        self.na1.setReadOnly(True)
        self.na2.setReadOnly(True)
        self.ad1.setReadOnly(True)
        self.ad2.setReadOnly(True)
        self.tk.setReadOnly(True)
        # Set tooltips
        self.aff.setToolTip('Α.Φ.Μ.')
        self.dat.setToolTip('Ημερομηνία ελέγχου')
        self.na1.setToolTip('Επωνυμία')
        self.na2.setToolTip('Εναλλακτική επωνυμία')
        self.ad1.setToolTip('Διεύθυνση')
        self.ad2.setToolTip('Πόλη/Περιοχή')
        self.tk.setToolTip('Ταχυδρομικός κωδικός')
        # Add widgets to layout manager
        glay.addWidget(Qw.QLabel(u'Ελληνικό ΑΦΜ για έλεγχο'), 0, 0)
        glay.addWidget(self.afm, 0, 1)
        self.bcheck = Qw.QPushButton(u'Έλεγχος')
        glay.addWidget(self.bcheck, 0, 2)
        gla2.addWidget(Qw.QLabel(u'Α.Φ.Μ.'), 0, 0)
        gla2.addWidget(self.aff, 0, 1)
        gla2.addWidget(Qw.QLabel(u'Επωνυμία1'), 1, 0)
        gla2.addWidget(self.na1, 1, 1)
        gla2.addWidget(Qw.QLabel(u'Επωνυμία2'), 2, 0)
        gla2.addWidget(self.na2, 2, 1)
        gla2.addWidget(Qw.QLabel(u'Διεύθυνση1'), 3, 0)
        gla2.addWidget(self.ad1, 3, 1)
        gla2.addWidget(Qw.QLabel(u'Διεύθυνση2'), 4, 0)
        gla2.addWidget(self.ad2, 4, 1)
        gla2.addWidget(Qw.QLabel(u'Ταχ.Κωδ.'), 5, 0)
        gla2.addWidget(self.tk, 5, 1)
        gla2.addWidget(Qw.QLabel(u'Ημερομηνία'), 6, 0)
        gla2.addWidget(self.dat, 6, 1)
        self.bclear = Qw.QPushButton(u'Καθαρισμός φόρμας')
        self.bexit = Qw.QPushButton(u'Έξοδος')
        buttonLayout.addWidget(self.bclear)
        buttonLayout.addWidget(self.bexit)
        # Connections here
        self.bcheck.clicked.connect(self.check)
        self.bclear.clicked.connect(self.clear)
        self.bexit.clicked.connect(self.accept)
        self.resize(500, 200)

    def check(self):
        self.clear()
        afm = self.afm.text()
        if len(afm) != 9:
            msg = u'Το Ελληνικό ΑΦΜ πρέπει να έχει 9 ακριβώς ψηφία'
            Qw.QMessageBox.critical(self, u"Προσοχή", msg)
            return
        gvat = get_vat(afm)
        if gvat['ok']:
            self.aff.setText(gvat['aff'])
            self.dat.setText('%s' % gvat['requestDate'])
            self.na1.setText(gvat['name'])
            self.na2.setText(gvat['name2'])
            self.ad1.setText(gvat['ad1'])
            self.ad2.setText(gvat['ad2'])
            self.tk.setText(gvat['tk'])
        else:
            Qw.QMessageBox.critical(self, u"Προσοχή", gvat['msg'])

    def clear(self):
        self.aff.setText('')
        self.dat.setText('')
        self.na1.setText('')
        self.na2.setText('')
        self.ad1.setText('')
        self.ad2.setText('')
        self.tk.setText('')


if __name__ == '__main__':
    APP = Qw.QApplication(sys.argv)
    UI = Vat_form()
    UI.show()
    sys.exit(APP.exec_())
