
from TP_LINK.widget.quick_setup_tlwr740n_v5_like import QuickSetupWidget
from TP_LINK.widget.login_page_tlwr742n_v5_like import LoginPageWidget

class Widgets(QuickSetupWidget, LoginPageWidget):
    def __init__(self):
        QuickSetupWidget.__init__(self)
        LoginPageWidget.__init__(self)
    
from TP_LINK.quick_setup_tlwr740n_v5_like import QuickSetup
    
class TL_WR740N_v5(QuickSetup):
    
    def __init__(self, *args, **kargs):
        self.widgets = Widgets()
        QuickSetup.__init__(self, *args, **kargs)