

class input_parser:

    def parse_dynamic_info_for_input(self, app_info):
        user_input = app_info.user_input
        for item in app_info.traffic_json_list:
            info = self.check_input(item['url'], user_input)
            if info:
                app_info.sensitive_json['traffic'].append((item, info))
            if item.has_key('body'):
                info = self.check_input(item['body'], user_input)
                if info:
                    app_info.sensitive_json['traffic'].append((item, info))

        for item in app_info.keychain_json_list:
            if item.has_key('attributes'):
                value = item['attributes']['kSecValueData']
            if (item.has_key('attributesToUpdate')):
                value = item['attributesToUpdate']['kSecValueData']
            info = self.check_input(value, user_input)
            if info:
                app_info.sensitive_json['keychain'].append((item, info))

        for item in app_info.plist_json_list:
            value = item['content']
            info = self.check_input(value, user_input)
            if info:
                app_info.sensitive_json['plist'].append((item, info))

        for item in app_info.userdefault_json_list:
            value = item['content']
            info = self.check_input(value, user_input)
            if info:
                app_info.sensitive_json['nsuserdefaults'].append((item, info))

        print app_info.sensitive_json

    def check_input(self, str, user_input):
        for each_input in user_input:
            if (each_input in str):
                return each_input
        return None
