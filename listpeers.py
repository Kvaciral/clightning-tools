#!/usr/bin/python3
from lightning import LightningRpc
import sys, os

class TermColors:
    '''
    Helper class to generate terminal control sequences.
    '''
    @staticmethod
    def rgb(hh):
        '''HTML color to terminal escape sequence'''
        assert(len(hh) == 6)
        rr = int(hh[0:2], 16)
        gg = int(hh[2:4], 16)
        bb = int(hh[4:6], 16)
        return f'\x1b[38;2;{rr};{gg};{bb}m'
    reset = '\x1b[0m' # reset to terminal defaults

def colorize(color, colorthis):
    '''
    Convert a something (color) to a terminal-colorized string.
    '''
    return T.rgb(color) + colorthis + T.reset

T = TermColors()

node = LightningRpc(os.path.join(os.getenv("HOME"), ".lightning/bitcoin/lightning-rpc"))

peers = node.listpeers()

for peer in peers['peers']:
    if len(peer['channels']) > 0:
        chan_status = peer['channels'][0]['state']
        chan_color = node.listnodes(peer["id"])['nodes'][0]['color']
        try:
            peerAlias = node.listnodes(peer["id"])['nodes'][0]['alias']
        except IndexError:
            peerAlias = "????????????????"
        except KeyError:
            peerAlias = "????????????????"
        print(peer['connected'], str(round((peer["channels"][0]["msatoshi_total"]/100000000), 1)) + " mBTC", peer["id"], colorize(chan_color, peerAlias), chan_status, str(round((peer["channels"][0]["msatoshi_to_us"]/100000000), 1)))
    else:
        if len(node.listnodes(peer["id"])['nodes']) > 0:
            print(peer['connected'], "........", peer["id"], node.listnodes(peer["id"])['nodes'][0]['alias'])
        else:
            print(peer['connected'], "........", peer["id"], "<NOT FOUND>")

if __name__ == '__main__':
    pass
