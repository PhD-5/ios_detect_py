
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
        self.bundle_id = id;
        self.user_input = []
        self.traffic_json_list = []
        self.cccrtpy_json_list = []
        self.plist_json_list = []
        self.userdefault_json_list = []
        self.keychain_json_list = []
        self.mitm_list = []
        self.urlscheme_list=[]