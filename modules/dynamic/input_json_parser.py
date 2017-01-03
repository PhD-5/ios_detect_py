

class input_parser:

    def parse_dynamic_info_for_input(self, app_info):
        user_input = app_info.user_input
        for item in app_info.traffic_json_list:
            self.check_input(item['msg']['url'], user_input)
            if (item['msg'].has_key('body')):
                if (self.check_input(item['msg']['body'], user_input)):
                    app_info.sensitive_json['traffic'].append(item)

        for item in app_info.keychain_json_list:
            if (item['msg'].has_key('attributes')):
                value = item['msg']['attributes']['kSecValueData']
            if (item['msg'].has_key('attributesToUpdate')):
                value = item['msg']['attributesToUpdate']['kSecValueData']
            if (self.check_input(value, user_input)):
                app_info.sensitive_json['keychain'].append(item)

        for item in app_info.plist_json_list:
            value = item['msg']['content']
            if (self.check_input(value, user_input)):
                app_info.sensitive_json['plist'].append(item)

        for item in app_info.userdefault_json_list:
            value = item['msg']['content']
            if (self.check_input(value, user_input)):
                app_info.sensitive_json['nsuserdefaults'].append(item)

        print app_info.sensitive_json


    def check_input(self, str, user_input):
        for each_input in user_input:
            if (each_input in str):
                return True
        return False
