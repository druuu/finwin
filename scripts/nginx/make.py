import sys

domain_name = sys.argv[1]

with open('template', 'r') as f:
    template = f.read()

with open('template2', 'r') as f:
    template2 = f.read()

template = template.replace('domain_name', domain_name)

template3 = ''
for i in range(30):
    if i < 9:
        server_prefix = '0%d' % (i+1)
    else:
        server_prefix = '%d' % (i+1)

    tmp = template2.replace('subdomain_name', '1'+server_prefix+'.'+domain_name)
    tmp = tmp.replace('domain_name', domain_name)
    tmp = tmp.replace('server_prefix', server_prefix)

    template3 += '\n' + tmp

final_template = template + '\n\n' + template3

with open('notebook', 'w') as f:
    f.write(final_template)
