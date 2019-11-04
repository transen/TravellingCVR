import hashlib
import binascii
import os

# https://www.vitoshacademy.com/hashing-passwords-in-python/ -kilde


def hash_password(password):
    """
    Hashes a password for storing in mongodb, through SHA512, with a randomly generated salt.

    TODO expand

    :param password:
    :type password: str
    :return: Hashed password
    :rtype: ????
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """
    Verify a stored password against one provided by user

    TODO expand

    :param stored_password: The password-hash retrieved from MongoDB
    :type stored_password: ????
    :param provided_password: The password provided by the user
    :type provided_password: str
    :return: True or False, depending on match
    :rtype: bool
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password