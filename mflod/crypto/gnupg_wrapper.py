import logging
import gnupg


class GnuPGWrapper(object):
    """
    Class uses python3_gnupg wrapper and allows access to GnuPG key management,
    creation, deletion, encryption and signature functionality. It is a parent of
    the KeyManager class and gives possibility child class to utilizes logger object.

    Currently it is possible to generate/delete/retrieve RSA key pair from a local environment.

    @todo Pulls down RSA key pair from RSA key server, etc.

    Developers:
        - Tornike Nanobashvili
    """

    def __init__(self):
        """
        Instantiate GnuPGWrapper class and creates following sub instances:
            - Defines GnuPG instance
            - Defines logging instance
        """
        self.gpg = gnupg.GPG()

        self.logger = logging.getLogger(__name__)
        self.logger.debug('GnuPGWrapper instance is being created.')

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

    def del_rsa_key(self, fingerprint):
        """
        Deletes RSA key pair of provided fingerprint

        :param fingerprint: str (key HEX SHA1 fingerprint)
        :return: void
        """
        try:
            self.gpg.delete_keys(fingerprint, True)
            self.gpg.delete_keys(fingerprint, False)

            self.logger.info('RSA key pair is being deleted. Fingerprint: ' + fingerprint)
        except Exception as ERROR:
            self.logger.error(ERROR)
