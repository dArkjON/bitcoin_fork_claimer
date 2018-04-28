#!/usr/bin/env python

import urllib
import json
import sys

addresses = """
1Q7Jmho4FixWBiTVcZ5aKXv4rTMMp6CjiD
1DmoibD5dQnDc9pHiFTk1ePMm4EJD1Aoar
"""

fork_list = {
"SBTC": { "name": "Super Bitcoin", "exp": "http://block.superbtc.org/insight-api/addr/" },
"BCD": { "name": "Bitcoin Diamond", "exp": "http://52.187.7.191:3001/insight-api/addr/" }
}

def main():
	addr_list = addresses.strip().split("\n")
	addr_list = [addr.strip() for addr in addr_list]

	for coincode, coindata in fork_list.viewitems():
		coindata["balances"] = {}
		for addr in addr_list:
			coindata["balances"][addr] = 0
			coindata["total_value"] = 0

	for coindata in fork_list.viewitems():
		print "Debug : Explorer : " + (coindata[1]["exp"])

	for addr in addr_list:
		print "Debug : Wallet : " + (addr)
		
		for coindata in fork_list.viewitems():
      
			a = urllib.urlopen(coindata[1]["exp"] + addr).read()
			txs = json.loads(a)["balance"]
			print "Debug : Coin : " + (coindata[0])
			print("Debug : Balance : " + str(txs))
			coindata[1]["balances"][addr] = txs
			
	for coindata in fork_list.viewitems():
	  coindata[1]["total_value"] = sum(coindata[1]["balances"].values())

	if not "-balance" in sys.argv:
		print_balances()

def print_balances():
  
	for coincode, coindata in fork_list.viewitems():
		if coindata["total_value"] > 0:
			print
			coin_fmt = (coindata["name"] + " (" + coincode + ")").ljust(
			    50, " ")
			total_fmt = format((coindata["total_value"] / 1), ".8f")
			print coin_fmt + total_fmt.rjust(15, " ") + " BTC"

			for addr, balance in coindata["balances"].viewitems():
				if balance > 0:
					addr_fmt = addr.ljust(50, " ")
					balance_fmt = format((balance / 1), ".8f")
					print addr_fmt + balance_fmt.rjust(15, " ") + " BTC "

main()