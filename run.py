from version import __version__ as version
from version import version_tag

import platform
import argparse
import logging
import yaml
import os

import uuid
import ipaddress

import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519

def keygen ( ):
	logger.info( 'Generating keys' )
	# generate private key
	# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/x25519/#cryptography.hazmat.primitives.asymmetric.x25519.X25519PublicKey.from_public_bytes
	logger.debug( 'Generating private key' )
	private_key = x25519.X25519PrivateKey.generate()

	private_bytes = private_key.private_bytes(
		encoding=serialization.Encoding.Raw,
		format=serialization.PrivateFormat.Raw,
		encryption_algorithm=serialization.NoEncryption()
	)
	# generate public key
	# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/x25519/#cryptography.hazmat.primitives.asymmetric.x25519.X25519PublicKey.from_public_bytes
	logger.debug( 'Generating public key' )
	public_key = private_key.public_key()

	public_bytes = public_key.public_bytes(
		    encoding=serialization.Encoding.Raw,
		    format=serialization.PublicFormat.Raw
	)

	# Convert keys to base64 strings
	private_key = base64.b64encode( private_bytes ).decode().strip()
	logger.debug( 'Private key: ' + private_key )

	public_key = base64.b64encode( public_bytes ).decode().strip()
	logger.info( 'Public key: ' + public_key )

	return private_key, public_key

def log_level(level_string):
	if level_string not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
		raise ValueError
	return level_string

if __name__ == '__main__':

	# Logging Set-up
	logger = logging.getLogger( __name__ )
	console_handler = logging.StreamHandler()

	level = logging.getLevelName( 'DEBUG' )
	logger.setLevel( level )

	formatter = logging.Formatter( '%(asctime)s %(levelname)s: %(message)s' )
	console_handler.setFormatter( formatter )
	logger.addHandler( console_handler )

	parser = argparse.ArgumentParser()
	parser.add_argument( '-l', '--log-level',
							dest='log_level',
							default='INFO',
							type=log_level,
							help='Valid loglevels: CRITICAL, ERROR, WARNING, INFO, DEBUG' )
	parser.add_argument( '-q', '--quiet',
							dest="quiet",
							action='store_true',
							default=False,
							help='Disable logging output' )
	parser.add_argument( '-c',
							dest='config_file',
							default=os.path.abspath( './config.yml' ),
							help='Specify a different config file' )
	parser.add_argument( '-ip',
							dest='ip_address',
							default=None,
							help='The interface IP address for the generated conf file' )
	parser.add_argument( '-k', '--PreSharedKey',
							dest='PreSharedKey',
							default=None,
							help='Pre-shared key for the generated conf file' )

	args = parser.parse_args()

	logger.disabled = args.quiet

	# Logging config
	if not logger.disabled:
		level = logging.getLevelName( args.log_level )
		logger.setLevel( level )

	if not os.path.exists( args.config_file ):
		logger.critical( 'Error: No config file found: ' + str(args.config_file) )

	# Load the configuration yaml file
	with open( args.config_file, 'r' ) as ymlfile:
		cfg = yaml.safe_load( ymlfile )

	logger.debug( platform.system() )
	logger.debug( 'Version: ' + version + ' - ' + version_tag )

	if args.ip_address != None:
		interface_ip = args.ip_address
	else:
		while True:
			interface_ip = input('Enter Interface IP [Exit]: ')
			if interface_ip in ['e', 'E', 'Exit']:
				logger.debug( 'Exit input recieved: ' + interface_ip )
				exit()
			try:
				ipaddress.ip_address(interface_ip)
			except Exception as e:
				logger.warning( 'Invalid IP address' )
				logger.warning( e )
				continue
			break

	if args.PreSharedKey != None:
		PreSharedKey = args.PreSharedKey
	else:
		while True:
			PreSharedKey = input('Enter PreSharedKey [Exit]: ')
			if PreSharedKey in ['e', 'E', 'Exit']:
				logger.debug( 'Exit input recieved: ' + PreSharedKey )
				exit()
			else:
				break

	private_key, public_key = keygen()

	output_dir = os.path.abspath( './output' )
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	filename = uuid.uuid4().hex + '.conf'

	logger.info( 'Output to: ' + filename )

	file_path = os.path.join( output_dir, filename )

	logger.debug( 'Output to: ' + file_path )

	wireguard_conf = f"""[Interface]
Address = {interface_ip}/24
DNS = {cfg['Interface']['DNS']}
MTU = {cfg['Interface']['MTU']}
PrivateKey = {private_key}

[Peer]
AllowedIPs = {cfg['Peer']['AllowedIPs']}
Endpoint = {cfg['Peer']['Endpoint']}
PreSharedKey = {PreSharedKey}
PublicKey = {cfg['Peer']['PublicKey']}"""

	logger.debug( wireguard_conf )

	with open( file_path , 'a', encoding='utf-8') as outfile:
			outfile.write( wireguard_conf )
