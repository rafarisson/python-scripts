#!/usr/bin/env python

# Para gerar o token: Personal access tokens (classic)
#
#	https://github.com/settings/tokens
#
# Defina os escopos para acesso à API:
#
#	repo
#		repo:invite 
#	admin:public_key
#		write:public_key
#		read:public_key
#	notifications

import argparse
import requests

GITHUB_API = "https://api.github.com"

def github_request(token, url, method="GET", params=None):
	headers = {
		"Authorization": f"Bearer {token}",
		"Accept": "application/vnd.github+json",
	}
	response = requests.request(method, url, headers=headers, params=params)
	response.raise_for_status()
	return response

def list_invitations(token):
	invitations = []
	page = 1
	while True:
		r = github_request(token, f"https://api.github.com/user/repository_invitations", params={"page": page})
		data = r.json()
		if not data:
			break
		for d in data:
			inv = {}
			inv['id'] = d['id']
			inv['repository'] = {}
			inv['repository']['full_name'] = d['repository']['full_name']
			inv['repository']['owner'] = d['repository']['owner']['login']
			invitations.append(inv)
		page += 1
	return invitations

def accept_invitation(token, inv):
	r = github_request(token, f"https://api.github.com/user/repository_invitations/{inv['id']}", method="PATCH")
	return r.status_code == 204

if __name__ == "__main__":
	arg_p = argparse.ArgumentParser(description="accept github invitations")
	arg_p.add_argument("--token", type=str, help="github token", required=True)

	args = arg_p.parse_args()

	print("search for invitations...")
	invitations = list_invitations(args.token)
	print(f"{len(invitations)} invitations.")

	print("accept invitations...")
	aceepted = []
	for inv in invitations:
		if accept_invitation(args.token, inv):
			aceepted.append(inv)
		else:
			print(f"fail to accept {inv['id'] } of {inv['repository']['full_name']}.")
	print(f"{len(aceepted)} invitations accepted.")
