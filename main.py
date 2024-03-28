import json
import ctypes
import requests
import concurrent.futures
from threading import Thread
from datetime import datetime
from colorama import Fore, Back, Style, init
init()

done = 0
success = 0
failure = 0
skipped = 0

class console: # Telegram: @virusdiscord
	def success(content: str):
		print(f'{Fore.LIGHTBLACK_EX}{datetime.now().strftime("%H:%M:%S")}{Fore.RESET} [{Fore.GREEN}+{Fore.RESET}] {content}')

	def failure(content: str):
		print(f'{Fore.LIGHTBLACK_EX}{datetime.now().strftime("%H:%M:%S")}{Fore.RESET} [{Fore.RED}!{Fore.RESET}] {content}')

class cleaner: # Telegram: @virusdiscord
	def __init__(self): # Telegram: @virusdiscord
		self.config = json.loads(open('config.json', 'r').read())

	def title(self): # Telegram: @virusdiscord
		global done, success, failure, skipped
		ctypes.windll.kernel32.SetConsoleTitleW(f"Done: {done} | Deauthorized: {success} | Failures: {failure} | Skipped: {skipped}")

	def headers(self, token: str) -> dict: # Telegram: @virusdiscord
		headers = {
		    'authority': 'discord.com',
		    'accept': '*/*',
		    'authorization': token,
		    'content-type': 'application/json',
		    'origin': 'https://discord.com',
		    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
		    'sec-ch-ua-mobile': '?0',
		    'sec-ch-ua-platform': '"Windows"',
		    'sec-fetch-dest': 'empty',
		    'sec-fetch-mode': 'cors',
		    'sec-fetch-site': 'same-origin',
		    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
		    'x-debug-options': 'bugReporterEnabled',
		    'x-discord-locale': 'en-US',
		    'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InVrLVVBIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIyLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI3NTU2NSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
		}
		return headers

	def fetch(self, token: str) -> dict: # Telegram: @virusdiscord
		global done, success, failure, skipped
		r = requests.get('https://discord.com/api/v9/oauth2/tokens', headers = self.headers(token))
		if r.ok:
			console.success(f'Fetched {Fore.MAGENTA}{len(r.json())}{Fore.RESET} app(s) for {Fore.MAGENTA}{token[:31]}***{Fore.RESET} token')
			return r.json()
		else:
			failure += 1
			self.title()
			console.failure(f'Failed while getting authorized applications for {Fore.MAGENTA}{token[:31]}***{Fore.RESET} token -> {r.json()}')
			return None

	def deauthorize(self, token: str): # Telegram: @virusdiscord
		global done, success, failure, skipped
		apps = self.fetch(token)
		if apps:
			a = 0
			for app in apps:
				if int(app['application']['id']) not in self.config['APPS_TO_IGNORE']:
					r = requests.delete(f'https://discord.com/api/v9/oauth2/tokens/{app['id']}', headers = self.headers(token))
					if r.ok:
						a += 1
						success += 1
						console.success(f'Deauthorized the application {Fore.MAGENTA}{app['application']['name']}{Fore.RESET} ({Fore.MAGENTA}{app['id']}{Fore.RESET}) for {Fore.MAGENTA}{token[:31]}***{Fore.RESET} token [{Fore.MAGENTA}{a}{Fore.RESET}/{Fore.MAGENTA}{len(apps)}{Fore.RESET}]')
					else:
						failure += 1
						console.failure(r.text)
				else:
					skipped += 1
					console.success(f'Skipping {Fore.MAGENTA}{app['application']['name']}{Fore.RESET} ({Fore.MAGENTA}{app['id']}{Fore.RESET}) for {Fore.MAGENTA}{token[:31]}***{Fore.RESET} token')
				self.title()
			done += 1
			self.title()

def start(token: str): # Telegram: @virusdiscord
    instance = cleaner()
    instance = Thread(target = instance.deauthorize, args = (token,))
    instance.start()

    instance.join()

if __name__ == '__main__': # Telegram: @virusdiscord
	tokens = open("tokens.txt", "r").read().splitlines()
	config = json.loads(open('config.json', 'r').read())
	with concurrent.futures.ThreadPoolExecutor(max_workers = config['THREADS']) as executor:
		executor.map(start, tokens)