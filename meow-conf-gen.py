#!/usr/bin/env python3
#coding=utf-8

import urllib3
import re
import datetime
import certifi
import codecs


def get_list(listUrl):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',  # Force certificate check.
        ca_certs=certifi.where(),  # Path to the Certifi bundle.
    )

    data = http.request('GET', listUrl, timeout=10).data
    return data

def get_white_List():
    dnsmasq_china_list = 'https://github.com/R0uter/gfw_domain_whitelist/raw/master/whitelistCache'
    try:
        print('Getting white list...')
        content = get_list(dnsmasq_china_list)
        content = content.decode('utf-8')
        f = codecs.open('./list/whitelist', 'w', 'utf-8')
        f.write(content)
        f.close()
    except:
        print('Get list update failed,use cache to update instead.')

    # domainList = []
    whitelist = codecs.open('./list/whitelist','r','utf-8')
    whitelistTxt = codecs.open('./config-file-here/direct','w','utf-8')
    whitelistTxt.write('# updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S" + '\n'))
    whitelistTxt.write('.cn')
    for line in whitelist.readlines():
        domain = re.findall(r'\w+\.\w+', line)
        if len(domain) > 0:
            # domainList.append(domain[0])
            whitelistTxt.write(domain[0] + '\n')

    whitelist.close()
    whitelistTxt.close()



def get_gfw_list():
    # the url of gfwlist
    baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'

    comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    tmpfile = './list/gfwlist'

    proxy_config = codecs.open('./config-file-here/proxy', 'w', 'utf-8')
    proxy_config.write('# updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    proxy_config.write('\n')

    try:

        data = get_list(baseurl)

        content = codecs.decode(data, 'base64_codec').decode('utf-8')

        # write the decoded content to file then read line by line
        tfs = codecs.open(tmpfile, 'w', 'utf-8')
        tfs.write(content + '\n')
        tfs.close()
        print('GFW list fetched, writing...')
    except:
        print('GFW list fetch failed, use tmp instead...')
    tfs = codecs.open(tmpfile, 'r', 'utf-8')

    # Store all domains, deduplicate records
    domainList = []

    # Write list
    for line in tfs.readlines():

     if re.findall(comment_pattern, line):
         continue
     else:
         domain = re.findall(domain_pattern, line)
         if domain:
             try:
                 found = domainList.index(domain[0])
             except ValueError:
                 domainList.append(domain[0])
                 proxy_config.write(domain[0] + '\n')
         else:
             continue

    tfs.close()
    proxy_config.close()

if __name__ == '__main__':
    get_white_List()
    get_gfw_list()
