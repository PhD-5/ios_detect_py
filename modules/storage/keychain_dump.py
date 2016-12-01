import data
from Utils.utils import Utils

class Keychain():

    # ==================================================================================================================
    # UTILS
    # ==================================================================================================================
    def __init__(self):
        self.client = data.client
        self.options = dict()
        # self.options['filter'] = data.metadata['binary_name']
        # self.options['output'] = self.local_op.build_temp_path_for_file(self, "keychain-dump.txt")

    # ==================================================================================================================
    # RUN
    # ==================================================================================================================
    def dump(self):
        # Composing the command string
        cmd = '{}'.format(data.DEVICE_TOOLS['KEYCHAINDUMPER'])
        # cmd += ' | grep "{}" -A 3 -B2'.format(self.options['filter'])

        # Dump Keychain
        out = Utils.cmd_block(self.client, cmd)

        print out

        # Check output
        # if out and filter(lambda x: "README" not in x, out):
        #     # Save to file
        #     outfile = self.options['output'] if self.options['output'] else None
        #     print out
        # else:
        #     if self.options['filter']:
        #         print('No content matches the filter. Ensure the screen is unlocked before dumping the keychain')
        #     else:
        #         print('No content found. Ensure the screen is unlocked before dumping the keychain')
