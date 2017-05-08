import logging
import gnupg


class KeyManager(object):
    """
    class is responsible for managing and retrieving GPG keys from GPG keychain

        Specifically, goal is to provide GPG key pairs:
            - GPG key ID
            - GPG public key
            - GPG private key

        Class uses GPG wrapper behind the scene (python3-gnupg package).

        Developers:
            - Tornike Nanobashvili
    """

    def __init__(self):
        """
        Initialize KeyManager class

        Processes:
            - Defines GnuPG instance
            - Defines logging basic configuration
        """
        self.gpg = gnupg.GPG()

        logging.basicConfig(filename='../../log/key_manager.log', level=logging.DEBUG)

        self.logger = logging.getLogger(__name__)
        self.logger.debug('KeyManager instance is being created.')

    def gen_rsa_key(self, key_length=2048, user_name='Auto Generated Key', user_comment='Generated by KeyManager',
                    user_email=''):
        """
        Generates RSA key pair

        :param key_length: int (defaults to 2048 bits)
        :param user_name: str (defaults to Auto Generated Key)
        :param user_comment: str (defaults to Generated by KeyManager)
        :param user_email: str (defaults to <username>@<hostname> of local environment)

        :return: str (RSA key fingerprint (SHA1))
        """
        try:
            input_data = self.gpg.gen_key_input(key_type='RSA', key_length=key_length, name_real=user_name,
                                                name_comment=user_comment, name_email=user_email)
            key = self.gpg.gen_key(input_data)

            self.logger.info('RSA ' + '(' + str(key_length) + ' bits) key pair is being generated. Fingerprint: ' +
                             str(key))

            return key.fingerprint
        except Exception as ERROR:
            self.logger.error(ERROR)
