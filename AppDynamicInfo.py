
class AppDynamicInfo():
    '''
    bundle_id=''
    user_input = []
    traffic_json_list = []
    cccrtpy_json_list = []
    plist_json_list = []
    userdefault_json_list = []
    keychain_json_list = []
    mitm_list = []
    '''

    def __init__(self,id):
        # socket msg from iphone tweak
        self.bundle_id             = id;
        self.user_input            = []
        self.traffic_json_list     = []
        self.cccrtpy_json_list     = []
        self.plist_json_list       = []
        self.userdefault_json_list = []
        self.keychain_json_list    = []
        self.mitm_list             = []
        self.urlscheme_list        = []

        # filted by user keyboead input
        self.sensitive_json=dict()    #key is traffic / plist / nsuserdefault / keychain  value is json list
        self.sensitive_json['traffic']        = []
        self.sensitive_json['plist']          = []
        self.sensitive_json['nsuserdefaults'] = []
        self.sensitive_json['keychain']       = []