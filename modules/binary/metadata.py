import os
from Utils.database import DBServer
from Utils.utils import Utils
import data
import plistlib



class Metadata():

    def get_metadata(self):
        self.client = data.client
        self.app = data.app_bundleID
        """Retrieve metadata of the target app."""
        # self._app = app_name
        # if self._device._applist is None:
        #     self._device._list_apps()
        return self._retrieve_metadata()

    def _retrieve_metadata(self):
        """Parse MobileInstallation.plist and the app's local Info.plist, and extract metadata."""
        # Content of the MobileInstallation plist
        # client = self.client
        app_name = self.app
        plist_global = data.app_dict[app_name]
        uuid = plist_global['BundleContainer'].rsplit('/', 1)[-1]
        name = plist_global['Path'].rsplit('/', 1)[-1]
        bundle_id = plist_global['CFBundleIdentifier']
        bundle_directory = plist_global['BundleContainer']
        data_directory = plist_global['Container']
        binary_directory = plist_global['Path']
        try:
            entitlements = plist_global['Entitlements']
        except:
            entitlements = None

        # Content of the app's local Info.plist
        path_local = Utils.escape_path('%s/Info.plist' % plist_global['Path'])
        plist_local = self.parse_plist(path_local)
        platform_version = plist_local['DTPlatformVersion']
        sdk_version = plist_local['DTSDKName']
        minimum_os = plist_local['MinimumOSVersion']
        app_version_long  = plist_local['CFBundleVersion']
        app_version_short = plist_local['CFBundleShortVersionString']
        app_version = '{} ({})'.format(app_version_long, app_version_short)
        try:
            url_handlers = plist_local['CFBundleURLTypes'][0]['CFBundleURLSchemes']
        except:
            url_handlers = None

        # Compose binary path
        binary_folder = binary_directory
        binary_name = os.path.splitext(binary_folder.rsplit('/', 1)[-1])[0]
        binary_path = Utils.escape_path(os.path.join(binary_folder, binary_name))

        # Detect architectures
        architectures = self._detect_architectures(binary_path)

        # Pack into a dict
        metadata = {
            'uuid': uuid,
            'name': name,
            'app_version': app_version,
            'bundle_id': bundle_id,
            'bundle_directory': bundle_directory,
            'data_directory': data_directory,
            'binary_directory': binary_directory,
            'binary_path': binary_path,
            'binary_name': binary_name,
            'entitlements': entitlements,
            'platform_version': platform_version,
            'sdk_version': sdk_version,
            'minimum_os': minimum_os,
            'url_handlers': url_handlers,
            'architectures': architectures,
        }
        try:
            values = (
                uuid,
                name,
                app_version,
                bundle_id,
                bundle_directory,
                data_directory,
                binary_directory,
                binary_path,
                binary_name,
                entitlements,
                platform_version,
                sdk_version,
                minimum_os,
                url_handlers,
                architectures
            )
            # print values
            # data.db.execute("INSERT INTO metadata VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", values)

            data.metadata = metadata
            return True
        except AttributeError:
            return False


    def parse_plist(self, plist):
        """Given a plist file, copy it to temp folder, convert it to XML, and run plutil on it."""
        # Copy the plist
        plist_temp = self.build_temp_path_for_file(plist.strip("'"))
        plist_copy = Utils.escape_path(plist_temp)
        self.file_copy(plist, plist_copy)
        # Convert to xml
        cmd = '{plutil} -convert xml1 {plist}'.format(plutil=data.DEVICE_TOOLS['PLUTIL'], plist=plist_copy)
        # self.command_blocking(cmd, internal=True)
        Utils.cmd_block(self.client, cmd)
        # Cat the content
        cmd = 'cat {}'.format(plist_copy)
        # out = self.command_blocking(cmd, internal=True)
        out = Utils.cmd_block(self.client, cmd)

        # Parse it with plistlib
        out = str(''.join(out).encode('utf-8'))
        pl = plistlib.readPlistFromString(out)
        return pl

    def build_temp_path_for_file(self, fname):
        """Given a filename, returns the full path for the filename in the device's temp folder."""
        return os.path.join(data.DEVICE_PATH_TEMP_FOLDER, Utils.extract_filename_from_path(fname))

    def file_copy(self, src, dst):
        src, dst = Utils.escape_path(src), Utils.escape_path(dst)
        cmd = "cp {} {}".format(src, dst)
        Utils.cmd_block(self.client, cmd)

    def _detect_architectures(self, binary):
        """Use lipo to detect supported architectures."""
        # Run lipo
        cmd = '{lipo} -info {binary}'.format(lipo=data.DEVICE_TOOLS['LIPO'], binary=binary)
        out = Utils.cmd_block(self.client, cmd)
        # Parse output
        # msg = out[0].strip()
        msg = out.strip()
        res = msg.rsplit(': ')[-1].split(' ')
        return res