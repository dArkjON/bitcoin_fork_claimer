#!/usr/bin/env python

import urllib
import json
import sys

addresses = """
1HoMERUvzdPcE9M9NBFcBTkd2Br197d7bn
1DmoibD5dQnDc9pHiFTk1ePMm4EJD1Aoar
"""

fork_list = {
"SBTC": { "name": "Super Bitcoin", "exp": "http://block.superbtc.org/insight-api/addr/" },
"BCD": { "name": "Bitcoin Diamond", "exp": "http://52.187.7.191:3001/insight-api/addr/" },
}

desired_forks = {}

def main():
	addr_list = addresses.strip().split("\n")
	addr_list = [addr.strip() for addr in addr_list]

	global desired_forks
	desired_forks = get_desired_forks()
	#if len(desired_forks) == 0:
	print "Retrieving all forks..."
	print
	desired_forks = fork_list

	# Add balance entry per fork
	for coincode, coindata in desired_forks.viewitems():
		coindata["balances"] = {}
		for addr in addr_list:
			coindata["balances"][addr] = 0
			#print coindata["balances"][addr]
	
	
	for coindata in desired_forks.viewitems():
		#print (coindata)
		#print (coindata[0])
		print "Debug : Explorer : " + (coindata[1]["exp"])
	
	
	for addr in addr_list:
		print "Debug : Wallet : " + (addr)
		for  coindata in desired_forks.viewitems():
			#print (coincode)
		
			a = urllib.urlopen(coindata[1]["exp"] + addr).read()
			txs = json.loads(a)["balance"]

			print "Debug : Coin : " + (coindata[0])
			
			#print(coindata["exp"] + addr)
		
			print ("Debug : Balance : " + str(txs))
			#print coincode

		
		for coincode, coindata in desired_forks.viewitems():
			#valid = process_txs(addr, txs, coindata)

			#for value in valid:
			
			coindata["balances"][addr] += txs
			
			
			coindata["total_value"] = sum(coindata["balances"].values())
			
	
	if not "-balance" in sys.argv:
		#print_commands()
		print_balances()
		#print (coindata)

def print_balances():
	decimals = 1.0
	for coincode, coindata in desired_forks.viewitems():
		if coindata["total_value"] > 0:
			print
			coin_fmt = (coindata["name"] + " (" + coincode + ")").ljust(50, " ")
			total_fmt = format((coindata["total_value"] / decimals), ".8f")
			print coin_fmt + total_fmt.rjust(15, " ") + " BTC"

			for addr, balance in coindata["balances"].viewitems():
				if balance > 0:
					addr_fmt = addr.ljust(50, " ")
					balance_fmt = format((balance / decimals), ".8f")
					print addr_fmt + balance_fmt.rjust(15, " ") + " BTC "

def get_desired_forks():
	return {}
	#cli_args = get_cli_args()
	#if cli_args is None:
	#return { k : v for k, v in fork_list.iteritems() if k in cli_args }

main()

#def get_cli_args():
#	if len(sys.argv) == 1:
#		print "You can also specify which forks you want. Example: python " + sys.argv[0] + " btv bcx"
#		return None
#
#	return [arg.upper() for arg in sys.argv[1:]]

#def print_commands():
#	for coincode, coindata in desired_forks.viewitems():
#		if coindata.has_key("commands"):
#			print coindata["name"] + " (" + coincode + ")"
#			print "\n".join(coindata["commands"])
#			print

#def process_txs(addr, txs, coin):
		
#	txs_before_fork = [tx for tx in txs if tx.has_key("block_height") and tx["block_height"] <= coin["block"]]
#	valid_txs = txs_before_fork[:]
#	valid = []

	# Remove spent transactions
#	for txid in valid_txs[:]:
#		for tx in txs_before_fork:
#			for input_tx in tx["inputs"]:
#				if input_tx["prev_out"]["tx_index"] == txid["tx_index"] and input_tx["prev_out"]["addr"] == addr:
#					try:
#						valid_txs.remove(txid)
#					except ValueError:
#						pass # Was probably removed before. Skipping.
#
#	for tx in valid_txs:
#		for tx_out in tx["out"]:
#			if addr == tx_out["addr"]:
#				coin["balances"][addr] += tx_out["value"]
#				valid.append([tx["hash"], "PRIV_KEY_OF_" + addr, addr])
#				break
#
#	return valid